<template>

  <AppNotification />
  <AppDialog />

  <AppHeader 
    :sidebar-open="sidebarOpen"
    @toggle-sidebar="sidebarOpen = !sidebarOpen"
  />

  <AppSidebar
    v-if="authStore.isLoggedIn"
    :open="sidebarOpen"
  />

  <main 
    class="app-main"
    :class="{ 'sidebar-open': sidebarOpen && authStore.isLoggedIn, 'sidebar-line': authStore.isLoggedIn }">
    <router-view />
  </main>

  <AppFooter />
</template>

<script setup>
import AppNotification from './components/ui/AppNotification.vue'
import AppDialog from './components/ui/AppDialog.vue'
import AppHeader from './components/layout/AppHeader.vue';
import AppFooter from './components/layout/AppFooter.vue';
import AppSidebar from './components/layout/AppSidebar.vue';
import { useAuthStore } from './stores/auth.js';
import { ref } from 'vue';

const authStore = useAuthStore();
const sidebarOpen = ref(false);
</script>