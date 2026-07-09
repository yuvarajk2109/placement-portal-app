<template>
    <div class="main-page">
        <h1 class="page-title">All Applications</h1>
        <AppSpinner v-if="loading" />
        <table v-else-if="applications.length > 0" class="data-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Student</th>
                    <th>Register Number</th>
                    <th>Company</th>
                    <th>Job Title</th>
                    <th>Status</th>
                    <th>Applied Date</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="application in applications" :key="application.application_id">
                    <td>{{ application.application_id }}</td>
                    <td>{{ application.student_name }}</td>
                    <td>{{ application.register_no }}</td>
                    <td>{{ application.company_name }}</td>
                    <td>{{ application.job_title }}</td>
                    <td><span class="status" :class="statusMessage(application.status)">{{ application.status }}</span></td>
                    <td>{{ new Date(application.applied_date).toLocaleDateString() }}</td>
                </tr>
            </tbody>
        </table>
        <div v-else class="card">
            <div class="empty-state">
                <p class="empty-state-text">No applications found.</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import AppSpinner from '@/components/ui/AppSpinner.vue';
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { onMounted, ref } from 'vue';

const notify = useNotificationStore();
const loading = ref(true);
const applications = ref([]);
const page = ref(1);
const totalPages = ref(1);

onMounted(fetchData);

async function fetchData() {
    loading.value = true;
    try {
        const params = {
            page: page.value,
            per_page: 20
        };
        const result = await api.get('/admin/applications', { params });
        applications.value = result.data.applications;
        totalPages.value = result.data.pages;
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to load applications');
    } finally {
        loading.value = false;
    }
}

function statusMessage(status) {
    return {
        Applied: 'is-info',
        Shortlisted: 'is-info',
        Interview: 'is-info',
        Selected: 'is-success',
        Rejected: 'is-error',
        Withdrawn: 'is-secondary'
    } [status] ||'is-secondary'
};
</script>