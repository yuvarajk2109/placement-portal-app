<template>
    <div class="main-page">
        <h1 class="page-title">All Placements</h1>
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
                    <td>{{ placement.salary }}</td>
                    <td>{{ new Date(placement.created_at).toLocaleDateString() }}</td>
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
            <h3 class="text-subtitle">Student Information</h3>
            <div class="flex justify-between">
                <span class="text-subtle">Name</span>
                <span class="font-medium">{{ selectedPlacement.student_name }}</span>
            </div>
            <div class="flex justify-between">
                <span class="text-subtle">Register Number</span>
                <span>{{ selectedPlacement.register_no }}</span>
            </div>
            <div class="flex justify-between">
                <span class="text-subtle">Email</span>
                <span>{{ selectedPlacement.student_email }}</span>
            </div>
            <div class="flex justify-between">
                <span class="text-subtle">Phone</span>
                <span>{{ selectedPlacement.student_phone || '—' }}</span>
            </div>
            <div class="flex justify-between">
                <span class="text-subtle">Branch</span>
                <span>{{ selectedPlacement.student_branch }}</span>
            </div>
            <div class="flex justify-between">
                <span class="text-subtle">CGPA</span>
                <span class="font-medium">{{ selectedPlacement.student_cgpa }}</span>
            </div>

            <!-- Placement Details -->
            <h3 class="text-subtitle mt-16">Placement Details</h3>
            <div class="flex justify-between">
                <span class="text-subtle">Company Name</span>
                <span class="font-medium">{{ selectedPlacement.company_name }}</span>
            </div>
            <div class="flex justify-between">
                <span class="text-subtle">Industry</span>
                <span>{{ selectedPlacement.company_industry }}</span>
            </div>
            <div class="flex justify-between">
                <span class="text-subtle">Job Title</span>
                <span>{{ selectedPlacement.job_title }}</span>
            </div>
            <div class="flex justify-between">
                <span class="text-subtle">Position</span>
                <span class="font-medium">{{ selectedPlacement.position }}</span>
            </div>
            <div class="flex justify-between">
                <span class="text-subtle">Location</span>
                <span>{{ selectedPlacement.drive_location || '—' }}</span>
            </div>
            <div class="flex justify-between">
                <span class="text-subtle">Drive Type</span>
                <span class="badge is-info">{{ selectedPlacement.drive_type }}</span>
            </div>
            <div class="flex justify-between">
                <span class="text-subtle">Salary (LPA)</span>
                <span class="font-medium text-success">{{ selectedPlacement.salary || '—' }}</span>
            </div>
            <div class="flex justify-between">
                <span class="text-subtle">Placement Date</span>
                <span>{{ new Date(selectedPlacement.created_at).toLocaleDateString() }}</span>
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
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { onMounted, ref } from 'vue';

const notify = useNotificationStore();
const loading = ref(true);
const placements = ref([]);
const page = ref(1);
const totalPages = ref(1);
const showDetail = ref(false);
const selectedPlacement = ref(null);

onMounted(fetchData);

async function fetchData() {
    loading.value = true;
    try {
        const params = {
            page: page.value,
            per_page: 20
        };
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