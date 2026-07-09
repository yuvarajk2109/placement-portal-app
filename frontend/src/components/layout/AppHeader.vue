<template>
    <header class="app-header">
        <div class="header-left">
            <button 
            class="btn is-primary is-icon-only"
            @click="$emit('toggle-sidebar')">
                <i class="fas fa-bars"></i>
            </button>
            <router-link to="/"  class="header-logo">
                Placement Portal
            </router-link>
        </div>
        <div class="header-right">
            <button class="btn is-primary is-icon-only" @click="toggleTheme()">
                <i :class="isDark ? 'fas fa-sun' : 'fas fa-moon'"></i>
            </button>

            <template v-if="authStore.isLoggedIn">
                <button 
                class="btn is-error"
                @click="handleLogout">
                    Logout
                </button>
            </template>
            <template v-else>
                <router-link 
                to="/login"
                class="btn is-inverse">
                    Login
                </router-link>
                <router-link 
                to="/verify-otp"
                class="btn is-inverse">
                    Verify OTP
                </router-link>
                <router-link 
                to="/register/student"
                class="btn is-inverse">
                    Register as Student
                </router-link>
                <router-link
                to="/register/company"
                class="btn is-inverse">
                    Register as Company
                </router-link>
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
import { useRouter } from 'vue-router';

const authStore=useAuthStore();
const router=useRouter();

const { isDark, toggleTheme }=useTheme();
defineEmits(['toggle-sidebar']);

function handleLogout() {
    authStore.logout();
    router.push({ name: 'login' });
}
</script>