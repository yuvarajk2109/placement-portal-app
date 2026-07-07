import { defineStore } from "pinia";
import { ref } from "vue";

export const useNotificationStore = defineStore('notification', () => {
    const notifications = ref([]);
    let nextId = 0;

    function addNotification(message, type = 'info', duration = 5000) {
        const id = nextId++;
        notifications.value.push({id, message, type});
        if (duration > 0) {
            setTimeout(() => {
                removeNotification(id);
            }, duration)
        }
    }

    function removeNotification(id) {
        notifications.value = notifications.value.filter(n => n.id != id);
    }

    function success(message) {
        addNotification(message, 'success');
    }

    function error(message) {
        addNotification(message, 'error');
    }

    function warning(message) {
        addNotification(message, 'warning');
    }

    function info(message) {
        addNotification(message, 'info');
    }

    return {
        notifications,
        addNotification,
        removeNotification,
        success,
        error,
        warning,
        info
    };
})