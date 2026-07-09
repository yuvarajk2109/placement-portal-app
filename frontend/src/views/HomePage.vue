<template>
    <div class="mt-24 text-center">
        <h1 class="page-title text-center">Welcome to the Placement Portal</h1>        
    </div>
</template>

<script setup>
import { useDialogStore } from '@/stores/dialog'
import { useNotificationStore } from '@/stores/notification'

const dialog = useDialogStore()
const notify = useNotificationStore()
</script>