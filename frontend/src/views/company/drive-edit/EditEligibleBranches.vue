<template>
    <AppModal v-model="modal" size="small"> 
        <template #title>Edit Eligible Branches</template>
        <form @submit.prevent="updateEligibleBranches">
            <div class="form-group">
                <AppMultiSelect
                    v-model="updateForm.eligible_branch_ids"
                    :options="allBranches"
                    value="branch_name"
                    id="branch_id"
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
const allBranches = ref([]);

const properties = defineProps({
    modelValue: {
        type: Boolean,
        required: true
    },
    driveId: {
        type: Number,
        required: true
    },
    eligibleBranches: {
        type: Array,
        required: true
    }
})

const updateForm = reactive({
    eligible_branch_ids: properties.eligibleBranches.map(branch => branch.branch_id)
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
        const result = await api.get('/shared/branches');
        allBranches.value = result.data.branches;
    } catch (err) {
        notify.error(err.response?.data?.error);
    } finally {
        loading.value = false;
    }
}

async function updateEligibleBranches() {
    saving.value = true;
    try {
        const result = await api.put(`/company/drives/${properties.driveId}`, updateForm);
        notify.success(result.data.message || 'Eligible branches have been updated successfully. Drive requires admin approval.');
        emit('updated');
    } catch (err) {
        notify.error(err.response?.data?.error);
    } finally {
        saving.value = false;
        modal.value = false;
    }
}

</script>