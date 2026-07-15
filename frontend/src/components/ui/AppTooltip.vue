<template>
  <div 
    class="app-tooltip-wrapper" 
    :class="{ 'is-block': block }"
    @mouseenter="show = true" 
    @mouseleave="show = false">
    <div class="tooltip-anchor" :style="{ anchorName: anchorId }">
      <slot></slot>
    </div>
    
    <div 
      v-show="show && !disabled" 
      class="tooltip-content" :style="{ positionAnchor: anchorId }"
      :data-position="position">
      <slot name="content">{{ text }}</slot>
    </div>
  </div>
</template>

<style scoped>
.app-tooltip-wrapper {
  display: inline-flex;
}

.app-tooltip-wrapper.is-block {
  display: block;
}

.app-tooltip-wrapper.is-block .tooltip-anchor {
  display: block;
}

.tooltip-anchor {
  display: inherit;
}

.tooltip-content {  
  position: fixed;  
  background: var(--surface-background-bright);
  color: var(--surface-foreground);
  border: 1px solid var(--surface-line-subtle);
  border-radius: 10px;
  padding: 8px 8px;
  font-size: 12px;
  font-weight: 500;
  z-index: 9999;
  max-width: 1000px;
  text-align: center;
  pointer-events: none;
}

.tooltip-content[data-position="top"] {
    position-area: top;
    transform: translateY(-8px);
}

.tooltip-content[data-position="bottom"] {
    position-area: bottom;
    transform: translateY(8px);
}

.tooltip-content[data-position="left"] {
    position-area: left;
    transform: translateX(-8px);
}

.tooltip-content[data-position="right"] {
    position-area: right;
    transform: translateX(8px);
}

/* Referred from: https://css-tip.com/tooltip-anchor/ */
</style>

<script setup>
import { ref } from 'vue';

const anchorId = `--tooltip-${Math.random().toString(36).slice(2)}`;

const props = defineProps({
  text: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  position: {
    type: String,
    default: 'top' // top, right, bottom, left
  },
  block: {
    type: Boolean,
    default: false // if true, the wrapper uses display: block instead of inline-flex
  }
});

const show = ref(false);
</script>