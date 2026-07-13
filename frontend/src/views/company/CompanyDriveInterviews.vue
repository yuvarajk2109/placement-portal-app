<template>
    <div class="main-page">   
        <div class="card">            
            <div class="flex justify-between mb-24">
                <h2 class="card-title">Interview Rounds</h2>
                <span class="flex gap-8">
                    <button type="button" class="btn is-primary" @click="showModal = true">
                        <i class="fas fa-plus"></i> 
                        Schedule New Interview
                    </button>
                </span>
            </div>
            <AppSpinner v-if="loading" />
            <template v-else-if="interviews.length > 0">                
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Round</th>
                            <th>Title</th>
                            <th>Date</th>
                            <th>Location</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="interview in interviews" :key="interview.interview_id">
                            <td>{{ interview.round_number }}</td>
                            <td>{{ interview.round_title }}</td>
                            <td>{{ interview.interview_date ? formatDateTime(interview.interview_date) : '-' }}</td>
                            <td>{{ interview.location || '-' }}</td>
                            <td class="actions-cell">
                                <button class="btn is-secondary" @click="editInterview(interview)">Edit</button>
                            </td>
                        </tr>
                    </tbody>
                </table>        
            </template>
            <div v-else class="empty-state">
                <p class="empty-state-text">No interviews scheduled yet. Schedule a new interview!</p>
            </div>
        </div>
       
        <AppModal v-model="showModal" size="small">
            <template #title>{{ editingId ? 'Edit Interview' : 'Schedule New Interview' }}</template>
            <form id="interview-form" @submit.prevent="submitInterview">
                <div class="form-group">
                    <label class="form-label" for="round_title">Round Title <span class="required">(required)</span></label>
                    <input id="round_title" type="text" v-model="interviewForm.round_title" @blur="validator.round_title.$touch()" class="form-input" :class="{ 'is-error': validator.round_title.$error }">    
                    <span v-if="validator.round_title.$error" class="form-error-text">{{ validator.round_title.$errors[0].$message }}</span>    
                </div>
                <div class="form-group">
                    <label class="form-label" for="interview_date">Interview Date <span class="required">(required)</span></label>
                    <input id="interview_date" type="datetime-local" v-model="interviewForm.interview_date" @blur="validator.interview_date.$touch()" class="form-input" :class="{ 'is-error': validator.interview_date.$error }">
                    <span v-if="validator.interview_date.$error" class="form-error-text">{{ validator.interview_date.$errors[0].$message }}</span>
                </div>
                <div class="form-group">
                    <label class="form-label" for="location">Location <span class="required">(required)</span></label>
                    <input id="location" type="text" v-model="interviewForm.location" @blur="validator.location.$touch()" class="form-input" :class="{ 'is-error': validator.location.$error }">
                    <span v-if="validator.location.$error" class="form-error-text">{{ validator.location.$errors[0].$message }}</span>
                </div>
            </form>
            <template #footer>
                <button type="button" class="btn is-secondary" @click="closeModal">Cancel</button>
                <button type="submit" form="interview-form" class="btn is-primary" :disabled="submitting || validator.$invalid">{{ submitting ? 'Saving' : 'Save' }}</button>
            </template>
        </AppModal>
    </div>
</template>

<script setup>
import AppModal from '@/components/ui/AppModal.vue';
import AppSpinner from '@/components/ui/AppSpinner.vue';
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { formatDateTime } from '@/utils/formatters';
import useVuelidate from '@vuelidate/core';
import { helpers, required } from '@vuelidate/validators';
import { computed, onMounted, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const notify = useNotificationStore();
const loading = ref(true);
const submitting = ref(false);
const showModal = ref(false);
const editingId = ref(null);
const interviews = ref([]);

const properties = defineProps({
    driveId: {
        type: [String],
        required: true
    }
});

const interviewForm = reactive({
    round_title: '',
    interview_date: '',
    location: ''
});

const interviewEmptyForm = reactive({
    round_title: '',
    interview_date: '',
    location: ''
});

const rules = computed(() => ({
    round_title: {
        required: helpers.withMessage('Round title is required', required)
    },
    interview_date: {
        required: helpers.withMessage('Interview date is required', required)
    },
    location: {
        required: helpers.withMessage('Location is required', required)
    }
}));

const validator = useVuelidate(rules, interviewForm);

onMounted(fetchInterviews);

async function fetchInterviews() {
    loading.value = true;
    try {
        const result = await api.get(`/company/drives/${properties.driveId}/interviews`);
        interviews.value = result.data.interviews;
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to load interviews');
    } finally {
        loading.value = false;
    }
}

function editInterview(interview) {
    editingId.value = interview.interview_id;
    interviewForm.round_title = interview.round_title;
    interviewForm.interview_date = interview.interview_date ? interview.interview_date.slice(0, 16) : '';
    interviewForm.location = interview.location || '';
    showModal.value = true;
}

function closeModal() {
    showModal.value = false;
    editingId.value = null;
    Object.assign(interviewForm, interviewEmptyForm);
}

async function submitInterview() {
    validator.value.$touch();
    if (validator.value.$invalid) return;

    submitting.value = true;
    try {
        if (editingId.value) {
            await api.put(`/company/interviews/${editingId.value}`, interviewForm);
            notify.success('Interview updated successfully');
        } else {
            await api.post(`/company/drives/${properties.driveId}/interviews`, interviewForm);
            notify.success('Interview scheduled successfully.');
        }
        closeModal();
        fetchInterviews();
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to save interviews');
    } finally {
        submitting.value = false;
    }
}
</script>