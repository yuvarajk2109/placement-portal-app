<template>
    <div class="main-page">
        <AppSpinner v-if="loading" />
        <template v-else-if="drive">
            <div class="full-width mb-24">
                <div class="flex items-center justify-between">
                    <h1 class="page-title mb-4">{{ drive.job_title }}</h1>
                    <router-link 
                        to="/company/drives"
                        class="btn is-secondary">
                        Go Back
                    </router-link>
                </div>
                <p class="page-subtitle">{{ drive.company_name }} &middot; <span class="status" :class="interviewStatusClass(drive.status)">{{ drive.status }}</span></p>
            </div>
            <div class="flex gap-16 mb-24">
                <router-link
                v-if="drive.applications_count > 0" 
                :to="{ name: 'company-drive-applications', params: { id: driveId } }" 
                class="btn is-primary">
                    View Applications ({{ drive.applications_count }})
                </router-link>
            </div>
            <div class="card mb-24">
                <div class="flex items-center justify-between mb-16">
                    <h2 class="card-title">Drive Details</h2>
                    <button type="button" class="btn is-secondary is-icon-only" v-if="canEdit" @click="modals.driveEdit = true"><i class="fas fa-edit"></i></button>
                </div>
                <div class="stats-grid">
                    <div class="stat-card is-info">
                        <div class="stat-card-value is-info">{{ drive.drive_type }}</div>
                        <div class="stat-card-label is-info">Type</div>
                    </div>
                    <div class="stat-card is-info">
                        <div class="stat-card-value is-info">{{ drive.cgpa_requirement }}</div>
                        <div class="stat-card-label is-info">CGPA Requirement</div>
                    </div>
                    <div class="stat-card is-warning">
                        <div class="stat-card-value is-warning">{{ formatDateTime(drive.application_deadline) }}</div>
                        <div class="stat-card-label is-warning">Application Deadline</div>
                    </div>
                    <div class="stat-card is-success">
                        <div class="stat-card-value is-success">{{ drive.salary_min || '' }} {{ drive.salary_min ? ' - ' : ''}} {{ drive.salary_max }} LPA</div>
                        <div class="stat-card-label is-success">Salary</div>
                    </div>
                </div>
            </div>
            <div class="card mb-24">
                <div class="flex items-center justify-between mb-16">
                    <h2 class="card-title">Job Description</h2>
                    <button v-if="canEdit" type="button" class="btn is-secondary is-icon-only" @click="modals.jobDescEdit = true"><i class="fas fa-edit"></i></button>
                </div>
                <p>{{ drive.job_desc }}</p>
            </div>
            <div class="card mb-24">
                <div class="flex items-center justify-between mb-16">
                    <h2 class="card-title">Eligible Branches</h2>
                    <button type="button" class="btn is-secondary is-icon-only" v-if="canEdit" @click="modals.eligibleBranchesEdit = true"><i class="fas fa-edit"></i></button>
                </div>
                <AppMultiSelect
                    :model-value="drive.eligible_branches.map(branch => branch.branch_id)"
                    :options="drive.eligible_branches"
                    value="branch_name"
                    id="branch_id"
                    :readonly="true"
                />
            </div>
            <div class="card mb-24">
                <div class="flex items-center justify-between mb-16">
                    <h2 class="card-title">Required Skills</h2>
                    <button type="button" class="btn is-secondary is-icon-only" v-if="canEdit" @click="modals.requiredSkillsEdit = true"><i class="fas fa-edit"></i></button>
                </div>
                <AppMultiSelect
                    :model-value="drive.required_skills.map(skill => skill.skill_id)"
                    :options="drive.required_skills"
                    value="skill_name"
                    id="skill_id"
                    :readonly="true"
                />
            </div>
            <CompanyDriveInterviews :drive-id="driveId"/>
            <EditDriveDetails 
                v-model="modals.driveEdit"
                @updated="fetchDrive"
                :driveId="drive.drive_id"
                :driveType="drive.drive_type"
                :cgpaRequirement="drive.cgpa_requirement"
                :applicationDeadline="drive.application_deadline"
                :salaryMin="drive.salary_min"
                :salaryMax="drive.salary_max"
            />  
            <EditJobDesc 
                v-model="modals.jobDescEdit"
                @updated="fetchDrive"
                :driveId="drive.drive_id"
                :jobDesc="drive.job_desc"
            /> 
            <EditEligibleBranches 
                v-model="modals.eligibleBranchesEdit"
                @updated="fetchDrive"
                :driveId="drive.drive_id"
                :eligibleBranches="drive.eligible_branches"
            />
            <EditRequiredSkills
                v-model="modals.requiredSkillsEdit"
                @updated="fetchDrive"
                :driveId="drive.drive_id"
                :requiredSkills="drive.required_skills"
            />
        </template> 
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
import { useDialogStore } from '@/stores/dialog';
import { useNotificationStore } from '@/stores/notification';
import { formatDateTime } from '@/utils/formatters';
import { computed, onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import CompanyDriveInterviews from './CompanyDriveInterviews.vue';
import EditEligibleBranches from './drive-edit/EditEligibleBranches.vue';
import EditRequiredSkills from './drive-edit/EditRequiredSkills.vue';
import EditDriveDetails from './drive-edit/EditDriveDetails.vue';
import EditJobDesc from './drive-edit/EditJobDesc.vue';
import { interviewStatusClass } from '@/utils/status.js';

const route = useRoute();
const router = useRouter();
const notify = useNotificationStore();
const dialog = useDialogStore();
const driveId = route.params.id;
const loading = ref(true);
const drive = ref(null);

const canEdit = computed(() => {
    if (!drive.value) return false;
    return new Date(drive.value.application_deadline) > new Date();
});

const modals = reactive({
    driveEdit: false,
    jobDescEdit: false,
    eligibleBranchesEdit: false,
    requiredSkillsEdit: false
})

onMounted(fetchDrive);

async function fetchDrive() {
    loading.value = true;
    try {
        const result = await api.get(`/company/drives/${driveId}`);
        drive.value = result.data;
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to load drive details');
        router.push({ name: 'company-drives'});
    } finally {
        loading.value = false;
    }
}

async function closeDrive(id) {
    const confirmed = await dialog.confirm({
        title: 'Close Drive',
        message: 'Close this drive? No more applications will be accepted.',
        type: 'warning',
        confirmText: 'Close'
    })
    if (!confirmed) return;
    try {
        const result = await api.put(`/company/drives/${id}/close`);
        notify.success(result.data?.message || 'Drive closed');
        fetchDrive();
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to close drive');
    }
}
</script>