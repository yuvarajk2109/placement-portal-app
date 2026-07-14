<template>
    <div class="auth-page">
        <div class="auth-card card">
            <h1 class="page-title text-center mb-24">Login</h1>

            <form @submit.prevent="handleLogin">
                <div class="form-group">
                    <label class="form-label" for="email">Email <span class="required">(required)</span></label>
                    <input id="email" v-model="form.email" @blur="validator.email.$touch()" type="email" class="form-input" :class="{ 'is-error': validator.email.$error }" placeholder="Enter your email">
                    <span v-if="validator.email.$error" class="form-error-text">{{ validator.email.$errors[0].$message }}</span>
                </div>
                <div class="form-group">
                    <label class="form-label" for="password">Password <span class="required">(required)</span></label>
                    <input id="password" v-model="form.password" @blur="validator.password.$touch()" type="password" class="form-input" :class="{ 'is-error': validator.password.$error }" placeholder="Enter your password">
                    <span v-if="validator.password.$error" class="form-error-text">{{ validator.password.$errors[0].$message }}</span>
                </div>                
                <button
                type="submit"
                class="btn is-primary is-large full-width-btn"
                :disabled="authStore.loading || validator.$invalid">
                    {{ authStore.loading? 'Signing in...' : 'Sign in' }}
                </button>
            </form>

            <div class="auth-links mt-16">
                <p>
                    Don't have an account?
                </p>
                <p class="mt-4">
                <router-link to="/register/student" class="text-link">Register as Student</router-link>
                &middot; 
                <router-link to="/register/company" class="text-link">Register as Company</router-link>
                </p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.auth-card {
    margin: auto;
    width: 420px;
}
</style>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { useNotificationStore } from '@/stores/notification';
import useVuelidate from '@vuelidate/core';
import { helpers, required } from '@vuelidate/validators';
import { computed, reactive } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const authStore = useAuthStore();
const notify = useNotificationStore();

const form = reactive({ email: '', password: '' });

const isValidEmail = helpers.regex(/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/);

const rules = computed(() => ({
    email: {
        required: helpers.withMessage('Login email is required', required),
        valid: helpers.withMessage('Invalid email address', isValidEmail)
    },
    password: {
        required: helpers.withMessage('Password is required', required)
    }
}));

const validator = useVuelidate(rules, form);

async function handleLogin() {
    validator.value.$touch();
    if (validator.value.$invalid) return;
    
    const result = await authStore.login(form.email, form.password);
    if (result.success) {
        notify.success('Login successful');
        const dashboards = {
            admin: 'admin-dashboard',
            company: 'company-dashboard',
            student: 'student-dashboard'
        };
        router.push({ name: dashboards[authStore.userRole] || 'home'})
    } else {
        notify.error(result.error);
    }
}
</script>