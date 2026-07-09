<template>
    <div class="auth-page">
        <div class="auth-card card">
            <h1 class="page-title">Verify Email</h1>

            <form v-if="step === 'request'" @submit.prevent="handleRequestOTP">
                <p class="page-subtitle">Enter your registered email to receive the OTP</p>
                <div class="form-group">
                    <label class="form-label" for="email">Email Address</label>
                    <input id="email" v-model="email" type="email" class="form-input">
                </div>
                <button type="submit" class="btn is-primary is-large full-width-btn" :disabled="loading || !email">
                    {{ loading ? 'Sending...' : 'Send OTP' }}
                </button>
            </form>
            <form v-else @submit.prevent="handleVerify">
                <p class="page-subtitle">Enter the 6-digit OTP sent to {{ email }}</p>
                <div class="form-group">
                    <label class="form-label" for="otp">One-Time Password</label>
                    <input id="otp" v-model="otp" type="text" class="form-input otp" maxlength = "6">
                </div>
                <button type="submit" class="btn is-primary is-large full-width-btn" :disabled="loading || !otp">
                    {{ loading ? 'Verifying...' : 'Verify OTP' }}
                </button>
            </form>
        </div>
    </div>
</template> 

<style scoped>
.form-input.otp {
    font-size: 24px;
    letter-spacing: 4px;
    text-align: center;
}
</style>

<script setup>
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const router = useRouter();
const route = useRoute();
const notify = useNotificationStore();

const email = ref('');
const otp = ref('');
const loading = ref(false);
const step = ref('request');

onMounted(() => {
    if (route.query.email) {
        email.value = route.query.email;
        step.value = 'verify';
    }
})

async function handleRequestOTP() {
    if (!email.value) return;
    loading.value = true;
    try {
        await api.post('/auth/resend-otp', {
            email: email.value
        });
        notify.success('OTP sent. Please check your email');
        step.value = 'verify';
        otp.value = '';
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to send OTP');
    } finally {
        loading.value = false;
    }
}

async function handleVerify() {
    loading.value = true;
    try {
        await api.post('/auth/verify-otp', {
            email: email.value,
            otp: otp.value
        })
        notify.success('Email verified successfully! You can now login');
        router.push('/login');
    } catch (err) {
        notify.error(err.response?.data?.error || 'Invalid OTP');
    } finally {
        loading.value = false;
    }
}
</script>