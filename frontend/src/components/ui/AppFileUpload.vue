<template>
    <div class="file-upload">
        <input
            ref="fileInput"
            type="file"
            class="hidden-input"
            :accept="accept"
            :disabled="disabled"
            @change="handleChange">

        <div class="form-input file-display" :class="{ disabled }">
            <span class="file-name">
                {{ fileName || placeholder }}
            </span>

            <div class="file-actions">
                <button type="button" class="btn is-primary" :disabled="disabled" @click="browse">
                    <i class="fas fa-upload"></i>
                    {{ modelValue ? 'Change' : 'Browse' }}
                </button>

                <a v-if="file && !modelValue" target="_blank" class="btn is-secondary" @click="$emit('download')">
                    <i class="fas fa-download"></i>
                    Download
                </a>

                <button v-if="modelValue" type="button" class="btn is-secondary is-icon-only" @click="clear">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
        <p v-if="hint" class="form-hint">
            {{ hint }}
        </p>
    </div>
</template>

<style scoped>
.hidden-input {
    display: none;
}

.file-display {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 30px 10px;
    gap: 12px;
}

.file-name {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: var(--surface-foreground);
}

.file-actions {
    display: flex;
    gap: 8px;
    flex-shrink: 0;
}

.file-display.disabled {
    background: var(--surface-background);
    cursor: not-allowed;
}
</style>

<script setup>
import { computed, ref } from 'vue';

const properties = defineProps({
    modelValue: {
        type: File,
        default: null
    },
    downloadUrl: {
        type: String,
        default: ''
    },
    file: {
        type: String,
        default: ''
    },
    accept: {
        type: String,
        default: ''
    },
    placeholder: {
        type: String,
        default: 'No file selected'
    },
    hint: {
        type: String,
        default: ''
    },
    disabled: {
        type: Boolean,
        default: false
    }
});

const emit = defineEmits(['update:modelValue', 'download']);

const fileInput = ref(null);

const fileName = computed(() => {
    if (properties.modelValue) return properties.modelValue.name;
    return properties.file;
});

function browse() {
    if (properties.disabled) return;
    fileInput.value.click();
}

function handleChange(event) {
    const file = event.target.files[0] || null;
    emit('update:modelValue', file);
}

function clear() {
    emit('update:modelValue', null);

    if (fileInput.value) {
        fileInput.value.value = '';
    }
}
</script>