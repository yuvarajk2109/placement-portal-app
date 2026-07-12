<template>
    <div class="paginator" v-if="totalPages > 1">
        <div class="paginator-items">
            <button 
                class="btn is-tertiary is-icon-only" 
                :disabled="currentPage <= 1" 
                @click="changePage(currentPage - 1)"
            >
                <i class="fa-solid fa-arrow-left"></i>
            </button>
            
            <span>Page {{ currentPage }} of {{ totalPages }}</span>
            
            <button 
                class="btn is-tertiary is-icon-only" 
                :disabled="currentPage >= totalPages" 
                @click="changePage(currentPage + 1)"
            >
                <i class="fa-solid fa-arrow-right"></i>
            </button>
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
