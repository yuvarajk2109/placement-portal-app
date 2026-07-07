<template>
    <div class="notification-container">
        <div
        v-for="notification in notificationStore.notifications"
        :key="notification.id"
        class="notification-toast"
        :class="`is-${notification.type}`">
            <span>{{ notification.message }}</span>
            <button 
            class="btn is-transparent is-icon-only is-small close-btn" 
            :class="`is-${notification.type}`"
            @click="notificationStore.removeNotification(notification.id)">
                <i class="fas fa-times"></i>
            </button>
        </div>
    </div>
</template>

<style scoped>
.notification-container {
  position: fixed;
  top: calc(var(--header-height) + 12px);
  right: 16px;
  z-index: var(--notification-z);
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-width: 400px;
}

.notification-toast {
  padding: 12px 12px;
  border-radius: 8px;
  font-size: 13.5px;
  font-weight: 400;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  animation: slideInRight 0.25s ease-out;
}

.notification-toast.is-success {
  background: var(--status-success-container-bg);
  color: var(--status-success-container-fg);
  border: 1px solid var(--status-success-container-line);
}

.notification-toast.is-error {
  background: var(--status-error-container-bg);
  color: var(--status-error-container-fg);
  border: 1px solid var(--status-error-container-line);
}

.notification-toast.is-warning {
  background: var(--status-warning-container-bg);
  color: var(--status-warning-container-fg);
  border: 1px solid var(--status-warning-container-line);
}

.notification-toast.is-info {
  background: var(--status-info-container-bg);
  color: var(--status-info-container-fg);
  border: 1px solid var(--status-info-container-line);
}

.close-btn {
  margin-left: auto;
}

@keyframes slideInRight {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
</style>

<script setup>
import { useNotificationStore } from '@/stores/notification';

const notificationStore = useNotificationStore();
</script>