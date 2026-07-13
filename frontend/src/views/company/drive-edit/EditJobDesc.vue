<template>
    <AppModal v-model="modal" size="small"> 
        <template #title>Edit Job Description</template>
        <form @submit.prevent="updateJobDescription">
            <div class="form-group">
                <textarea id="job_desc" class="form-textarea" v-model="updateForm.job_desc"></textarea>
            </div>
            <button type="submit" class="btn is-primary full-width-btn" :disabled="saving">{{ saving ? 'Saving Changes...' : 'Save Changes' }}</button>
        </form>
    </AppModal>
</template>

<script setup>
import AppModal from '@/components/ui/AppModal.vue';
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { computed, reactive, ref } from 'vue';

const notify = useNotificationStore();
const saving = ref(false);

const properties = defineProps({
    modelValue: {
        type: Boolean,
        required: true
    },
    driveId: {
        type: Number,
        required: true
    },
    jobDesc: {
        type: String,
        required: true
    }
})

const updateForm = reactive({
    job_desc: properties.jobDesc}
);

const emit = defineEmits([
    'update:modelValue',
    'updated'
]);

const modal = computed({
    get: () => properties.modelValue,
    set: value => emit('update:modelValue', value)
});

async function updateJobDescription() {
    saving.value = true;
    try {
        const result = await api.put(`/company/drives/${properties.driveId}`, updateForm);
        notify.success(result.data.message || 'Job description has been updated successfully. Drive requires admin approval.');
        emit('updated');
    } catch (err) {
        notify.error(err.response?.data?.error);
    } finally {
        saving.value = false;
        modal.value = false;
    }
}

</script>