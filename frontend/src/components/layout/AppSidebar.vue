<template>
    <aside class="sidebar" :class="{ 'is-open': open }">
        <nav class="sidebar-nav">
            <router-link
                v-for="item in menuItems"
                :key="item.route"
                :to="{ name: item.route }"
                class="sidebar-link"
                :class="{ active: $route.name === item.route }"
                :title="!open ? item.label : undefined">
                <i :class="item.icon"></i>
                <span 
                    v-if="open"
                    class="sidebar-link-text">
                    {{ item.label }}
                </span>
            </router-link>
        </nav>
    </aside>
</template>

<style scoped>
.sidebar {
    position: fixed;
    top: var(--header-height);
    left: 0;
    bottom: var(--footer-height);
    width: var(--sidebar-width-closed);
    background: var(--surface-background);
    border-right: 2px solid var(--surface-line-subtle);
    z-index: var(--sidebar-z);
    transition: width 0.25s ease;
    overflow: hidden;
}

.sidebar.is-open {
    width: var(--sidebar-width-open);
}

.sidebar-nav {
    display: flex;
    flex-direction: column;
    padding: 12px 8px;
    gap: 4px;
}

.sidebar-link {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 16px;
    border-radius: 8px;
    color: var(--surface-foreground);
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
    transition: background 0.15s ease, color 0.15s ease;
    white-space: nowrap;
}

.sidebar-link i {
    width: 20px;
    text-align: left;
    font-size: 16px;
    flex-shrink: 0
}

.sidebar-link:hover,
.sidebar-link.active {
    background: var(--accent-primary-background);
    color: var(--accent-primary-foreground);
}
</style>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { computed } from 'vue';

const properties=defineProps({
    open: {
        type: Boolean,
        default: false
    }
});
const authStore=useAuthStore();

const menuItems=computed(() => {
    const role=authStore.userRole;
    if (role === 'admin') {
        return [
            { 
                route: 'admin-dashboard',
                icon: 'fas fa-chart-line',
                label: 'Dashboard'
            },
            { 
                route: 'admin-companies',
                icon: 'fas fa-building',
                label: 'Companies'
            },
            { 
                route: 'admin-drives',
                icon: 'fas fa-briefcase',
                label: 'Drives'
            },
            { 
                route: 'admin-students',
                icon: 'fas fa-user-graduate',
                label: 'Students'
            },
            { 
                route: 'admin-applications',
                icon: 'fas fa-file-alt',
                label: 'Applications'
            },
            { 
                route: 'admin-placements',
                icon: 'fas fa-trophy',
                label: 'Placements'
            },
        ]
    }
    return [];
})
</script>