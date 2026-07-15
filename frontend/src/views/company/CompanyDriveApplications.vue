<template>
    <div class="main-page">
        <div class="flex items-center justify-between mb-16">
            <h1 class="page-title mb-4">Drive Applications</h1>

            <AppTooltip text="Go Back"> 
                <router-link 
                    :to="{ name: 'company-drive-detail', params: { id: driveId } }"
                    class="btn is-icon-only is-secondary">
                    <i class="fa-solid fa-angles-left"></i>
                </router-link>
            </AppTooltip>
            
        </div>
        <div class="card">
            <AppSpinner v-if="loading || saving" />
            <table v-else-if="applications.length > 0" class="data-table">
                <thead>
                    <tr>
                        <th>Student</th>
                        <th>Register No.</th>
                        <th>CGPA</th>
                        <th>Applied Date</th>
                        <th>Status</th>
                        <th>Round</th>
                        <th>Feedback from Previous Round</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="application in applications" :key="application.application_id">
                        <td>{{ application.student_name }}</td>
                        <td>{{ application.register_no }}</td>
                        <td>{{ application.cgpa }}</td>
                        <td>{{ formatDateTime(application.applied_date) }}</td>
                        <td><span class="status" :class="interviewStatusClass(application.application_status)">{{ application.application_status }}</span></td>
                        <td>{{ application.current_round || '-' }}</td>
                        <td>{{ application.feedback || 'None'}}</td>
                        <td class="actions-cell">
                            <select v-if="application.application_status != 'Withdrawn' && getAvailableActions(application).length > 0" class="form-select" @change="updateStatus(application.student_name, application.application_id, $event.target?.value); $event.target.value = ''">
                                <option value="">Update...</option>
                                <option v-for="action in getAvailableActions(application)" :type="action" :value="action">{{ action }}</option>
                            </select>
                            <span v-else>None</span>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div v-else class="empty-state">
                <p class="empty-state-text">No applications for this drive yet.</p>
            </div>
            <AppPagination 
                v-model:currentPage="page" 
                :totalPages="totalPages" 
                @page-change="fetchApplications" 
            />
        </div>

        <AppModal v-model="showModal" size="medium">
            <template #title>Update Status of {{ studentName }} - <span class="status" :class="interviewStatusClass(updateForm.application_status)">{{ updateForm.application_status }}</span></template>
            <form id="application-feedback-form" @submit.prevent="finaliseStatus">
                <div class="form-group">
                    <div v-if="updateForm.application_status === 'Selected'">
                        <label for="joining_date" class="form-label">Joining Date <span class="required">(required)</span></label>
                        <input id="joining_date" type="date" v-model="updateForm.joining_date" class="form-input" @blur="validator.joining_date.$touch()" :class="{ 'is-error': validator.joining_date.$error }">
                        <span class="form-error-text" v-if="validator.joining_date.$error">{{ validator.joining_date.$errors[0].$message }}</span>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="feedback" class="form-label">Feedback <span class="required">(if any)</span></label>
                    <textarea id="feedback" v-model="updateForm.feedback" class="form-textarea"></textarea>
                </div>
            </form>
            <template #footer>
                <button type="button" class="btn is-secondary" @click="closeModal">Cancel</button>
                <button type="submit" form="application-feedback-form" class="btn is-primary" :disabled="saving || validator.$invalid">{{ saving ? 'Saving' : 'Save' }}</button>
            </template>
        </AppModal>
    </div>
</template>

<script setup>
import AppModal from '@/components/ui/AppModal.vue';
import AppPagination from '@/components/ui/AppPagination.vue';
import AppSpinner from '@/components/ui/AppSpinner.vue';
import AppTooltip from '@/components/ui/AppTooltip.vue';
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { formatDateTime } from '@/utils/formatters';
import { interviewStatusClass } from '@/utils/status';
import useVuelidate from '@vuelidate/core';
import { helpers, required, requiredIf } from '@vuelidate/validators';
import { computed, onMounted, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const notify = useNotificationStore();
const driveId = route.params.id;
const loading = ref(true);
const applications = ref([]);
const page = ref(1);
const totalPages = ref(1);
const saving = ref(false);
const showModal = ref(false);
const actions = ref([]);
const studentName = ref('');

const updateForm = reactive({
    applicationId: '',
    application_status: '',
    feedback: '',
    joining_date: ''
})

const emptyForm = reactive({
    applicationId: '',
    application_status: '',
    feedback: '',
    joining_date: ''
})

const rules = computed(() => ({
    joining_date: {
        required: helpers.withMessage('Joining date is required for selected candidate', requiredIf(() => updateForm.application_status === 'Selected')),
    }
}));

const validator = useVuelidate(rules, updateForm);

onMounted(fetchApplications);

async function fetchApplications() {
    loading.value = true;
    try {
        const params = { page: page.value };
        const [applicationsResult, actionsResult] = await Promise.all([
            api.get(`/company/drives/${driveId}/applications`, { params }),
            api.get('/shared/application-actions')
        ]);
        applications.value = applicationsResult.data.applications;
        totalPages.value = applicationsResult.data.pages;
        actions.value = actionsResult.data.application_actions;
        
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to load applications');
    } finally {
        loading.value = false;
    }
}

async function updateStatus(student_name, application_id, updatedStatus) {
    if (!updatedStatus) return;
    updateForm.applicationId = application_id;
    studentName.value = student_name;
    updateForm.application_status = updatedStatus;
    if (updatedStatus === 'Shortlisted') {
        finaliseStatus();
        return;
    }
    showModal.value = true;
}

async function finaliseStatus() {
    validator.value.$touch();
    if (validator.value.$invalid) return;
    closeModal();
    saving.value = true;
    try {
        const result = await api.put(`/company/applications/${updateForm.applicationId}/status`, updateForm);
        notify.success(result.data?.message || `Application status updated to ${updateForm.application_status}`);
        Object.assign(updateForm, emptyForm);
        fetchApplications();
    } catch (err) {
        notify.error(err.response?.data?.error || `Failed to update status to ${updateForm.application_status}`);
    } finally {
        saving.value = false;
        
    }
}

function closeModal() {
    showModal.value = false;
}

function getAvailableActions(application) {
    if (application.application_status === 'Selected') {
        return [];
    }
    if (['Shortlisted', 'Rejected'].includes(application.application_status)) {
        return actions.value.filter(
            action => action !== application.application_status
        );
    }
    return actions.value;
}
</script>