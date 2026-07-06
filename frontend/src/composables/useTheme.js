import { ref, watchEffect } from "vue";

const isDark = ref(localStorage.getItem('theme') === 'dark');

export function useTheme() {
    watchEffect(() => {
        document.documentElement.setAttribute('data-theme', isDark.value? 'dark' : 'light');
        localStorage.setItem('theme', isDark.value ? 'dark' : 'light');
    })

    function toggleTheme() {
        isDark.value = !isDark.value;
    }

    return {
        isDark,
        toggleTheme
    };
}
