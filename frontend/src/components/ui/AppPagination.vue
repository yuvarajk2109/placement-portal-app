<template>
    <div class="paginator" v-if="totalPages > 1">
        <div class="paginator-items">
            <AppTooltip :disabled="currentPage <= 1"  text="Go to Previous Page">
                <button 
                    class="btn is-tertiary is-icon-only" 
                    :disabled="currentPage <= 1" 
                    @click="changePage(currentPage - 1)"            >
                    <i class="fas fa-arrow-left"></i>
                </button>
            </AppTooltip>
            
            <span>Page {{ currentPage }} of {{ totalPages }}</span>
            
            <AppTooltip :disabled="currentPage >= totalPages" text="Go to Next Page">
                <button 
                    class="btn is-tertiary is-icon-only" 
                    :disabled="currentPage >= totalPages" 
                    @click="changePage(currentPage + 1)"            >
                    <i class="fas fa-arrow-right"></i>
                </button>
            </AppTooltip>
        </div>
    </div>
</template>

<style scoped>
.paginator {
  display: flex;
  justify-content: flex-end;
  width: 100%;
}

.paginator-items {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 16px;
  font-size: 13.5px;
}
</style>

<script setup>
import AppTooltip from './AppTooltip.vue';

const properties = defineProps({
    currentPage: {
        type: Number,
        required: true
    },
    totalPages: {
        type: Number,
        required: true
    }
})

const emit = defineEmits(['update:currentPage', 'page-change'])

function changePage(newPage) {
    if (newPage >= 1 && newPage <= properties.totalPages) {
        emit('update:currentPage', newPage)
        emit('page-change', newPage)
    }
}
</script>
