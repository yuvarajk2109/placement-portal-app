<template>
    <div class="auth-page">
        <div class="auth-card card">
            <h1 class="page-title text-center mb-24">Student Registration</h1>

            <form @submit.prevent="handleRegister">
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="register_no">Register Number <span class="required">(required)</span></label>
                        <input id="register_no" v-model="form.register_no" @blur="touched.register_no = true" type="text" class="form-input" :class="{ 'is-error': touched.register_no && errors.register_no }" maxlength = "10">
                        <span v-if="touched.register_no && errors.register_no" class="form-error-text">{{ errors.register_no }}</span>
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="branch_id">Branch <span class="required">(required)</span></label>
                        <select id="branch_id" v-model="form.branch_id" @blur="touched.branch_id = true" class="form-select" :class="{ 'is-error': touched.branch_id && errors.branch_id }">
                            <option value="" disabled>Select Branch</option>
                            <option 
                            v-for="branch in branches"
                            :key = "branch.branch_id"
                            :value = "branch.branch_id">
                                {{ branch.branch_name }}
                            </option>
                        </select>
                        <span v-if="touched.branch_id && errors.branch_id" class="form-error-text">{{ errors.branch_id }}</span>
                    </div>
                </div>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="fname">First Name <span class="required">(required)</span></label>
                        <input id="fname" v-model="form.fname"  @blur="touched.fname = true" type="text" class="form-input" :class="{ 'is-error': touched.fname && errors.fname }">
                        <span v-if="touched.fname && errors.fname" class="form-error-text">{{ errors.fname }}</span>
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="lname">Last Name <span class="required">(required)</span></label>
                        <input id="lname" v-model="form.lname" @blur="touched.lname = true" type="text" class="form-input" :class="{ 'is-error': touched.lname && errors.lname }">
                        <span v-if="touched.lname && errors.lname" class="form-error-text">{{  errors.lname }}</span>
                    </div>
                </div>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="dob">Date of Birth <span class="required">(required)</span></label>
                        <input id="dob" v-model="form.dob" @blur="touched.dob = true" type="date" class="form-input" :class="{ 'is-error': touched.dob && errors.dob }">
                        <span v-if="touched.dob && errors.dob" class="form-error-text">{{ errors.dob }}</span>
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="phone">Phone Number</label>
                        <input id="phone" v-model="form.phone" type="text" class="form-input">
                    </div>
                </div>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="email">University Email Address <span class="required">(required)</span></label>
                        <input id="email" v-model="form.email" @blur="touched.email = true" type="email" class="form-input" :class="{ 'is-error': touched.email && errors.email }">
                        <span v-if="touched.email && errors.email" class="form-error-text">{{ errors.email }}</span>
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="cgpa">Current CGPA (as of latest even semester)<span class="required">(required)</span></label>
                        <input id="cgpa" v-model="form.cgpa" @blur="touched.cgpa = true" type="text" class="form-input" :class="{ 'is-error': touched.cgpa && errors.cgpa }">
                        <span v-if="touched.cgpa && errors.cgpa" class="form-error-text">{{ errors.cgpa }}</span>
                    </div>
                </div>
                <div class="form-group">
                    <label class="form-label" for="password">Password <span class="required">(required)</span></label>
                    <input id="password" v-model="form.password" @blur="touched.password" type="password" class="form-input" :class="{ 'is-error': touched.password && errors.password }">
                    <span v-if="touched.password && errors.password" class="form-error-text">{{ errors.password }}</span>
                </div>
                <button type="submit" class="btn is-primary is-large full-width-btn" :disabled="loading || !isFormValid">
                    {{ loading ? 'Registering...' : 'Register' }}
                </button>
            </form>
            <div class="auth-links mt-16">
                <p class="text-subtle">
                    Already have an account?
                </p>
                <p class="mt-4">
                    <router-link to="/login" class="text-link">Sign in</router-link>
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
    password: '',
    backendError: null
});

watch(form, () => {
    if (form.backendError) {
        form.backendError = null;
    }
}, { deep: true });

const touched = reactive({
    register_no: false,
    branch_id: false,
    fname: false,
    lname: false,
    dob: false,
    email: false,
    cgpa: false,
    password: false
});

onMounted(async () => {
    try {
        const result = await api.get('shared/branches');
        branches.value = result.data.branches;
    } catch (err) {
        notify.error("Failed to load branches. Please try again later.");
    }
})

const errors = computed(() => {
    const e = {};

    if (form.backendError) {
        e[form.backendError.field] = form.backendError.message;
    }

    if (form.register_no && (form.register_no.length !== 10 || !/^\d{10}$/.test(form.register_no))) {
        e.register_no = 'Invalid register no.';
    } else if (!form.register_no) {
        e.register_no = 'Register no. is required'
    }

    if (!form.branch_id) {
        e.branch_id = 'Please select a branch';
    } else if (form.register_no.length === 10 && /^\d{10}$/.test(form.register_no)) {
        const dept_id = parseInt(form.register_no.substring(4,7));
        const selected_branch = branches.value.find(b => b.branch_id === form.branch_id);
        if (selected_branch && selected_branch.dept_id !== dept_id) {
            e.branch_id = 'Branch doesn\'t match department ID in register no.';
        }
    }

    if (!form.fname) e.fname = 'First name is required';
    if (!form.lname) e.lname = 'Last name is required';
    if (!form.dob) e.dob = 'Date of Birth is required';

    if (!form.email) {
        e.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(form.email)) {
        e.email = 'Enter a valid email address';
    }

    if (!form.cgpa) {
        e.cgpa = 'CGPA is required';
    } else if (parseFloat(form.cgpa) < 0 || parseFloat(form.cgpa) > 10) {
        e.cgpa = 'Invalid CGPA';
    }

    if (!form.password) {
        e.password = 'Password is required';
    } else if (form.password.length < 6) {
        e.password = 'Must be at least 6 characters';
    }

    return e;
})

const isFormValid = computed(() =>
    Object.keys(errors.value).length === 0
);

async function handleRegister() {
    Object.keys(touched).forEach(k => touched[k] = true);
    if (!isFormValid.value) return;
    loading.value = true;
    try {
        await api.post('/auth/register/student', form);
        notify.success('Registration successful. Please check your email for OTP verification.');
        router.push({
            name: 'verify-otp',
            query: {
                email: form.email
            }
        })
    } catch (err) {
        const backendError = err.response?.data?.error || '';
        if (backendError.toLowerCase().includes('register number')) {
            form.backendError = {
                field: 'register_no',
                message: backendError
            }
        } else if (backendError.toLowerCase().includes('branch')) {
            form.backendError = {
                field: 'branch_id',
                message: backendError
            }
        } else if (backendError.toLowerCase().includes('email')) {
            form.backendError = {
                field: 'email',
                message: backendError
            }
        } else {
            notify.error(backendError || 'Registration failed');
        }
    } finally {
        loading.value = false;
    }
}
</script>