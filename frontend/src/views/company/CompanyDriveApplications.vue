<template>
    <div class="main-page">
        <div class="flex items-center justify-between mb-16">
            <h1 class="page-title mb-4">Drive Applications</h1>
            <router-link 
                :to="{ name: 'company-drive-detail', params: { id: driveId } }"
                class="btn is-secondary">
                Go Back
            </router-link>
        </div>
        <div class="card">
            <AppSpinner v-if="loading" />
            <table v-else-if="applications.length > 0" class="data-table">
                <thead>
                    <tr>
                        <th>Student</th>
                        <th>Register No.</th>
                        <th>CGPA</th>
                        <th>Applied Date</th>
                        <th>Status</th>
                        <th>Feedback</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="application in applications" :key="application.application_id">
                        <td>{{ application.student_name }}</td>
                        <td>{{ application.register_no }}</td>
                        <td>{{ application.cgpa }}</td>
                        <td>{{ formatDateTime(application.applied_date) }}</td>
                        <td><span class="status" :class="statusClass(application.application_status)">{{ application.application_status }}</span></td>
                        <td>{{ application.feedback }}</td>
                        <td class="actions-cell">
                            <select class="form-select" @change="updateStatus(application.application_id, $event.target?.value); $event.target.value = ''">
                                <option value="">Update...</option>
                                <option value="Shortlisted">Shortlist</option>
                                <option value="Selected">Select</option>
                                <option value="Rejected">Reject</option>
                            </select>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div v-else class="empty-state">
                <p class="empty-state-text">No applications for this drive yet.</p>
            </div>
            <AppPagination 
                v-model:currentPage="page" 
                :totalPages="totalPages" 
                @page-change="fetchApplications" 
            />
        </div>
    </div>
</template>

<script setup>
import AppPagination from '@/components/ui/AppPagination.vue';
import AppSpinner from '@/components/ui/AppSpinner.vue';
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { formatDate, formatDateTime } from '@/utils/formatters';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const notify = useNotificationStore();
const driveId = route.params.id;
const loading = ref(true);
const applications = ref([]);
const page = ref(1);
const totalPages = ref(1);

onMounted(fetchApplications);

async function fetchApplications() {
    loading.value = true;
    try {
        const params = { page: page.value, per_page: 10 };
        const result = await api.get(`/company/drives/${driveId}/applications`, { params });
        applications.value = result.data.applications;
        totalPages.value = result.data.pages;
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to load applications');
    } finally {
        loading.value = false;
    }
}

async function updateStatus(application_id, newStatus) {
    if (!newStatus) return;
    try {
        await api.get(`/company/applications/${application_id}/status`, { application_status: newStatus});
        notify.success(`Application status updated to ${newStatus}`);
        fetchApplications();
    } catch (err) {
        notify.error(err.response?.data?.error || `Failed to update status to ${newStatus}`);
    }
}

function statusClass(status) {
    return {
        Applied: 'is-info',
        Shortlisted: 'is-warning',
        Interview: 'is-warning',
        Selected: 'is-success',
        Rejected: 'is-error',
        Withdrawn: 'is-neutral'
    } [status] || 'is-neutral';
}
</script>