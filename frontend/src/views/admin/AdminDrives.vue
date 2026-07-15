<template>
    <div class="main-page">
        <h1 class="page-title">Manage Drives</h1>
        <div class="flex items-center justify-between mb-8">
            <div class="page-toolbar">
                <select class="form-select" v-model="statusFilter" @change="page = 1; fetchData();">
                    <option value="">All Statuses</option>
                    <option value="Pending">Pending</option>
                    <option value="Approved">Approved</option>
                    <option value="Rejected">Rejected</option>
                    <option value="Closed">Closed</option>
                </select>
                <select class="form-select" v-model="driveTypeFilter" @change="page = 1; fetchData();">
                    <option value="">All Drive Types</option>
                    <option v-for="type in driveTypes" :key="type" :value="type">{{ type }}</option>
                </select>                
            </div>
            <AppTooltip text="Reset Filters">
                <button class="btn is-secondary is-icon-only" @click="resetCurrentFilters">
                    <i class="fas fa-undo"></i>
                </button>
            </AppTooltip>
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
                    <td><span class="status" :class="driveStatusClass(drive.status)">{{ drive.status }}</span></td>
                    <td>{{ formatDate(drive.created_at) }}</td>
                    <td class="actions-cell">
                        <button v-if="drive.status === 'Pending'" class="btn is-primary" @click="updateStatus(drive.drive_id, 'approve')">Approve</button>
                        <button v-if="drive.status === 'Pending'" class="btn is-warning" @click="updateStatus(drive.drive_id, 'reject')">Reject</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <div v-else class="card">
            <div class="empty-state">
                <p class="empty-state-text">No drives found.</p>
            </div>
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
import AppTooltip from '@/components/ui/AppTooltip.vue';
import AppPagination from '@/components/ui/AppPagination.vue';
import { formatDate } from '@/utils/formatters';
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { onMounted, ref } from 'vue';
import { driveStatusClass } from '@/utils/status';

const notify = useNotificationStore();
const loading = ref(true);
const drives = ref([]);
const driveTypes = ref([]);
const statusFilter = ref('');
const driveTypeFilter = ref('');
const page = ref(1);
const totalPages = ref(1);

function resetCurrentFilters() {
    statusFilter.value = '';
    driveTypeFilter.value = '';
    page.value = 1;
    fetchData();
}

onMounted(() => {
    fetchDriveTypes();
    fetchData();
});

async function fetchDriveTypes() {
    try {
        const result = await api.get('/shared/drive-types');
        driveTypes.value = result.data.drive_types;
    } catch (err) {
        notify.error('Failed to load drive types');
    }
}

async function fetchData() {
    loading.value = true;
    try {
        const params = { page: page.value };
        if (statusFilter.value) params.status = statusFilter.value;
        if (driveTypeFilter.value) params.drive_type = driveTypeFilter.value;
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
        const result = await api.put(`/admin/drives/${id}/${action}`);
        notify.success(result.data?.message || `Drive ${action} is successful`);
        fetchData();
    } catch (err) {
        notify.error(err.response?.data?.error || `Failed to ${action} drive`);
    }
}
</script>