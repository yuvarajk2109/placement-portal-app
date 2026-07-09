import { defineStore } from "pinia";
import { ref } from "vue";

export const useDialogStore = defineStore('dialog', () => {
    const isOpen = ref(false);
    const options = ref({});
    let resolvePromise = null;

    function confirm(config) {
        options.value = {
            title: config.title || 'Confirm',
            message: config.message || 'Are you sure?',
            type: config.type || 'info',
            confirmText: config.confirmText || 'Yes',
            cancelText: config.cancelText || 'No'
        };
        isOpen.value = true;
        return new Promise((resolve) => {
            resolvePromise = resolve;
        })
    }

    function proceed() {
        isOpen.value = false;
        if (resolvePromise) resolvePromise(true);
    }

    function cancel() {
        isOpen.value = false;
        if (resolvePromise) resolvePromise(false);
    }

    return {
        isOpen,
        options,
        confirm,
        proceed,
        cancel
    }
})