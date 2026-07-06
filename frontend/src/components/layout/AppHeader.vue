<template>
    <header class = "app-header">
        <div class = "header-left">
            <button class = "btn is-primary is-icon-only">
                <i class = "fas fa-bars"></i>
            </button>
            <router-link to = "/"  class = "header-logo">
                Placement Portal
            </router-link>
        </div>
        <div class = "header-right">
            <button class = "btn is-primary is-icon-only" @click = "toggleTheme()">
                <i :class = "isDark ? 'fas fa-sun' : 'fas fa-moon'"></i>
            </button>
        </div>
    </header>
</template>

<style scoped>
.app-header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: var(--header-height);
    background: var(--accent-primary-background);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0px 5px;
    z-index: var(--header-z);
}

.header-left {
    display: flex;
    align-items: center;
    gap: 12px;
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
}
</style>

<script setup>
import { useTheme } from '@/composables/useTheme';

const { isDark, toggleTheme } = useTheme()
</script>