<template>
    <footer class="app-footer">
        <span class="footer-content">
            Placement Portal            
        </span>
        <span class="footer-content">
            &copy; 2026. All Rights Reserved.           
        </span>
    </footer>
</template>

<style scoped>
.app-footer {
    position: sticky;
    display: flex;
    flex-direction: column;
    justify-content: center;      
    gap: 4px;                  

    height: var(--footer-height);

    font-size: 16px;
    color: var(--accent-primary-foreground);
    border-top: 1px solid var(--surface-line);
    background: var(--accent-primary-background);
}

.footer-content {
    text-align: right;
    margin: 0 16px;
}
</style>