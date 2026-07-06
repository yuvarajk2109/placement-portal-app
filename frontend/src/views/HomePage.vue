<template>
    <div class = "home-page">
        <div class = "welcome-banner text-center">
            <h1 class = "welcome-text">
                Welcome to the Placement Portal
            </h1>
        </div>
    </div>
</template>

<style scoped>
.home-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: calc(var(--header-height) + 20px);
    min-height: calc(100vh - var(--header-height) - 60px);
}
</style>