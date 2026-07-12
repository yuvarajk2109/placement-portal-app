<template>
    <h1 class="page-title">Placement Details</h1>
    <AppSpinner v-if="loading" />
    <template v-else>
        <div class="stats-grid mb-24">
            <div class="stat-card">
                <div class="stat-card-value">{{ placement.position }}</div>
                <div class="stat-card-label">Position</div>
            </div>
            <div class="stat-card">
                <div class="stat-card-value">{{ placement.company_name }}</div>
                <div class="stat-card-label">Company</div>
            </div>
            <div class="stat-card">
                <div class="stat-card-value">{{ placement.salary }} LPA</div>
                <div class="stat-card-label">Annual Salary</div>
            </div>
            <div class="stat-card">
                <div class="stat-card-value">{{ formatDate(placement.created_at) }}</div>
                <div class="stat-card-label">Placed On</div>
            </div>
        </div>
        <div class="stats-grid">
            <div class="stat-card span-3">
                <div class="stat-card-value">{{ placement.drive_type }}</div>
                <div class="stat-card-label">Type</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-card-value">{{ placement.joining_date || 'TBA' }}</div>
                <div class="stat-card-label">Joining Date</div>
            </div>
        </div>
    </template>
</template>

<style scoped>
.stats-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 24px;
}

.span-3 {
    grid-column: span 3;
}
</style>

<script setup>
import AppSpinner from '@/components/ui/AppSpinner.vue';
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { formatDate } from '@/utils/formatters';
import { onMounted, ref } from 'vue';


const notify = useNotificationStore();
const loading = ref(true);
const placement = ref(null);

onMounted(fetchPlacement);

async function fetchPlacement() {
    loading.value = true;
    try {
        const result = await api.get('/student/placement');
        placement.value = result.data.placement;
    } catch (err) {
        if (err.response?.status !== 404) notify.error(err.response?.data?.error || 'Failed to load placement');
    } finally {
        loading.value = false;
    }
}
</script>