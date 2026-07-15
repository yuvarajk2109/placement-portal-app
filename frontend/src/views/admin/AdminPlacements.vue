<template>
    <div class="main-page">
        <h1 class="page-title">All Placements</h1>
        <div class="flex items-center justify-between mb-8">
            <div class="page-toolbar">
                <select class="form-select" v-model="driveTypeFilter" @change="page = 1; fetchData();">
                    <option value="">All Drive Types</option>
                    <option v-for="type in driveTypes" :key="type" :value="type">{{ type }}</option>
                </select>                
            </div>
            <AppTooltip text="Reset Filters">
                <button class="btn is-icon-only is-secondary" @click="resetCurrentFilters">
                    <i class="fas fa-undo"></i>
                </button>
            </AppTooltip>
        </div>
        <AppSpinner v-if="loading" />
        <table v-else-if="placements.length > 0" class="data-table">
            <thead>
                <tr>
                    <th>Student</th>
                    <th>Register Number</th>
                    <th>Company</th>
                    <th>Position</th>
                    <th>Type</th>
                    <th>Salary (LPA)</th>
                    <th>Date of Placement</th>
                </tr>
            </thead>
            
            <tbody>
                <tr v-for="placement in placements" :key="placement.placement_id" class="clickable-row" @click="viewDetails(placement)">
                    <td>{{ placement.student_name }}</td>
                    <td>{{ placement.register_no }}</td>
                    <td>{{ placement.company_name }}</td>
                    <td>{{ placement.position }}</td>
                    <td><span class="status is-info">{{ placement.drive_type }}</span></td>
                    <td>{{ formatSalary(placement.salary) }}</td>
                    <td>{{ formatDate(placement.created_at) }}</td>
                </tr>
            </tbody>
        </table>
        <div v-else class="card">
            <div class="empty-state">
                <p class="empty-state-text">No placements yet. Don't worry, trust the students!</p>
            </div>
        </div>
        <AppPagination
            v-model:currentPage="page"
            :totalPages="totalPages"
            @page-change="fetchData"
        />
    </div>
    <AppModal v-model="showDetail">
        <template #title>Placement Details</template>
        <div v-if="selectedPlacement" class="flex flex-col gap-12">
            <!-- Student Details -->
            <h3 class="section-heading">Student Information</h3>
            <div class="flex justify-between">
                <span>Name</span>
                <span>{{ selectedPlacement.student_name }}</span>
            </div>
            <div class="flex justify-between">
                <span>Register Number</span>
                <span>{{ selectedPlacement.register_no }}</span>
            </div>
            <div class="flex justify-between">
                <span>Student Email</span>
                <span>{{ selectedPlacement.student_email }}</span>
            </div>
            <div class="flex justify-between">
                <span>Phone</span>
                <span>{{ selectedPlacement.student_phone || '—' }}</span>
            </div>
            <div class="flex justify-between">
                <span>Branch</span>
                <span>{{ selectedPlacement.student_branch }}</span>
            </div>
            <div class="flex justify-between">
                <span>CGPA</span>
                <span>{{ selectedPlacement.student_cgpa }}</span>
            </div>

            <!-- Placement Details -->
            <h3 class="section-heading mt-16">Placement Details</h3>
            <div class="flex justify-between">
                <span>Company Name</span>
                <span>{{ selectedPlacement.company_name }}</span>
            </div>
            <div class="flex justify-between">
                <span>Industry</span>
                <span>{{ selectedPlacement.company_industry }}</span>
            </div>
            <div class="flex justify-between">
                <span>Job Title</span>
                <span>{{ selectedPlacement.job_title }}</span>
            </div>
            <div class="flex justify-between">
                <span>Position</span>
                <span>{{ selectedPlacement.position }}</span>
            </div>
            <div class="flex justify-between">
                <span>Location</span>
                <span>{{ selectedPlacement.drive_location || '—' }}</span>
            </div>
            <div class="flex justify-between">
                <span>Drive Type</span>
                <span>{{ selectedPlacement.drive_type }}</span>
            </div>
            <div class="flex justify-between">
                <span>Salary (LPA)</span>
                <span>{{ selectedPlacement.salary ? formatSalary(selectedPlacement.salary) : '—' }}</span>
            </div>
            <div class="flex justify-between">
                <span>Placement Date</span>
                <span>{{ formatDate(selectedPlacement.created_at) }}</span>
            </div>
        </div>
        <template #footer>
            <button class="btn is-secondary" @click="showDetail = false">Close</button>
        </template>
    </AppModal>
</template>

<script setup>
import AppModal from '@/components/ui/AppModal.vue';
import AppPagination from '@/components/ui/AppPagination.vue';
import AppSpinner from '@/components/ui/AppSpinner.vue';
import AppTooltip from '@/components/ui/AppTooltip.vue';
import { formatDate, formatSalary } from '@/utils/formatters';
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { onMounted, ref } from 'vue';

const notify = useNotificationStore();
const loading = ref(true);
const placements = ref([]);
const driveTypes = ref([]);
const driveTypeFilter = ref('');
const page = ref(1);
const totalPages = ref(1);
const showDetail = ref(false);
const selectedPlacement = ref(null);


function resetCurrentFilters() {
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
        notify.error(err.response?.data?.error || 'Failed to load drive types');
    }
}

async function fetchData() {
    loading.value = true;
    try {
        const params = { page: page.value };
        if (driveTypeFilter.value) params.drive_type = driveTypeFilter.value;
        const result = await api.get('/admin/placements', { params });
        placements.value = result.data.placements || [];
        totalPages.value = result.data.pages;
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to load placements');
    } finally {
        loading.value = false;
    }
}

function viewDetails(placement) {
    selectedPlacement.value = placement;
    showDetail.value = true;
}
</script>