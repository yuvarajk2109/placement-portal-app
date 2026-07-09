<template>
<Teleport to="body">
    <div v-if="modelValue" class="modal-overlay" @click.self="close">
        <div class="modal-content app-modal">
            <div class="modal-header">
                <h2 class="modal_title"><slot name="title">Modal</slot></h2>
                <button class="btn is-secondary is-icon-only" @click="close">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
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
    min-width: 500px;
    max-width: 700px;
}
.modal-body {
    margin-top: 16px;
    max-height: 60vh;
    overflow-y: auto;
}
</style>

<script setup>
defineProps({
    modelValue: {
        type: Boolean,
        required: true
    }
});

const emit = defineEmits(['update:modelValue']);
function close() {
    emit('update:modelValue', false);
}
</script>