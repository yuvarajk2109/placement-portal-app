<template>
    <div class="main-page">
        <div class="flex items-center justify-between mb-24">
            <h1 class="page-title">Drives</h1>
            <button class="btn is-primary" @click="showCreateModal = true"><i class="fa-solid fa-plus"></i> Create Drive</button>
        </div>
        <AppSpinner v-if="loading" />
        <table v-else-if="drives.length > 0" class="data-table">
            <thead>
                <tr>
                    <th>Job Title</th>
                    <th>Type</th>
                    <th>CGPA Requirement</th>
                    <th>Location</th>
                    <th>Deadline</th>
                    <th>No. of Applications</th>
                    <th>Drive Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr 
                    v-for="drive in drives" 
                    :key="drive.drive_id" 
                    class="clickable-row"
                    @click="$router.push({ name: 'company-drive-detail', params: { id: drive.drive_id } })"> 
                    <!-- <router-link :to="{ name: 'company-drive-detail', params: { id: drive.drive_id } }" class="text-link" /> -->
                    <td>{{ drive.job_title }}</td>
                    <td><span class="status is-info">{{ drive.drive_type }}</span></td>
                    <td>{{ drive.cgpa_requirement }}</td>
                    <td>{{ drive.location }}</td>
                    <td>{{ drive.application_deadline ? formatDateTime(drive.application_deadline) : '' }}</td>
                    <td>{{ drive.applications_count }}</td>
                    <td><span class="status" :class="statusClass(drive.status)">{{ drive.status }}</span></td>
                    <td>
                        <button v-if="drive.status === 'Approved'" class="btn is-warning" @click="closeDrive(drive.drive_id)">Close Drive</button>
                        <div v-else>-</div>
                    </td>
                </tr>
            </tbody>
        </table>        
        <div v-else class="card">
            <div class="empty-state">
                <p class="empty-state-text">No drives started. Go ahead and create a drive to hire our smartest minds!</p>
            </div>
        </div>
        <AppPagination 
            v-model:currentPage="page" 
            :totalPages="totalPages" 
            @page-change="fetchDrives" 
        />

        <AppModal v-model="showCreateModal">
            <template #title>Create Placement Drive</template>
            <form id="create-drive-form" @submit.prevent="createDrive">
                <div class="form-group">
                    <label class="form-label" for="job_title">Job Title <span class="required">(required)</span></label>
                    <input id="job_title" v-model="newDrive.job_title" type="text" @blur="validator.job_title.$touch()" class="form-input" :class="{'is-error': validator.job_title.$error}">
                    <span v-if="validator.job_title.$error" class="form-error-text">{{ validator.job_title.$errors[0].$message }}</span>
                </div>
                <div class="form-group">
                    <label class="form-label" for="job_desc">Job Description <span class="required">(required)</span></label>
                    <textarea id="job_desc" v-model="newDrive.job_desc" @blur="validator.job_desc.$touch()" class="form-textarea" :class="{'is-error': validator.job_desc.$error}"></textarea>
                    <span v-if="validator.job_desc.$error" class="form-error-text">{{ validator.job_desc.$errors[0].$message }}</span>
                </div>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="drive_type">Drive Type <span class="required">(required)</span></label>
                        <select id="drive_type" v-model="newDrive.drive_type" @blur="validator.drive_type.$touch()" class="form-select" :class="{'is-error': validator.drive_type.$error}">
                            <option value="" disabled>Select drive type...</option>
                            <option value="2M Internship">2M Internship</option>
                            <option value="5M Internship">5M Internship</option>
                            <option value="6M Internship">6M Internship</option>
                            <option value="5M Internship + Placement">5M Internship + Placement</option>
                            <option value="6M Internship + Placement">6M Internship + Placement</option>
                            <option value="5M Internship + Performance-based Placement">5M Internship + Performance-based Placement</option>
                            <option value="6M Internship + Performance-based Placement">6M Internship + Performance-based Placement</option>
                            <option value="Direct Placement">Direct Placement</option>
                        </select>
                        <span v-if="validator.drive_type.$error" class="form-error-text">{{ validator.drive_type.$errors[0].$message }}</span>
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="application_deadline">Application Deadline <span class="required">(required)</span></label>
                        <input id="application_deadline" v-model="newDrive.application_deadline" type="datetime-local" @blur="validator.application_deadline.$touch()" class="form-input" :class="{'is-error': validator.application_deadline.$error }">
                        <span v-if="validator.application_deadline.$error" class="form-error-text">{{ validator.application_deadline.$errors[0].$message }}</span>
                    </div>
                </div>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="location">Location</label>
                        <input id="location" v-model="newDrive.location" type="text" class="form-input">
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="cgpa_requirement">Min CGPA Requirement <span class="required">(required)</span></label>
                        <input id="cgpa_requirement" v-model="newDrive.cgpa_requirement" type="text" @blur="validator.cgpa_requirement.$touch()" class="form-input" :class="{'is-error': validator.cgpa_requirement.$error}">
                        <span v-if="validator.cgpa_requirement.$error" class="form-error-text">{{ validator.cgpa_requirement.$errors[0].$message }}</span>
                    </div>
                </div>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="location">Min Salary (LPA)</label>
                        <input id="location" v-model="newDrive.salary_min" type="text" class="form-input">
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="salary_max">Max Salary (LPA) <span class="required">(required)</span></label>
                        <input id="salary_max" v-model="newDrive.salary_max" type="text" @blur="validator.salary_max.$touch()" class="form-input" :class="{'is-error': validator.salary_max.$error}">
                        <span v-if="validator.salary_max.$error" class="form-error-text">{{ validator.salary_max.$errors[0].$message }}</span>
                    </div>
                </div>
                <div class="form-group">                    
                    <label class="form-label">Eligible Branches <span class="required">(required)</span></label>
                    <AppMultiSelect 
                        v-model="newDrive.eligible_branches" 
                        :options="branches" 
                        value="branch_name" 
                        id="branch_id"
                        @blur="validator.eligible_branches.$touch()"
                    />
                    <span v-if="validator.eligible_branches.$error" class="form-error-text">{{ validator.eligible_branches.$errors[0].$message }}</span>
                </div>
                <div class="form-group">
                    <label class="form-label">Required Skills</label>
                    <AppMultiSelect 
                        v-model="newDrive.skill_ids" 
                        :options="skills" 
                        value="skill_name" 
                        id="skill_id"
                    />
                </div>
            </form>
            <template #footer>
                <button type="button" class="btn is-secondary" @click="showCreateModal = false">Cancel</button>
                <button type="submit" form="create-drive-form" class="btn is-primary" :disabled="creating || validator.$invalid">{{ creating ? 'Creating' : 'Create Drive' }}</button>
            </template>
        </AppModal>
    </div>
</template>

<script setup>
import AppModal from '@/components/ui/AppModal.vue';
import AppMultiSelect from '@/components/ui/AppMultiSelect.vue';
import api from '@/services/api';
import { useDialogStore } from '@/stores/dialog';
import { useNotificationStore } from '@/stores/notification';
import { formatDateTime } from '@/utils/formatters';
import useVuelidate from '@vuelidate/core';
import { helpers, required } from '@vuelidate/validators';
import { onMounted, reactive, ref } from 'vue';

const notify = useNotificationStore();
const dialog = useDialogStore();
const loading = ref(true);
const creating = ref(false);
const showCreateModal = ref(false);
const drives = ref([]);
const branches = ref([]);
const skills = ref([]);
const page = ref(1);
const totalPages = ref(1);

const newDrive = reactive({
    job_title: '',
    job_desc: '',
    drive_type: '',
    cgpa_requirement: '',
    salary_min: null,
    salary_max: '',
    location: null,
    application_deadline: '',
    eligible_branches: [],
    skill_ids: []
});

const rules = {
    job_title: { 
        required: helpers.withMessage('Job title is required', required) 
    },
    job_desc: { 
        required: helpers.withMessage('Job description is required', required)
    },
    drive_type: { 
        required: helpers.withMessage('Drive type is required', required) 
    },
    cgpa_requirement: { 
        required: helpers.withMessage('CGPA Requirement is required', required)
    },
    salary_max: {
        required: helpers.withMessage('Salary is required', required)
    },
    application_deadline: {
        required: helpers.withMessage('Deadline is required', required)
    },
    eligible_branches: {
        required: helpers.withMessage('At least one branch is required', required)
    }
};

const validator = useVuelidate(rules, newDrive);

const driveTemplate = {
    job_title: '',
    job_desc: '',
    drive_type: '',
    cgpa_requirement: '',
    salary_min: '',
    salary_max: '',
    location: '',
    application_deadline: '',
    eligible_branches: [],
    skill_ids: []
}

onMounted(async () => {
  await fetchDrives();
  try {
    const [branchResult, skillResult] = await Promise.all([
        api.get('/shared/branches'),
        api.get('/shared/skills')
    ]);
    branches.value = branchResult.data.branches;
    skills.value = skillResult.data.skills;
  } catch (err) {
    notify.error('Failed to load branches/skills data');
  }
})

async function fetchDrives() {
    loading.value = true;
    try {
        const params = { page: page.value, per_page: 10 };
        const result = await api.get('/company/drives', { params });
        drives.value = result.data.drives;
        totalPages.value = result.data.pages
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to load drives');
    } finally {
        loading.value = false;
    }
}

async function createDrive() {
    validator.value.$touch();
    if (validator.value.$invalid) return;
    creating.value = true;
    try {
        await api.post('/company/drives', newDrive);
        notify.success('Drive created. Awaiting university approval.');
        showCreateModal.value = false;
        Object.assign(newDrive, driveTemplate);
        validator.value.$reset();
        fetchDrives();
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to create drive');
    } finally {
        creating.value = false;
    }
}

async function closeDrive(id) {
    const confirmed = await dialog.confirm({
        title: 'Close Drive',
        message: 'Close this drive? No more applications will be accepted.',
        type: 'warning',
        confirmText: 'Close',
        cancelText: 'Cancel'
    })
    if (!confirmed) return;
    try {
        await api.put(`/company/drives/${id}/close`);
        notify.success('Drive closed');
        fetchDrives();
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to close drive');
    }
}

function statusClass(status) {
    return {
        Pending: 'is-warning',
        Approved: 'is-success',
        Rejected: 'is-error',
        Closed: 'is-secondary'
    } [status] || 'is-info'
}
</script>