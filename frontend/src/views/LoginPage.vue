<template>
    <div class="auth-page">
        <div class="auth-card card">
            <h1 class="page-title text-center mb-24">Login</h1>

            <form @submit.prevent="handleLogin">
                <div class="form-group">
                    <label class="form-label" for="email">Email <span class="required">(required)</span></label>
                    <input id="email" v-model="form.email" @blur="touched.email = true" type="email" class="form-input" :class="{ 'is-error': touched.email && errors.email }" placeholder="Enter your email">
                    <span v-if="touched.email && errors.email" class="form-error-text">{{ errors.email }}</span>
                </div>
                <div class="form-group">
                    <label class="form-label" for="password">Password <span class="required">(required)</span></label>
                    <input id="password" v-model="form.password" @blur="touched.password = true" type="password" class="form-input" :class="{ 'is-error': touched.password && errors.password }" placeholder="Enter your password">
                    <span v-if="touched.password && errors.password" class="form-error-text">{{ errors.password }}</span>
                </div>                
                <button
                type="submit"
                class="btn is-primary is-large full-width-btn"
                :disabled="authStore.loading || !isFormValid">
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
import { computed, reactive } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const authStore = useAuthStore();
const notify = useNotificationStore();

const form = reactive({ email: '', password: '' });
const touched = reactive({ email: false, password: false });

const errors = computed(() => {
    const e = {};
    if (!form.email) {
        e.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(form.email)) {
        e.email = 'Enter a valid email address';
    }
    if (!form.password) {
        e.password = 'Password is required';
    }
    return e;
})

const isFormValid = computed(() => {
    return Object.keys(errors.value).length === 0;
})

async function handleLogin() {
    // Mark all as touched on submit attempt
    touched.email = true;
    touched.password = true;

    if (!isFormValid.value) return;
    
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