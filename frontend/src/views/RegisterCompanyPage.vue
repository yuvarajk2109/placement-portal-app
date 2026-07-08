<template>
    <div class="auth-page">
        <div class="auth-card card">
            <h1 class="page-title text-center mb-24">Company Registration</h1>

            <form>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="company_name">Company Name <span class="required">(required)</span></label>
                        <input id="company_name" v-model="form.company_name" @blur="touched.company_name = true" type="text" class="form-input" :class="{ 'is-error': touched.company_name && errors.company_name}">
                        <span v-if="touched.company_name && errors.company_name" class="form-error-text">{{ errors.company_name }}</span>
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="industry">Industry</label>
                        <input id="industry" v-model="form.industry" type="text" class="form-input">
                    </div>
                </div>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="website">Website <span class="required">(required)</span></label>
                        <input id="website" v-model="form.website" type="url" class="form-input">
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="location">Location</label>
                        <input id="location" v-model="form.location" type="text" class="form-input">
                    </div>
                </div>
                <div class="form-group">
                    <label class="form-label" for="description">Company Description</label>
                    <textarea id="description" v-model="form.description" class="form-input" rows="3"></textarea>
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
                    <input id="hr_email" v-model="form.hr_email" @blur="touched.hr_email = true" type="email" class="form-input" :class="{ 'is-error': touched.hr_email && errors.hr_email }">
                    <span v-if="touched.hr_email && errors.hr_email" class="form-error-text">{{ errors.hr_email }}</span>
                </div>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="email">Login Email <span class="required">(required)</span></label>
                        <input id="email" v-model="form.email" @blur="touched.email = true" type="email" class="form-input" :class="{ 'is-error': touched.email && errors.email }">
                        <span v-if="touched.email && errors.email" class="form-error-text">{{ errors.email }}</span>
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="password">Password</label>
                        <input id="password" v-model="form.password" @blur="touched.password = true" type="password" class="form-input" :class="{ 'is-error': touched.password }">
                        <span v-if="touched.password && errors.password" class="form-error-text">{{ errors.password }}</span>
                    </div>
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
import { useNotificationStore } from '@/stores/notification';
import { computed, reactive, ref, watch } from 'vue';
import { useRouter } from 'vue-router';

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
    password: '',
    backendError: null
})

watch(form, () => {
    if (form.backendError) {
        form.backendError = null
    }
}, { deep: true });

const touched = reactive({
    company_name: false,
    hr_email: false,
    email: false,
    password: false
})

const errors = computed(() => {
    const e = {};

    if (form.backendError) {
        e[form.backendError.field] = form.backendError.message;
    }

    if (!form.hr_email) {
        e.hr_email = 'HR Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(form.email).test(form.hr_email)) {
        e.hr_email = 'Enter a valid email address';
    }

    if (!form.email) {
        e.email = 'Login email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(form.email).test(form.hr_email)) {
        e.email = 'Enter a valid email address';
    }

    if (!form.password) {
        e.password = 'Password is required';
    } else if (form.password.length < 6) {
        e.password = 'Password must be at least 6 characters';
    }

    return e;
})

const isFormValid = computed(() => Object.keys(errors.value).length === 0);

async function handleRegister() {
    Object.keys(touched).forEach(k => touched[k] = true);
    if (!isFormValid.value) return;
    loading.value = true;

    try {
        await api.post('/auth/register/company', form);
        notify.success('Registration successful! Awaiting admin approval.');
        router.push('/login');
    } catch (err) {
        const backendError = err.response?.data?.error || '';
        
        if (backendError.toLowerCase().includes('email')) {
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