<template>
    <div class="multiselect-container">
        <button 
            type="button" 
            v-for="option in options" 
            :key="option[id]" 
            class="btn is-small is-readonly" 
            :class="
                properties.readonly
                ? 'is-primary'
                : (isSelected(option) ? 'is-primary' : 'is-secondary')"
            @click="toggleSelection(option)">
            {{ option[value] }}
        </button>
    </div>
</template>

<style scoped>
.multiselect-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.is-readonly {
    cursor: default;
}

.is-readonly:hover {
    transform: translateY(-1px);
}
</style>

<script setup>
const properties = defineProps({
    modelValue: {
        type: Array,
        required: true
    },
    options: {
        type: Array,
        required: true
    },
    value: {
        type: String,
        required: true
    },
    id: {
        type: String,
        required: true
    },
    readonly: {
        type: Boolean,
        default: false
    }
});

const emit = defineEmits(['update:modelValue', 'blur']);

function isSelected(option) {
    return properties.modelValue.includes(option[properties.id]);
}

function toggleSelection(option) {
    if (properties.readonly) return;

    const id = option[properties.id];
    const index = properties.modelValue.indexOf(id);
    const newIds = [...properties.modelValue];

    if (index === -1) {
        newIds.push(id);
    } else {
        newIds.splice(index, 1);
    }

    emit('update:modelValue', newIds);
    emit('blur');
}
</script>