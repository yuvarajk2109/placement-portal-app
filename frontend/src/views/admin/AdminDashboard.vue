<template>
    <div class="main-page">
        <div class="page-title">Welcome, Admin</div>

        <AppSpinner v-if="loading" />
        <div v-else class="stats-grid mt-32">
            <div class="stat-card info">
                <div class="stat-card-value info">
                    {{  stats.total_students  }}
                </div>
                <div class="stat-card-label info">
                    Total Students
                </div>
            </div>
            <div class="stat-card info">
                <div class="stat-card-value info">
                    {{ stats.total_companies }}
                </div>
                <div class="stat-card-label info">
                    Total Companies
                </div>
            </div>
            <div class="stat-card warning">
                <div class="stat-card-value warning">
                    {{ stats.pending_companies }}
                </div>
                <div class="stat-card-label warning">   
                    Pending Companies
                </div>
            </div>
            <div class="stat-card info">
                <div class="stat-card-value info">
                    {{ stats.total_drives }}
                </div>
                <div class="stat-card-label info">
                    Total Drives
                </div>
            </div>
            <div class="stat-card warning">
                <div class="stat-card-value warning">
                    {{ stats.pending_drives }}
                </div>
                <div class="stat-card-label warning">
                    Pending Drives
                </div>
            </div>
            <div class="stat-card info">
                <div class="stat-card-value info">
                    {{ stats.total_applications }}
                </div>
                <div class="stat-card-label info">
                    Total Applications
                </div>
            </div>
            <div class="stat-card success">
                <div class="stat-card-value success">
                    {{ stats.total_placements }}
                </div>
                <div class="stat-card-label success">
                    Total Placements
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.stats-grid {    
  display: grid;
  grid-template-columns: repeat(8, 1fr);
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

onMounted(async () => {
    try {
        const result = await api.get('/admin/dashboard');
        stats.value = result.data;
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to load dashboard');
    } finally {
        loading.value = false;
    }
})
</script>