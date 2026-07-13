<template>
    <AppModal v-model="modal" size="small">
        <template #title>Edit Drive Details</template>
        <form @submit.prevent="updateDriveDetails">
            <div class="form-group">
                <label for="drive_type" class="form-label">Drive Type</label>
                <select id="drive_type" class="form-select" v-model="updateForm.drive_type">
                    <option v-for="type in driveTypes" :key="type" :value="type">{{ type }}</option>
                </select>
            </div>
            <div class="form-group flex gap-16">
                <div class="flex-1">
                    <label class="form-label" for="cgpa_requirement">Minimum CGPA Requirement</label>
                    <input id="cgpa_requirement" type="text" class="form-input" v-model="updateForm.cgpa_requirement">
                </div>
                <div class="flex-1">
                    <label class="form-label" for="application_deadline">Application Deadline</label>
                    <input id="cgpa_requirement" type="datetime-local" class="form-input" v-model="updateForm.application_deadline">
                </div>
            </div>
            <div class="form-group flex gap-16">
                <div class="flex-1">
                    <label class="form-label" for="salary_min">Minimum Salary (LPA)</label>
                    <input id="salary_min" type="text" class="form-input" v-model="updateForm.salary_min">
                </div>
                <div class="flex-1">
                    <label class="form-label" for="salary_max">Maximum Salary (LPA)</label>
                    <input id="salary_max" type="text" class="form-input" v-model="updateForm.salary_max">
                </div>
            </div>
            <button type="submit" class="btn is-primary full-width-btn">{{ saving ? 'Saving Changes...' : 'Save Changes' }}</button>
        </form>
    </AppModal>
    
</template>

<script setup>
import AppModal from '@/components/ui/AppModal.vue';
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { computed, onMounted, reactive, ref } from 'vue';

const notify = useNotificationStore();
const loading = ref(true);
const saving = ref(false);
const driveTypes = ref([]);

const properties = defineProps({
    modelValue: {
        type: Boolean,
        required: true
    },
    driveId: {
        type: Number,
        required: true
    },
    driveType: {
        type: String,
        required: true
    },
    cgpaRequirement: {
        type: Number,
        required: true
    },
    applicationDeadline: {
        type: String,
        required: true
    },
    salaryMin: {
        type: Number,
        required: false
    },
    salaryMax: {
        type: Number,
        required: true
    }
});

const emit = defineEmits([
    'update:modelValue',
    'updated'
]);

const modal = computed({
    get: () => properties.modelValue,
    set: value => emit('update:modelValue', value)
});

const updateForm = reactive({
    drive_type: properties.driveType,
    cgpa_requirement: properties.cgpaRequirement,
    application_deadline: properties.applicationDeadline,
    salary_min: properties.salaryMin,
    salary_max: properties.salaryMax
})

onMounted(fetchDriveTypes);

async function fetchDriveTypes() {
    loading.value = true;
    try {
        const result = await api.get('/shared/drive-types');
        driveTypes.value = result.data.drive_types;
        console.log(result.data);
    } catch (err) {
        notify.error(err.response?.data?.error || 'Failed to load drive types');
    } finally {
        loading.value = false;
    }
}

async function updateDriveDetails() {
    saving.value = true;
    try {
        await api.put(`/company/drives/${properties.driveId}`, updateForm);
        notify.success('Drive details have been updated successfully');
        emit('updated');
    } catch (err) {
        notify.error(err.response?.data?.error);
    } finally {
        saving.value = false;
        modal.value = false;
    }
}

</script>