<template>
    <div class="page-title">Welcome, Admin</div>

    <div v-if="loading" class="loading-spinner">
        <div class="spinner"></div>
    </div>
    <div v-else class="stats-grid">
        <div class="stat-card">
            <div class="stat-card-value">

            </div>
            <div class="stat-card-label">

            </div>
        </div>
        <div class="stat-card">
            <div class="stat-card-value">

            </div>
            <div class="stat-card-label">
                
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-card-value">

            </div>
            <div class="stat-card-label">
                
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-card-value">

            </div>
            <div class="stat-card-label">
                
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-card-value">

            </div>
            <div class="stat-card-label">
                
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-card-value">

            </div>
            <div class="stat-card-label">
                
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-card-value">

            </div>
            <div class="stat-card-label">
                
            </div>
        </div>
    </div>
</template>

<script setup>
import { useNotificationStore } from '@/stores/notification';

const notify = useNotificationStore();
</script>