<template>
<Teleport to="body">
    <div v-if="modelValue" class="modal-overlay">
        <div class="modal-content app-modal" :class="`is-${size}`">
            <div class="modal-header">
                <h2 class="modal-title"><slot name="title">Modal</slot></h2>
                <button class="btn is-secondary is-icon-only" @click="close">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body" :class="{ 'footer-border' : $slots.footer }"> 
                <slot></slot>
            </div>
            <div class="modal-footer" v-if="$slots.footer">
                <slot name="footer"></slot>
            </div>
        </div>
    </div>
</Teleport>
</template>

<style scoped>
.app-modal {
    width: 1000px;
    max-width: 1000px;
}

.app-modal.is-small {
    width: 500px;
}

.app-modal.is-medium {
    width: 750px;
}

.modal-body {
    padding: 12px 20px;
    max-height: 60vh;
    overflow-y: auto;
}

.modal-body.footer-border {
  border-bottom: 1px solid var(--surface-line-subtle);
}
</style>

<script setup>
defineProps({
    modelValue: {
        type: Boolean,
        required: true
    },
    size: {
        type: String,
        required: false,
        default: 'large',
        validator: value => ['small', 'medium', 'large'].includes(value)
    }
});

const emit = defineEmits(['update:modelValue']);
function close() {
    emit('update:modelValue', false);
}
</script>