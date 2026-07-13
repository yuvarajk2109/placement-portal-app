<template>
    <AppModal v-model="modal" size="small"> 
        <template #title>Edit Required Skills</template>
        <form @submit.prevent="updateRequiredSkills">
            <div class="form-group">
                <AppMultiSelect
                    v-model="updateForm.skill_ids"
                    :options="allSkills"
                    value="skill_name"
                    id="skill_id"
                />
            </div>
            <button type="submit" class="btn is-primary full-width-btn" :disabled="saving">{{ saving ? 'Saving Changes...' : 'Save Changes' }}</button>
        </form>
    </AppModal>
</template>

<script setup>
import AppModal from '@/components/ui/AppModal.vue';
import AppMultiSelect from '@/components/ui/AppMultiSelect.vue';
import api from '@/services/api';
import { useNotificationStore } from '@/stores/notification';
import { computed, onMounted, reactive, ref } from 'vue';

const notify = useNotificationStore();
const loading = ref(true);
const saving = ref(false);
const allSkills = ref([]);

const properties = defineProps({
    modelValue: {
        type: Boolean,
        required: true
    },
    driveId: {
        type: Number,
        required: true
    },
    requiredSkills: {
        type: Array,
        required: true
    }
})

const updateForm = reactive({
    skill_ids: properties.requiredSkills.map(skill => skill.skill_id)
});

const emit = defineEmits([
    'update:modelValue',
    'updated'
]);

const modal = computed({
    get: () => properties.modelValue,
    set: value => emit('update:modelValue', value)
});

onMounted(fetchEligibleBranches);

async function fetchEligibleBranches() {
    loading.value = true;
    try {
        const result = await api.get('/shared/skills');
        allSkills.value = result.data.skills;
    } catch (err) {
        notify.error(err.response?.data?.error);
    } finally {
        loading.value = false;
    }
}

async function updateRequiredSkills() {
    saving.value = true;
    try {
        const result = await api.put(`/company/drives/${properties.driveId}`, updateForm);
        notify.success(result.data.message || 'Required skills have been updated successfully. Drive requires admin approval.');
        emit('updated');
    } catch (err) {
        notify.error(err.response?.data?.error);
    } finally {
        saving.value = false;
        modal.value = false;
    }
}

</script>