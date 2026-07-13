<template>
    <div class="main-page">
       <h1 class="page-title text-center">Company Profile</h1>
       <AppSpinner v-if="loading" />
       <div v-else class="card">
            <form @submit.prevent="saveProfile">
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="company_name">Company Name</label>
                        <input id="company_name" v-model="profile.company_name" class="form-input" readonly>
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="industry">Industry</label>
                        <input id="industry" v-model="form.industry" class="form-input">
                    </div>
                </div>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="status">Company Status</label>
                        <input id="status" v-model="profile.status" class="form-input" :class="statusClass(profile.status)" readonly>
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="created_at">Created At</label>
                        <input id="created_at" v-model="profile.created_at" class="form-input" readonly>
                    </div>
                </div>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="website">Website URL</label>
                        <input id="website" v-model="form.website" class="form-input">
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="location">Location</label>
                        <input id="location" v-model="form.location" class="form-input">
                    </div>
                </div>
                <div class="form-group">
                    <label class="form-label" for="description">Description</label>
                    <textarea id = "description" v-model="form.description" class="form-textarea"></textarea>
                </div>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="hr_name">HR Name</label>
                        <input id="hr_name" v-model="form.hr_name" class="form-input">
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="hr_phone">HR Phone</label>
                        <input id="hr_phone" v-model="form.hr_phone" class="form-input">
                    </div>
                </div>
                <div class="form-group">
                    <label class="form-label" for="hr_email">HR Email</label>
                    <input id="hr_email" v-model="form.hr_email" class="form-input">
                </div>
                <button type="submit" class="btn is-primary is-large full-width-btn" @click="saveProfile" :disabled="saving">{{ saving ? 'Saving...' : 'Save Changes' }}</button>
            </form>
       </div>
    </div>
</template>

<style scoped>
.card {
    max-width: 800px;
    margin: auto;
}
</style>

<script setup>
import AppSpinner from '@/components/ui/AppSpinner.vue';
import { formatDateTime } from '@/utils/formatters';
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { onMounted, reactive, ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const notify = useNotificationStore();
const router = useRouter();
const loading = ref(true);
const saving = ref(false);
const profile = ref({});

const form = reactive({
    industry: '',
    website: '',
    location: '',
    description: '',
    hr_name: '',
    hr_phone: '',
    hr_email: '',
})

onMounted(fetchProfile);

async function fetchProfile() {
    try {
        const result = await api.get('/company/profile');
        profile.value = result.data;
        profile.value.created_at = formatDateTime(profile.value.created_at)
        Object.assign(form, result.data);
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to load profile');
    } finally {
        loading.value = false;
    }
}

async function saveProfile() {
    saving.value = true;
    try {
        const result = await api.put('/company/profile', form);
        notify.success(result.data?.message || 'Profile updated successfully');
        if (result.data?.logout) {
            handleLogout();
        } else {
            fetchProfile();
        }    
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to update profile');
    } finally {
        saving.value = false;
        loading.value = true;
    }
}

function statusClass(status) {
    return {
        Pending: 'is-warning',
        Approved: 'is-success',
        Rejected: 'is-error',
        Closed: 'is-secondary'
    } [status] || 'is-info'
}

function handleLogout() {
    authStore.logout();
    notify.success("Logout successful");
    router.push({ name: 'home' });
}
</script>