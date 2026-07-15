<template>
    <header class="app-header">
        <div class="header-left">
            <AppTooltip v-if="authStore.isLoggedIn" position = "right" text="Toggle Sidebar">
                <button v-if="authStore.isLoggedIn" class="btn is-primary is-icon-only" @click="$emit('toggle-sidebar')">
                    <i class="fas fa-bars"></i>
                </button>
            </AppTooltip>
            <AppTooltip v-else position = "bottom" text="Go to Home Page">
                <button  class="btn is-primary is-icon-only" @click="router.push({ name: 'home'})">
                    <i class="fas fa-home"></i>
                </button>
            </AppTooltip>
            
            <router-link to="/"  class="header-logo">
                Placement Portal
            </router-link>
        </div>
        <div class="header-right">
            <AppTooltip :text="isDark? 'Light Mode' : 'Dark Mode'" position = "bottom">
                <button class="btn is-primary is-icon-only" @click="toggleTheme()">
                    <i :class="isDark ? 'fas fa-sun' : 'fas fa-moon'"></i>
                </button>
            </AppTooltip>

            <template v-if="authStore.isLoggedIn">
                <AppTooltip
                    text="Logout" position="bottom">
                    <button 
                    class="btn is-icon-only is-error"
                    @click="handleLogout">
                        <i class="fa-solid fa-power-off"></i>
                    </button>
                </AppTooltip>
                
            </template>
        </div>
    </header>
</template>

<style scoped>
.app-header {
    position: sticky;
    top: 0;
    left: 0;
    right: 0;
    height: var(--header-height);
    background: var(--accent-primary-background);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0px 5px;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-left: 8px;
}

.header-logo {
    font-size: 18px;
    font-weight: 700;
    color: var(--accent-primary-foreground);
    text-decoration: none;
}

.header-right {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-right: 16px;
}
</style>

<script setup>
import { useTheme } from '@/composables/useTheme';
import { useAuthStore } from '@/stores/auth';
import { useNotificationStore } from '@/stores/notification';
import { useRouter } from 'vue-router';
import AppTooltip from '../ui/AppTooltip.vue';

const authStore = useAuthStore();
const notify = useNotificationStore();
const router = useRouter();

const { isDark, toggleTheme }=useTheme();
defineEmits(['toggle-sidebar']);

function handleLogout() {
    authStore.logout();
    notify.success("Logout successful");
    router.push({ name: 'home' });
}
</script>