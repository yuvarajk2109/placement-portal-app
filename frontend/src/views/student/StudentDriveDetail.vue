<template>
    <div class="main-page">
        <AppSpinner v-if="loading" />
        <div v-else-if="drive">
            <div class="full-width mb-24">
                <div class="flex items-center justify-between">
                    <h1 class="page-title mb-4">{{ drive.job_title }}</h1>
                    <div class="flex gap-16">                        
                    <button class="btn is-primary" v-if="!drive.already_applied" :disabled="applying" @click="applyForDrive">{{ applying ? 'Applying' : 'Apply for Drive' }}</button>
                    <router-link 
                        to="/student/drives"
                        class="btn is-secondary">
                        Go Back
                    </router-link>
                    </div>
                </div>
                <p class="page-subtitle">{{ drive.company_name }} &middot; <span class="status" :class="statusClass(drive.application_status)">{{ drive.application_status }}</span></p>
            </div>
            <div class="card mb-24">
                <h2 class="card-title">Drive Details</h2>
                <div class="stats-grid">
                    <div class="stat-card info">
                        <div class="stat-card-value info">
                            {{ drive.drive_type }}
                        </div>
                        <div class="stat-card-label info">
                            Type
                        </div>
                    </div>
                    <div class="stat-card info">
                        <div class="stat-card-value info">
                            {{ drive.cgpa_requirement }}
                        </div>
                        <div class="stat-card-label info">
                            CGPA Requirement
                        </div>
                    </div>
                    <div class="stat-card warning">
                        <div class="stat-card-value warning">
                            {{ formatDateTime(drive.application_deadline) }}
                        </div>
                        <div class="stat-card-label warning">
                            Application Deadline
                        </div>
                    </div>
                    <div class="stat-card success">
                        <div class="stat-card-value success">
                            {{ drive.salary_min || '' }} {{ drive.salary_min ? ' - ' : ''}} {{ drive.salary_max }} LPA
                        </div>
                        <div class="stat-card-label success">
                            Salary
                        </div>
                    </div>
                </div>
            </div>
            <div class="card mb-24">
                <h2 class="card-title">Job Description</h2>
                <p class="text-subtle">{{ drive.job_desc }}</p>
            </div>
            <div class="card mb-24">
                <h2 class="card-title">Eligible Branches</h2>
                <AppMultiSelect
                    :model-value="drive.eligible_branches.map(branch => branch.branch_id)"
                    :options="drive.eligible_branches"
                    value="branch_name"
                    id="branch_id"
                    :readonly="true"
                />
            </div>
            <div class="card mb-24">
                <h2 class="card-title">Required Skills</h2>
                <AppMultiSelect
                    :model-value="drive.required_skills.map(skill => skill.skill_id)"
                    :options="drive.required_skills"
                    value="skill_name"
                    id="skill_id"
                    :readonly="true"
                />
            </div>
            <studentDriveInterviews :drive-id="driveId"/>
        </div>
    </div>
</template>

<style scoped>
.stats-grid {
    display: inline-flex;
    grid-template-columns: auto;
}
</style>

<script setup>
import AppSpinner from '@/components/ui/AppSpinner.vue';
import AppMultiSelect from '@/components/ui/AppMultiSelect.vue';
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { formatDateTime } from '@/utils/formatters';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const notify = useNotificationStore();
const driveId = route.params.id;
const loading = ref(true);
const applying = ref(false);
const drive = ref(null);

onMounted(fetchDrive);

async function fetchDrive() {
    loading.value = true;
    try {
        const result = await api.get(`/student/drives/${driveId}`);
        drive.value = result.data;
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to load drive details');
        router.push({ name: 'student-drives'});
    } finally {
        loading.value = false;
    }
}

async function applyForDrive() {
    applying.value = true;
    try {
        await api.post(`/student/drives/${driveId}/apply`);
        notify.success('Your application has been submitted!');
        fetchDrive();
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to apply');
    } finally {
        applying.value = false;
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