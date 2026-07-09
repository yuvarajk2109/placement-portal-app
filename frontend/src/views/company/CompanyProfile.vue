<template>
    <div class="main-page">
       <h1 class="page-title text-center">Company Profile</h1>
       <!-- <AppSpinner v-if="loading" /> -->
       <div class="card">
            <form>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="company_name">Company Name</label>
                        <input id="company_name" class="form-input">
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="industry">Industry</label>
                        <input id="industry" class="form-input">
                    </div>
                </div>
                <div class="form-group flex gap-16">
                    <div class="flex-1">
                        <label class="form-label" for="website">Website URL</label>
                        <input id="website" class="form-input">
                    </div>
                    <div class="flex-1">
                        <label class="form-label" for="location">Location</label>
                        <input id="location" class="form-input">
                    </div>
                </div>
            </form>
       </div>
    </div>
</template>

<style scoped>
.card {
    max-width: 800px;
    margin: auto;
}
</style>

<script setup>
import AppSpinner from '@/components/ui/AppSpinner.vue';


</script>