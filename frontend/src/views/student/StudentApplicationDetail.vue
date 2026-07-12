<template>
    <AppSpinner v-if="loading" />
    <template v-else>
        <div class="card mb-24">
            <h2 class="card-title">Application Details</h2>
            <div class="detail-row-2">
                <div class="detail-item">
                    <div class="detail-label">Applied Date</div>
                    <div class="detail-value">{{ formatDateTime(application.applied_date) }}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Status</div>
                    <div class="detail-value"><span class="status" :class="statusClass(application.status)">{{ application.status }}</span></div>
                </div>
            </div>
        </div>
        <div class="card mb-24">
            <h2 class="card-title">Job Details</h2>
            <div class="detail-row-1 mb-16">
                <div class="detail-item">
                    <div class="detail-label">Job Description</div>
                    <div class="detail-value">{{ application.job_desc }}</div>
                </div>
            </div>
            <div class="detail-row-2">
                <div class="detail-item">
                    <div class="detail-label">Salary</div>
                    <div class="detail-value">
                        <span v-if="application.salary_min">{{ application.salary_min }} -</span>
                        <span>{{ application.salary_max }} LPA</span>
                    </div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Location</div>
                    <div class="detail-value">{{ application.location }}</div>
                </div>
            </div>            
        </div>
        <div v-if="application.current_round_id" class="card">
            <h2 class="card-title">My Progress</h2>
            <div class="detail-row-3">
                <div class="detail-item">
                    <div class="detail-label">Current Round Number</div>
                    <div class="detail-value">Round {{ application.current_round_number }}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Round Title</div>
                    <div class="detail-value">{{ application.current_round_title }}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Round Location</div>
                    <div class="detail-value">{{ application.current_round_location }}</div>
                </div>
            </div> 
            <div v-if="application.feedback" class="detail-row-1 mt-16">
                <div class="detail-item">
                    <div class="detail-label">Feedback for Previous Round</div>
                    <div class="detail-value">{{ application.feedback }}</div>
                </div>
            </div>
        </div>
        
    </template>
    
</template>

<style scoped>
.detail-row-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
}

.detail-row-2 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
}

.detail-row-1 {
    display: grid;
    grid-template-columns: auto;
}

.detail-item {
    color: var(--surface-foreground);
}
.detail-label {
    font-weight: 600;
    margin-bottom: 2px;
}
</style>

<script setup>
import AppSpinner from '@/components/ui/AppSpinner.vue';
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { formatDateTime } from '@/utils/formatters';
import { onMounted, ref } from 'vue';


const notify = useNotificationStore();
const loading = ref(true);
const application = ref([]);
const properties = defineProps({
    application_id: {
        type: Number,
        required: true
    }
})

onMounted(fetchApplication);

async function fetchApplication() {
    try {
        const result = await api.get(`student/applications/${properties.application_id}`);
        application.value = result.data;
        console.log(result.data)
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to load application');
    } finally {
        loading.value = false
    }
}

function statusClass(status) {
    return {
        Applied: 'is-info',
        Shortlisted: 'is-warning',
        Selected: 'is-success',
        Rejected: 'is-error',
        Withdrawn: 'is-neutral'
    } [status] || 'is-neutral'
}
</script>