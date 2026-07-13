<template>
    <div class="auth-page">
        <div class="auth-card card">
            <h1 class="page-title text-center mb-24">Company Registration</h1>

            <form @submit.prevent="handleRegister">
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="company_name">Company Name <span class="required">(required)</span></label>
                        <input id="company_name" v-model="form.company_name" @blur="validator.company_name.$touch()" type="text" class="form-input" :class="{ 'is-error':  validator.company_name.$error }">
                        <span v-if="validator.company_name.$error" class="form-error-text">{{ validator.company_name.$errors[0].$message }}</span>
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="industry">Industry</label>
                        <input id="industry" v-model="form.industry" type="text" class="form-input">
                    </div>
                </div>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="website">Website</label>
                        <input id="website" v-model="form.website" type="url" class="form-input">
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="location">Location</label>
                        <input id="location" v-model="form.location" type="text" class="form-input">
                    </div>
                </div>
                <div class="form-group">
                    <label class="form-label" for="description">Company Description</label>
                    <textarea id="description" v-model="form.description" class="form-textarea"></textarea>
                </div>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="hr_name">HR Name</label>
                        <input id="hr_name" v-model="form.hr_name" class="form-input">
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="hr_phone">HR Phone Number</label>
                        <input id="hr_phone" v-model="form.hr_phone" type="text" class="form-input">
                    </div>
                </div>
                <div class="form-group">
                    <label class="form-label" for="hr_email">HR Email <span class="required">(required)</span></label>
                    <input id="hr_email" v-model="form.hr_email" @blur="validator.hr_email.$touch()" type="email" class="form-input" :class="{ 'is-error': validator.hr_email.$error }">
                    <span v-if="validator.hr_email.$error" class="form-error-text">{{ validator.hr_email.$errors[0].$message }}</span>
                </div>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="email">Login Email <span class="required">(required)</span></label>
                        <input id="email" v-model="form.email" @blur="validator.email.$touch()" type="email" class="form-input" :class="{ 'is-error': validator.email.$error }">
                        <span v-if="validator.email.$error" class="form-error-text">{{ validator.email.$errors[0].$message }}</span>
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="password">Password <span class="required">(required)</span></label>
                        <input id="password" v-model="form.password" @blur="validator.password.$touch()" type="password" class="form-input" :class="{ 'is-error': validator.password.$error }">
                        <span v-if="validator.password.$error" class="form-error-text">{{ validator.password.$errors[0].$message }}</span>
                    </div>
                </div>
                <button type="submit" class="btn is-primary is-large full-width-btn" :disabled="loading || validator.$invalid">
                    {{ loading ? 'Registering...' : 'Register' }}
                </button>
            </form>
            <div class="auth-links mt-16">
                <p>
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
import { useNotificationStore } from '@/stores/notification';
import { computed, reactive, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import { helpers, minLength, required } from '@vuelidate/validators';
import useVuelidate from '@vuelidate/core';

const router = useRouter();
const notify = useNotificationStore();
const loading = ref(false);

const form = reactive({
    company_name:'',
    industry: '',
    website: '',
    location: '',
    description: '',
    hr_name: '',
    hr_phone: '',
    hr_email: '',
    email: '',
    password: ''
})

const $externalResults = ref({});

watch(form, () => {
    $externalResults.value = {};
}, { deep: true });

const isValidEmail = helpers.regex(/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/);

const rules = computed(() => ({
    company_name: {
        required: helpers.withMessage('Company name is required', required)
    },
    hr_email: {
        required: helpers.withMessage('HR Email is required', required),
        valid: helpers.withMessage('Invalid email address', isValidEmail)
    },
    email: {
        required: helpers.withMessage('Company login email is required', required),
        valid: helpers.withMessage('Invalid email address', isValidEmail)
    },
    password: {
        required: helpers.withMessage('Password is required', required),
        valid: helpers.withMessage('Password must have at least 6 characters', minLength(6))
    }
}));

const validator = useVuelidate(rules, form, { $externalResults })

async function handleRegister() {
    validator.value.$touch();
    if (validator.value.$invalid) return;

    loading.value = true;

    try {
        await api.post('/auth/register/company', form);
        notify.success('Registration successful! Awaiting admin approval.');
        router.push('/login');
    } catch (err) {
        const backendError = err.response?.data?.error || '';
        const lowercaseError = backendError.toLowerCase();
        
        if (lowercaseError.includes('email')) {
            $externalResults.value = { email: backendError }
        } else {
            notify.error(backendError || 'Registration failed');
        }
    } finally {
        loading.value = false;
    }
}
</script>