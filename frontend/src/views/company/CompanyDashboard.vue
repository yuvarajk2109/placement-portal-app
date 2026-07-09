<template>
    <div class="main-page">
        <h1 class="page-title">Company Dashboard</h1>
        <AppSpinner v-if="loading" />
        <div v-else class="stats-grid mt-32">
            <div class="stat-card info">
                <div class="stat-card-value info">
                    {{  stats.total_drives  }}
                </div>
                <div class="stat-card-label info">
                    Total Drives
                </div>
            </div>
            <div class="stat-card info">
                <div class="stat-card-value info">
                    {{ stats.active_drives }}
                </div>
                <div class="stat-card-label info">
                    Active Drives
                </div>
            </div>
            <div class="stat-card warning">
                <div class="stat-card-value warning">
                    {{ stats.pending_drives }}
                </div>
                <div class="stat-card-label warning">   
                    Drives Pending Approval
                </div>
            </div>
            <div class="stat-card info">
                <div class="stat-card-value info">
                    {{ stats.total_applications }}
                </div>
                <div class="stat-card-label info">
                    Total No. of Applications
                </div>
            </div>
            <div class="stat-card warning">
                <div class="stat-card-value warning">
                    {{ stats.total_selected }}
                </div>
                <div class="stat-card-label warning">
                    Candidates Selected
                </div>
            </div>
        </div>
    </div>
</template> 

<style scoped>
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
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
        const result = await api.get('/company/dashboard');
        stats.value = result.data;
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to load dashboard');
    } finally {
        loading.value = false;
    }
})
</script>