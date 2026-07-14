<template>
<div class="main-page">
    <div class="flex justify-between mb-16">
        <h1 class="page-title">My Applications</h1>
        <div v-if="applications.length > 0">
            <button type="button" class="btn is-secondary" @click="exportApplications"><i class="fas fa-file-export"></i>Export Applications as CSV</button>
        </div>
    </div>
    
    <div class="card">
        <AppSpinner v-if="loading" />
        <table v-else-if="applications.length > 0" class="data-table">
            <thead>
                <tr>
                    <th>Job Title</th>
                    <th>Company</th>
                    <th>Status</th>
                    <th>Feedback</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr class="clickable-row" v-for="application in applications" :key="application.application_id" @click="viewApplicationDetail(application)">
                    <td>{{ application.job_title }}</td>
                    <td>{{ application.company_name }}</td>
                    <td><span class="status" :class="applicationStatusClass(application.status)">{{ application.status }}</span></td>
                    <td>{{ application.feedback || 'None' }}</td>
                    <td class="actions-cell" @click.stop>
                        <button 
                            type="button"
                            class="btn is-error"
                            v-if="['Applied', 'Shortlisted'].includes(application.status)"
                            @click="withdraw(application.application_id)">
                            Withdraw Application
                        </button>
                        <span v-else>None</span>
                    </td>
                </tr>
            </tbody>
        </table>
        <div v-else class="empty-state">
            <p class="empty-state-text">You haven't applied to any drives yet. Go to the drives tab to search and apply for eligible drives.</p>
        </div>
        <AppPagination 
            v-model:current-page="page",
            :total-pages="totalPages"
            @page-change="fetchApplications"
        />
    </div>
    <AppModal v-model="applicationDetailOpen" size="medium">
        <template #title>{{ selectedApplication.job_title }} &middot; {{ selectedApplication.company_name }}</template>
        <StudentApplicationDetail :application_id="selectedApplication.application_id"/>
        <template #footer>
            <button type="button" class="btn is-secondary" @click="closeModal">Close</button>
        </template>
    </AppModal>
</div>
</template>

<script setup>
import AppModal from '@/components/ui/AppModal.vue';
import AppPagination from '@/components/ui/AppPagination.vue';
import AppSpinner from '@/components/ui/AppSpinner.vue';
import api from '@/services/api';
import { useDialogStore } from '@/stores/dialog';
import { useNotificationStore } from '@/stores/notification';
import { onMounted, ref } from 'vue';
import StudentApplicationDetail from './StudentApplicationDetail.vue';
import { applicationStatusClass } from '@/utils/status.js';

const notify = useNotificationStore();
const dialog = useDialogStore();
const loading = ref(true);
const applications = ref([]);
const page = ref(1);
const totalPages = ref(1);
const selectedApplication = ref();
const applicationDetailOpen = ref(false);

onMounted(fetchApplications);

async function fetchApplications() {
    loading.value = true;
    try {
        const result = await api.get('/student/applications', { params: { page: page.value, per_page: 20} });
        applications.value = result.data.applications;
        totalPages.value = result.data.pages;
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to load applications');
    } finally {
        loading.value = false;
    }
}

async function withdraw(applicationId) {
    const confirmed = await dialog.confirm({
        title: 'Withdraw Application?',
        message: 'Are you sure you want to withdraw your application? This action can\'t be undone.',
        type: 'warning',
        confirmText: 'Withdraw'
    });
    if (!confirmed) return;
    try {
        const result = await api.put(`/student/applications/${applicationId}/withdraw`);
        notify.success(result.data?.message || 'Application successfully withdrawn.');
        fetchApplications();
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to withdraw applications');
    }
}

function viewApplicationDetail(application) {
    selectedApplication.value = application;
    applicationDetailOpen.value = true;
}

function closeModal() {
    applicationDetailOpen.value = false;
}

async function exportApplications() {
    loading.value = true;
    try {
        const result = await api.post('/student/export/applications');
        notify.success(result.data?.message);
    } catch (err) {
        notify.error(err.response?.data?.message || 'Failed to initiate export, please try again alter.');
    } finally {
        loading.value = false;
    }
}
</script>