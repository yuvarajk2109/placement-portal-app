<template>
<div v-if="dialog.isOpen" class="modal-overlay" @click.self="dialog.cancel()">
    <div class="modal-content dialog-modal" :class="`is-${dialog.options.type}`">
        <div class="modal-header">
            <h2 class="modal-title flex items-center gap-8">
                <i v-if="dialog.options.type === 'warning'" class="fas fa-exclamation-triangle"></i>
                <i v-else-if="dialog.options.type === 'error'" class="fas fa-times-circle"></i>
                <i v-else-if="dialog.options.type === 'success'" class="fas fa-check-circle"></i>
                <i v-else class="fas fa-info-circle"></i>
                {{ dialog.options.title }}
            </h2>
            <button class="btn is-secondary is-icon-only" @click="dialog.cancel()"><i class="fas fa-times"></i></button>
        </div> 
        <div class="modal-body">
            {{ dialog.options.message }}
        </div>
        <div class="modal-footer">
            <button class="btn is-secondary" @click="dialog.cancel()">
                    {{ dialog.options.cancelText }}
                </button>
                <button class="btn" :class="confirmButtonClass" @click="dialog.proceed()">
                    {{ dialog.options.confirmText }}
                </button>
            </div>
        </div>           
    </div>
</template>

<style scoped>
.dialog-modal {
    max-width: 450px;
}
.dialog-modal.is-warning .modal-title {
    color: var(--status-warning-container-fg);
}
.dialog-modal.is-error .modal-title {
    color: var(--status-error-container-fg);
}
.dialog-modal.is-info .modal-title {
    color: var(--status-info-container-fg);
}
.dialog-modal.is-success .modal-title {
    color: var(--status-success-container-fg);
}
</style>

<script setup>
import { useDialogStore } from '@/stores/dialog';
import { computed } from 'vue';

const dialog = useDialogStore();

const confirmButtonClass = computed(() => {
    switch(dialog.options.type) {
        case 'error': return 'is-error'
        case 'warning': return 'is-warning'
        case 'success': return 'is-success'
        default: return 'is-info'
    }
})
</script>