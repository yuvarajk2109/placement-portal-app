<template>
    <div class="main-page">
        <h1 class="page-title">Student Dashboard</h1>
        <AppSpinner v-if="loading" />
        <div v-else>
            <div v-if="stats.is_placed" class="placed-card card mb-24">
                <p class="mb-16">Congratulations! You have been placed! Go get all the staff some chocolates (we don't recommend sweets as we have to eat them immediately. Chocolates, though, we can savour and relish and enjoy later!)</p>
                <router-link class="btn is-primary">View Placement <i class="fas fa-arrow-right"></i></router-link>
            </div>
            <p class="page-subtitle">Welcome, {{ stats.student_name }}</p>
            <!-- <p class="page-subtitle mb-4">Year {{ stats.year_of_study }}</p>
            <p class="page-subtitle">CGPA: {{ stats.cgpa }}</p> -->
            <div class="stats-grid">
                <div class="stat-card info">
                    <div class="stat-card-value info">
                        {{ stats.year_of_study }}
                    </div>
                    <div class="stat-card-label info">
                        Year of Study
                    </div>
                </div>
                <div class="stat-card info">
                    <div class="stat-card-value info">
                        {{ stats.cgpa }}
                    </div>
                    <div class="stat-card-label info">
                        CGPA
                    </div>
                </div>
                <div class="stat-card success">
                    <div class="stat-card-value success">
                        {{ stats.eligible_drives_count }}
                    </div>
                    <div class="stat-card-label success">
                        Eligible Drives
                    </div>
                </div>
                <div class="stat-card" :class="stats.total_applications > 0 ? 'info' : 'warning'">
                    <div class="stat-card-value" :class="stats.total_applications > 0 ? 'info' : 'warning'">
                        {{ stats.total_applications }}
                    </div>
                    <div class="stat-card-label" :class="stats.total_applications > 0 ? 'info' : 'warning'">
                        Total Applications
                    </div>
                </div>
                <div v-for="(count, status) in stats.application_status_counts" :key="status" class="stat-card" :class="applicationStatusClass(status)">
                    <div class="stat-card-value" :class="applicationStatusClass(status)">
                        {{ count }}
                    </div>
                    <div class="stat-card-label" :class="applicationStatusClass(status)">
                        {{ status}}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.placed-card {
    border-color: var(--status-success-container-line);
    background: var(--status-success-container-bg);
    color: var(--status-success-container-fg);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
}
</style>

<script setup>
import AppSpinner from '@/components/ui/AppSpinner.vue';
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { onMounted, ref } from 'vue';

const notify = useNotificationStore();
const loading = ref(true);
const stats = ref({});

onMounted(getDashboard);

async function getDashboard() {
    try {
        const result = await api.get('/student/dashboard');
        stats.value = result.data;
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to load dashboard');
    } finally {
        loading.value = false
    }
}

function applicationStatusClass(status) {
    return {
        Applied: 'info', 
        Shortlisted: 'warning', 
        Interview: 'warning',
        Selected: 'success',
        Rejected: 'error'
    } [status]
}
</script>