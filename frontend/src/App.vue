<script setup>
import AppNotification from './components/ui/AppNotification.vue'
import AppHeader from './components/layout/AppHeader.vue';
import AppFooter from './components/layout/AppFooter.vue';

</script>

<template>

  <AppNotification />

  <AppHeader />

  <main class="app-main">
    <router-view />
  </main>

  <AppFooter />
</template>