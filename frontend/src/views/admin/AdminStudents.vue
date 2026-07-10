<template>
    <div class="main-page">
        <h1 class="page-title">Manage Students</h1>
        <div v-if="students.length > 0" class="page-toolbar">
            <input v-model="search" class="form-input search-input" placeholder="Search by name or register no..." @input="debouncedFetch">
            <div class="filter-group">
                <select v-model="statusFilter" class="form-select" @change="page = 1; fetchData();">
                    <option value="">All Statuses</option>
                    <option value="Active">Active</option>
                    <option value="Inactive">Inactive</option>
                    <option value="Blacklisted">Blacklisted</option>
                    <option value="Unblacklisted">Unblacklisted</option>
                </select>
            </div>
        </div>
        <AppSpinner v-if="loading"/>
        <table v-else-if="students.length > 0" class="data-table">
            <thead>
                <tr>
                    <th>Register Number</th>
                    <th>Name</th>
                    <th>Branch</th>
                    <th>Year</th>
                    <th>CGPA</th>
                    <th>Active</th>
                    <th>Blacklisted</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="student in students" :key="student.register_no">
                    <td>{{ student.register_no }}</td>
                    <td>{{ student.name }}</td>
                    <td>{{ student.branch }}</td>
                    <td>{{ student.year_of_study }}</td>
                    <td>{{ student.cgpa }}</td>
                    <td><span class="status" :class="student.is_active ? 'is-success' : 'is-error'">{{ student.is_active ? 'Yes' : 'No' }}</span></td>
                    <td><span class="status" :class="student.is_blacklisted ? 'is-error' : 'is-success'">{{ student.is_blacklisted ? 'Yes' : 'No' }}</span></td>
                    <td class="actions-cell">
                        <button v-if="!student.is_blacklisted" class="btn is-warning" @click="toggleBlacklist(student.register_no, 'blacklist')">Blacklist</button>
                        <button v-if="student.is_blacklisted" class="btn is-secondary" @click="toggleBlacklist(student.register_no, 'unblacklist')">Unblacklist</button>
                        <button v-if="!student.is_active" class="btn is-primary" @click="toggleActive(student.register_no, 'activate')">Activate</button>
                        <button v-if="student.is_active" class="btn is-warning" @click="toggleActive(student.register_no, 'deactivate')">Deactivate</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
import AppSpinner from '@/components/ui/AppSpinner.vue';
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { onMounted, ref } from 'vue';

const notify = useNotificationStore();
const loading = ref(true);
const students = ref([]);
const search = ref('');
const statusFilter = ref('Active');
const page = ref(1);
const totalPages = ref(1);

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
        const result = await api.get('/admin/students', { params });
        students.value = result.data.students;
        totalPages.value = result.data.pages;
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to load students');
    } finally {
        loading.value = false;
    }
}

async function toggleBlacklist(regNo, action) {
    try {
        await api.put(`/admin/students/${regNo}/${action}`);
        notify.success(`Student ${action}ed successfully`);
        fetchData();
    } catch (err) {
        notify.error(err.response?.data?.error || `Failed to ${action} student`);
    }
}

async function toggleActive(regNo, action) {
    try {
        await api.put(`/admin/students/${regNo}/${action}`);
        notify.success(`Student ${action}d successfully`);
        fetchData();
    } catch (err) {
        notify.error(err.response?.data?.error || `Failed to ${action} student`);
    }
}
</script>