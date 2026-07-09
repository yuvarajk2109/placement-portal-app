<template>
    <div class="main-page">
        <h1 class="page-title">Manage Drives</h1>
        <div class="page-toolbar">
            <div class="filter-group">
                <select class="form-select" v-model="statusFilter" @change="page = 1; fetchData();">
                    <option value="">All Statuses</option>
                    <option value="Pending">Pending</option>
                    <option value="Approved">Approved</option>
                    <option value="Rejected">Rejected</option>
                </select>
            </div>
        </div>
        <AppSpinner v-if="loading" />
        <table v-else-if="drives.length > 0" class="data-table">
            <thead>
                <tr>
                    <th>Job Title</th>
                    <th>Company</th>
                    <th>Type</th>
                    <th>Applications</th>
                    <th>Status</th>
                    <th>Created at</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="drive in drives" :key="drive.drive_id">
                    <td>{{ drive.job_title }}</td>
                    <td>{{ drive.company_name }}</td>
                    <td><span class="status is-info">{{ drive.drive_type }}</span></td>
                    <td>{{ drive.applications_count }}</td>
                    <td><span class="status" :class="statusMessage(drive.status)">{{ drive.status }}</span></td>
                    <td>{{ new Date(drive.created_at).toLocaleDateString() }}</td>
                    <td class="actions-cell">
                        <button v-if="drive.status === 'Pending'" class="btn is-primary" @click="updateStatus(drive.drive_id, 'approve')">Approve</button>
                        <button v-if="drive.status === 'Pending'" class="btn is-warning" @click="updateStatus(drive.drive_id, 'reject')">Reject</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <div v-else class="empty-state">
            <p class="empty-state-text">No drives found.</p>
        </div>
        <AppPagination 
            v-model:currentPage="page" 
            :totalPages="totalPages" 
            @page-change="fetchData" 
        />
    </div>
</template>

<script setup>
import AppSpinner from '@/components/ui/AppSpinner.vue';
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { onMounted, ref } from 'vue';

const notify = useNotificationStore();
const loading = ref(true);
const drives = ref([]);
const statusFilter = ref('');
const page = ref(1);
const totalPages = ref(1);

onMounted(fetchData);

async function fetchData() {
    loading.value = true;
    try {
        const params = { page: page.value, per_page: 20 };
        if (statusFilter.value) params.status = statusFilter.value;
        const result = await api.get('/admin/drives', { params });
        drives.value = result.data.drives;
        totalPages.value = result.data.pages;
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to load drives');
    } finally {
        loading.value = false;
    }
}

async function updateStatus(id, action) {
    try {
        await api.put(`/admin/drives/${id}/${action}`);
        notify.success(`Drive ${action} is successful`);
        fetchData();
    } catch (err) {
        notify.error(err.response?.data?.error || `Failed to ${action} drive`);
    }
}

function statusMessage(status) {
    return {
        Pending: 'is-warning',
        Approved: 'is-success',
        Rejected: 'is-error',
        Closed: 'is-secondary'
    } [status] || 'is-info';
}
</script>