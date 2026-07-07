<template>
    <div class="auth-page">
        <div class="auth-card card">
            <h1 class="page-title text-center mb-24">Login</h1>

            <form @submit.prevent="handleLogin">
                <div class="form-group">
                    <label class="form-label" for="email">Email <span class="required">(required)</span></label>
                    <input id="email" v-model="email" type="email" class="form-input" placeholder="Enter your email" />
                    <span v-if="errors.email" class="form-error-text">{{ errors.email }}</span>
                </div>
                <div class="form-group">
                    <label class="form-label" for="password">Password <span class="required">(required)</span></label>
                    <input id="password" v-model="password" type="password" class="form-input" placeholder="Enter your password" />
                    <span v-if="errors.password" class="form-error-text">{{ errors.password }}</span>
                </div>                
                <button
                type="submit"
                class="btn is-primary is-large full-width-btn">
                    Sign in
                </button>
            </form>

            <div class="auth-links mt-16">
                <p class="text-subtle">Don't have an account?</p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.auth-card {
    margin: auto;
    width: 420px;
}

.auth-links {
  text-align: center;
  font-size: 13px;
}
</style>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { useNotificationStore } from '@/stores/notification';
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const authStore = useAuthStore();
const notify = useNotificationStore();

const email = ref('');
const password = ref('');
const errors = reactive({ email: '', password: ''});

async function handleLogin() {
    errors.email = !email.value ? 'Email is required' : '';
    errors.password = !password.value ? 'Password is required' : '';
    if (errors.email || errors.password) return;
    
    const result = await authStore.login(email.value, password.value);
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