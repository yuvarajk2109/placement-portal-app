<template>
    <div class="auth-page">
        <div class="auth-card card">
            <h1 class="page-title text-center mb-24">Student Registration</h1>

            <form @submit.prevent="handleRegister">
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="register_no">Register Number <span class="required">(required)</span></label>
                        <input id="register_no" v-model="form.register_no" @blur="validator.register_no.$touch()" type="text" class="form-input" :class="{ 'is-error': validator.register_no.$error }" maxlength="10">
                        <span v-if="validator.register_no.$error" class="form-error-text">{{ validator.register_no.$errors[0].$message }}</span>
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="branch_id">Branch <span class="required">(required)</span></label>
                        <select id="branch_id" v-model="form.branch_id" @blur="validator.branch_id.$touch()" class="form-select" :class="{ 'is-error': validator.branch_id.$error }">
                            <option value="" disabled>Select Branch</option>
                            <option 
                            v-for="branch in branches"
                            :key="branch.branch_id"
                            :value="branch.branch_id">
                                {{ branch.branch_name }}
                            </option>
                        </select>
                        <span v-if="validator.branch_id.$error" class="form-error-text">{{ validator.branch_id.$errors[0].$message }}</span>
                    </div>
                </div>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="fname">First Name <span class="required">(required)</span></label>
                        <input id="fname" v-model="form.fname" @blur="validator.fname.$touch()" type="text" class="form-input" :class="{ 'is-error': validator.fname.$error }">
                        <span v-if="validator.fname.$error" class="form-error-text">{{ validator.fname.$errors[0].$message }}</span>
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="lname">Last Name <span class="required">(required)</span></label>
                        <input id="lname" v-model="form.lname" @blur="validator.lname.$touch()" type="text" class="form-input" :class="{ 'is-error': validator.lname.$error }">
                        <span v-if="validator.lname.$error" class="form-error-text">{{ validator.lname.$errors[0].$message }}</span>
                    </div>
                </div>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="dob">Date of Birth <span class="required">(required)</span></label>
                        <input id="dob" v-model="form.dob" @blur="validator.dob.$touch()" type="date" class="form-input" :class="{ 'is-error': validator.dob.$error }">
                        <span v-if="validator.dob.$error" class="form-error-text">{{ validator.dob.$errors[0].$message }}</span>
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="phone">Phone Number</label>
                        <input id="phone" v-model="form.phone" type="text" class="form-input">
                    </div>
                </div>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="email">University Email Address <span class="required">(required)</span></label>
                        <input id="email" v-model="form.email" @blur="validator.email.$touch()" type="email" class="form-input" :class="{ 'is-error': validator.email.$error }">
                        <span v-if="validator.email.$error" class="form-error-text">{{ validator.email.$errors[0].$message }}</span>
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="cgpa">Current CGPA (as of latest even semester)<span class="required">(required)</span></label>
                        <input id="cgpa" v-model="form.cgpa" @blur="validator.cgpa.$touch()" type="text" class="form-input" :class="{ 'is-error': validator.cgpa.$error }">
                        <span v-if="validator.cgpa.$error" class="form-error-text">{{ validator.cgpa.$errors[0].$message }}</span>
                    </div>
                </div>
                <div class="form-group">
                    <label class="form-label" for="password">Password <span class="required">(required)</span></label>
                    <input id="password" v-model="form.password" @blur="validator.password.$touch()" type="password" class="form-input" :class="{ 'is-error': validator.password.$error }">
                    <span v-if="validator.password.$error" class="form-error-text">{{ validator.password.$errors[0].$message }}</span>
                </div>
                <button type="submit" class="btn is-primary is-large full-width-btn" :disabled="loading || validator.$invalid">
                    {{ loading ? 'Registering...' : 'Register' }}
                </button>
            </form>
            <div class="auth-links mt-16">
                <p>
                    Already have an account? Need to login or verify?
                </p>
                <p class="mt-4">
                    <router-link to="/login" class="text-link">Sign in</router-link>
                    &middot;
                    <router-link to="/verify-otp" class="text-link">Verify OTP</router-link>
                </p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.auth-card {
    width: 800px;
}
</style>

<script setup>
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { useVuelidate } from '@vuelidate/core';
import { helpers, maxValue, minLength, minValue, required } from '@vuelidate/validators';
import { computed, onMounted, reactive, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();
const notify = useNotificationStore();
const loading = ref(false);
const branches = ref([]);

const form = reactive({
    register_no: '',
    branch_id: '',
    fname: '',
    lname: '',
    dob: '',
    phone: '',
    email: '',
    cgpa: '',
    password: ''
});

const $externalResults = ref({});

watch(form, () => {
    $externalResults.value = {};
}, { deep: true });

onMounted(async () => {
    try {
        const result = await api.get('shared/branches');
        branches.value = result.data.branches;
    } catch (err) {
        notify.error("Failed to load branches. Please try again later.");
    }
})

const isValidRegisterNo = helpers.regex(/^\d{10}$/);
const isValidEmail = helpers.regex(/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/);

const matchesDepartment = (value) => {
    if (!form.register_no || form.register_no.length !== 10 || !/^\d{10}$/.test(form.register_no)) return true;
    const dept_id = parseInt(form.register_no.substring(4,7));
    const selected_branch = branches.value.find(b => b.branch_id === value);
    if (!selected_branch) return true;
    return selected_branch.dept_id === dept_id;
};

const rules = computed(() => ({
    register_no: { 
        required: helpers.withMessage('Register no. is required', required),
        valid: helpers.withMessage('Invalid register no.', isValidRegisterNo)
    },
    branch_id: { 
        required: helpers.withMessage('Please select a branch', required),
        matchesDept: helpers.withMessage('Branch doesn\'t match department ID in register no.', matchesDepartment)
    },
    fname: { required: helpers.withMessage('First name is required', required) },
    lname: { required: helpers.withMessage('Last name is required', required) },
    dob: { required: helpers.withMessage('Date of Birth is required', required) },
    email: { 
        required: helpers.withMessage('Email is required', required),
        valid: helpers.withMessage('Enter a valid email address', isValidEmail)
    },
    cgpa: { 
        required: helpers.withMessage('CGPA is required', required),
        min: helpers.withMessage('Invalid CGPA', minValue(0)),
        max: helpers.withMessage('Invalid CGPA', maxValue(10))
    },
    password: { 
        required: helpers.withMessage('Password is required', required),
        min: helpers.withMessage('Must be at least 6 characters', minLength(6))
    }
}));

const validator = useVuelidate(rules, form, { $externalResults });

async function handleRegister() {
    validator.value.$touch();
    if (validator.value.$invalid) return;
    
    loading.value = true;
    try {
        const result = await api.post('/auth/register/student', form);
        notify.success(result.data?.message || 'Registration successful. Please check your email for OTP verification.');
        router.push({
            name: 'verify-otp',
            query: { email: form.email }
        });
    } catch (err) {
        const backendError = err.response?.data?.error || '';
        const lowercaseError = backendError.toLowerCase();
        
        if (lowercaseError.includes('register number')) {
            $externalResults.value = { register_no: backendError };
        } else if (lowercaseError.includes('branch')) {
            $externalResults.value = { branch_id: backendError };
        } else if (lowercaseError.includes('email')) {
            $externalResults.value = { email: backendError };
        } else {
            notify.error(backendError || 'Registration failed');
        }
    } finally {
        loading.value = false;
    }
}
</script>