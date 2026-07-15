<template>
<div class="loading-spinner"><div class="dots"></div></div>
</template>

<style scoped>
.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px;
}

.dots {
   width: 4.5px;
   height: 4.5px;
   border-radius: 50%;
   color: var(--accent-primary-background);
   box-shadow: 21.3px 0 0 7.8px, 42.6px 0 0 3.4px, 63.900000000000006px 0 0 0;
   transform: translateX(-42.6px);
   animation: dots-ijr34dmd 0.5s infinite alternate linear;
}

@keyframes dots-ijr34dmd {
   50% {
      box-shadow: 21.3px 0 0 3.4px, 42.6px 0 0 7.8px, 63.900000000000006px 0 0 3.4px;
   }

   100% {
      box-shadow: 21.3px 0 0 0, 42.6px 0 0 3.4px, 63.900000000000006px 0 0 7.8px;
   }
}

/* Referred from: https://10015.io/tools/css-loader-generator */
</style>