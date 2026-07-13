<template>
    <div class="main-page">
        <h1 class="page-title">Available Drives</h1>
        <div class="flex items-center justify-between mb-8">
            <div class="page-toolbar">
                <input class="form-input search-input" placeholder="Search by job title..." v-model="filters.search" @input="debouncedFetch">
                <input class="form-input search-input small" placeholder="Location..." v-model="filters.location" @input="debouncedFetch">
                <input v-model="filters.min_salary" type="number" class="form-input search-input small" placeholder="Min Salary (LPA)" @input="debouncedFetch" />
                <select class="form-select" v-model="filters.drive_type" @change="page = 1; fetchDrives()">
                    <option value="">All Types</option>
                    <option v-for="type in driveTypes" :key="type" :value="type">{{ type }}</option>
                </select>
                <select class="form-select" v-model="filters.application_status" @change="page = 1; fetchDrives()">
                    <option value="">All Statuses</option>
                    <option v-for="status in applicationStatuses" :key="status" :value="status">{{ status }}</option>
                </select>
            </div> 
            <button type="button" class="btn is-secondary mb-16" @click="resetFilters">Reset Filters</button>
        </div>
        
        <AppSpinner v-if="loading" />      
        <table v-else-if="drives.length > 0" class="data-table">
            <thead>
                <tr>
                    <th>Job Title</th>
                    <th>Type</th>
                    <th>CGPA Requirement</th>
                    <th>Location</th>
                    <th>Deadline</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr 
                    v-for="drive in drives" 
                    :key="drive.drive_id" 
                    class="clickable-row"
                    @click="$router.push({ name: 'student-drive-detail', params: { id: drive.drive_id } })"
                    > 
                    <td>{{ drive.job_title }}</td>
                    <td><span class="status is-info">{{ drive.drive_type }}</span></td>
                    <td>{{ drive.cgpa_requirement }}</td>
                    <td>{{ drive.location }}</td>
                    <td>{{ drive.application_deadline ? formatDateTime(drive.application_deadline) : '' }}</td>
                    <td><span class="status" :class="applicationStatusClass(drive.application_status)">{{ drive.application_status }}</span></td>
                </tr>
            </tbody>
        </table>                    
        <div v-else class="card">
            <div class="empty-state">
                <p class="empty-state-text">No drives found. Reset your filters and try again.</p>
            </div>
        </div>
        <AppPagination 
            v-model:currentPage="page" 
            :totalPages="totalPages" 
            @page-change="fetchDrives" 
        />  
    </div>
</template>

<script setup>
import AppSpinner from '@/components/ui/AppSpinner.vue';
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { formatDateTime } from '@/utils/formatters';
import { onMounted, reactive, ref } from 'vue';
import { applicationStatusClass } from '@/utils/status';

const notify = useNotificationStore();
const loading = ref(true);
const drives = ref([]);
const driveTypes = ref([]);
const applicationStatuses = ref([]);
const page = ref(1);
const totalPages = ref(1);
const filters = reactive({
    search: '',
    location: '',
    drive_type: '',
    min_salary: '',
    application_status: ''
})
const emptyFilters = {
    search: '',
    location: '',
    drive_type: '',
    min_salary: '',
    application_status: ''
}

let debounceTimer = null;
function debouncedFetch() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => { page.value = 1; fetchDrives() }, 300)
}

onMounted(fetchDrives);

async function fetchDrives() {
    loading.value = true;
    try {
        const params = { page: page.value, per_page: 20 };
        if (filters.search) params.search = filters.search;
        if (filters.location) params.location = filters.location;
        if (filters.drive_type) params.drive_type = filters.drive_type;
        if (filters.min_salary) params.min_salary = filters.min_salary;
        if (filters.application_status) params.application_status = filters.application_status;
        const [driveResult, driveTypeResult, applicationStatusResult] = await Promise.all([
            api.get('/student/drives', { params }),
            api.get('/shared/drive-types'),
            api.get('/shared/application-statuses')
        ]);
        drives.value = driveResult.data.drives;
        totalPages.value = driveResult.data.pages;
        driveTypes.value = driveTypeResult.data.drive_types;
        applicationStatuses.value = applicationStatusResult.data.application_statuses;
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to load drives');
    } finally {
        loading.value = false;
    }
}

function resetFilters() {
    Object.assign(filters, emptyFilters);
    fetchDrives();
}
</script>