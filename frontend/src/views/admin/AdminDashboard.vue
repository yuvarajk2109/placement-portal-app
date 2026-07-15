<template>
    <div class="main-page">
        <div class="page-title">Welcome, Admin</div>

        <AppSpinner v-if="loading" />
        <template v-else>
            <div class="custom-grid">
                <div class="title-card stat-card">
                    <div class="stat-card-value"><i class="fas fa-user"></i></div>
                    <div class="stat-card-label">Students</div>
                </div>             
                <div class="stats-grid">
                    <div class="stat-card is-info">
                        <div class="stat-card-value is-info">{{ stats.total_students }}</div>
                        <div class="stat-card-label is-info">Total Students</div>
                    </div>
                    <div class="stat-card is-success">
                        <div class="stat-card-value is-success">{{ stats.active_students }}</div>
                        <div class="stat-card-label is-success">Active Students</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-card-value">{{ stats.inactive_students }}</div>
                        <div class="stat-card-label">Inactive Students</div>
                    </div>   
                    <div class="stat-card is-error">
                        <div class="stat-card-value is-error">{{ stats.blacklisted_students }}</div>
                        <div class="stat-card-label is-error">Blacklisted Students</div>
                    </div>       
                </div>
            </div>
            
            <div class="custom-grid">
                <div class="title-card stat-card">
                    <div class="stat-card-value"><i class="fas fa-building"></i></div>
                    <div class="stat-card-label">Companies</div>
                </div>
                <div class="stats-grid">
                    <div class="stat-card is-info">
                        <div class="stat-card-value is-info">{{ stats.total_companies }}</div>
                        <div class="stat-card-label is-info">Total Companies</div>
                    </div>
                    <div class="stat-card is-success">
                        <div class="stat-card-value is-success">{{ stats.approved_companies }}</div>
                        <div class="stat-card-label is-success">Active Companies</div>
                    </div>
                    <div class="stat-card is-warning">
                        <div class="stat-card-value is-warning">{{ stats.rejected_companies }}</div>
                        <div class="stat-card-label is-warning">Pending Companies</div>
                    </div>
                    <div class="stat-card is-error">
                        <div class="stat-card-value is-error">{{ stats.pending_companies }}</div>
                        <div class="stat-card-label is-error">Rejected Companies</div>
                    </div>
                    <div class="stat-card is-error">
                        <div class="stat-card-value is-error">{{  stats.blacklisted_companies  }}</div>
                        <div class="stat-card-label is-error">Blacklisted Companies</div>
                    </div>
                </div>
            </div>
            
            <div class="custom-grid">
                <div class="title-card stat-card">
                    <div class="stat-card-value"><i class="fas fa-briefcase"></i></div>
                    <div class="stat-card-label">Drives</div>
                </div>
                <div class="stats-grid">
                    <div class="stat-card is-info">
                        <div class="stat-card-value is-info">{{ stats.total_drives }}</div>
                        <div class="stat-card-label is-info">Total Drives</div>
                    </div>
                    <div class="stat-card is-success">
                        <div class="stat-card-value is-success">{{ stats.approved_drives }}</div>
                        <div class="stat-card-label is-success">Approved Drives</div>
                    </div>
                    <div class="stat-card is-warning">
                        <div class="stat-card-value is-warning">{{ stats.pending_drives }}</div>
                        <div class="stat-card-label is-warning">Pending Drives</div>
                    </div>
                    <div class="stat-card is-error">
                        <div class="stat-card-value is-error">{{ stats.rejected_drives }}</div>
                        <div class="stat-card-label is-error">Rejected Drives</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-card-value">{{ stats.closed_drives }}</div>
                        <div class="stat-card-label">Closed Drives</div>
                    </div>
                </div>
            </div>

            <div class="custom-grid">
                <div class="title-card stat-card">
                    <div class="stat-card-value"><i class="fas fa-file-alt"></i></div>
                    <div class="stat-card-label">Applications</div>
                </div>
                <div class="stats-grid">
                    <div class="stat-card is-info">
                        <div class="stat-card-value is-info">{{ stats.total_applications }}</div>
                        <div class="stat-card-label is-info">Total Applications</div>
                    </div>
                    <div class="stat-card is-success">
                        <div class="stat-card-value is-success">{{ stats.total_placements }}</div>
                        <div class="stat-card-label is-success">Total Placements</div>
                    </div>
                </div>
            </div>
        </template>
    </div>
</template>

<style scoped>
.custom-grid {
    display: flex;
    align-items: center;
    gap: 24px;
    margin-top: 32px;
}

.title-card.stat-card {
    text-align: center;
    width: 125px;
}

.stats-grid {    
  grid-template-columns: repeat(5, 1fr);
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