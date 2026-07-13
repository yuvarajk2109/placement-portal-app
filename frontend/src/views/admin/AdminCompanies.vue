<template>
    <div class="main-page">
        <h1 class="page-title">Manage Companies</h1>
        <div v-if="companies.length > 0" class="page-toolbar">
            <input class="form-input search-input" placeholder="Search companies..." @input="debouncedFetch">
            <select v-model="statusFilter" class="form-select" @change="page = 1; fetchData();">
                <option value="">All Statuses</option>
                <option value="Pending">Pending</option>
                <option value="Approved">Approved</option>
                <option value="Rejected">Rejected</option>
            </select>
        </div>
        <AppSpinner v-if="loading" />
        <table v-else-if="companies.length" class="data-table">
            <thead>
                <tr>
                    <th>Company Name</th>
                    <th>Industry</th>
                    <th>Location</th>
                    <th>HR Email</th>
                    <th>Status</th>
                    <th>Blacklisted</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="company in companies" :key="company.company_id">
                    <td>{{ company.company_name }}</td>
                    <td>{{ company.industry || '-' }}</td>
                    <td>{{ company.location || '-'}}</td>
                    <td>{{ company.hr_email }}</td>
                    <td><span class="status" :class="companyStatusClass(company.status)">{{ company.status }}</span></td>
                    <td><span class="status" :class="company.is_blacklisted ? 'is-error': 'is-neutral'">{{ company.is_blacklisted? 'Yes' : 'No' }}</span></td>
                    <td class="actions-cell">
                        <button v-if="company.status === 'Pending'" class="btn is-primary" @click="updateStatus(company.company_id, 'approve')">Approve</button>
                        <button v-if="company.status === 'Pending'" class="btn is-warning" @click="updateStatus(company.company_id, 'reject')">Reject</button>
                        <button v-if="company.status === 'Approved' && !company.is_blacklisted" class="btn is-warning" @click="toggleBlacklist(company.company_id, 'blacklist')">Blacklist</button>
                        <button v-if="company.status === 'Approved' && company.is_blacklisted" class="btn is-secondary" @click="toggleBlacklist(company.company_id, 'unblacklist')">Unblacklist</button>
                        <button v-if="company.status === 'Rejected'" class="btn is-warning" @click="removeCompany(company.company_id)">Remove</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <div v-else class="card">
            <div class="empty-state">
                <p class="empty-state-text">No companies found.</p>
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
import AppPagination from '@/components/ui/AppPagination.vue';
import AppSpinner from '@/components/ui/AppSpinner.vue';
import api from '@/services/api';
import { useDialogStore } from '@/stores/dialog';
import { useNotificationStore } from '@/stores/notification';
import { companyStatusClass } from '@/utils/status';
import { onMounted, ref } from 'vue';

const notify = useNotificationStore();
const loading = ref(true);
const companies = ref([]);
const search = ref('');
const statusFilter = ref('');
const page = ref(1);
const totalPages = ref(1);
const dialog = useDialogStore();

let debounceTimer = null;
function debouncedFetch() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        page.value = 1; 
        fetchData();
    }, 300);
}

onMounted(fetchData);

async function fetchData() {
    loading.value = true;
    try {
        const params = {
            page: page.value,
            per_page: 20
        };
        if (search.value) params.search = search.value;
        if (statusFilter.value) params.status = statusFilter.value;
        const result = await api.get('/admin/companies', { params });
        companies.value = result.data.companies;
        totalPages.value = result.data.pages;
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to load companies');
    } finally {
        loading.value = false;
    }
}

async function updateStatus(id, action) {
    try {
        const result = await api.put(`/admin/companies/${id}/${action}`);
        notify.success(result.data?.message || `Company ${action} is successful`);
        fetchData();
    } catch (err) {
        notify.error(err.response?.data?.error || `Failed to update status to ${action}`);
    }
}

async function toggleBlacklist(id, action) {
    try {
        const result = await api.put(`/admin/companies/${id}/${action}`);
        notify.success(result.data?.message || `Company ${action}ed successfully`);
        fetchData();
    } catch (err) {
        notify.error(err.response?.data?.error || `Failed to ${action} company`);
    }
}

async function removeCompany(id) {
    const confirmed = await dialog.confirm({
        title: 'Remove Company',
        message: 'Are you sure you want to permanently remove this company? This action can\'t be undone.',
        type: 'error',
        confirmText: 'Remove'
    });
    if (!confirmed) return;

    try {
        await api.delete(`/admin/companies/${id}`);
        notify.success('Company removed');
        fetchData();
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to remove company');
    }
}
</script>