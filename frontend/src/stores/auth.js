import api from "@/services/api";
import { defineStore } from "pinia"
import { computed, ref } from "vue"


export const useAuthStore = defineStore('auth', () => {
    const user = ref(null);
    const accessToken = ref(localStorage.getItem('access_token') || null);
    const refreshToken = ref(localStorage.getItem('refresh_token') || null);
    const loading = ref(false);

    const isLoggedIn = computed(() => !!accessToken.value);
    const userRole = computed(() => user.value?.role || null);
    const userName = computed(() => {
        if (!user.value) return ''
        if (user.value.role === 'student' && user.value.profile) {
            return user.value.profile.name;
        }
        if (user.value.role === 'company' && user.value.profile) {
            return user.value.profile.company_name;
        }
        if (user.value.role === 'admin') {
            return 'Admin';
        }
        return user.value.email;
    })

    async function login(email, password) {
        try {
            const result = await api.post('/auth/login', { email, password });
            accessToken.value = result.data.access_token;
            refreshToken.value = result.data.refresh_token;
            localStorage.setItem('access_token', result.data.access_token);
            localStorage.setItem('refresh_token', result.data.refresh_token);
            user.value = result.data.user;
            await fetchProfile();
            return {
                success: true
            };
        } catch (err) {
            return {
                success: false,
                error: err.response?.data?.error || 'Login Failed'
            };
        } finally {
            loading.value = false;
        }
    }

    async function fetchProfile() {
        try {
            const result = await api.get('/auth/profile');
            user.value = result.data;
        } catch (err) {
            if (err.response?.status === 401) {
                logout();
            }
        }
    }

    async function logout() {
        user.value = null;
        accessToken.value = null;
        refreshToken.value = null;
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    }

    if (accessToken.value) {
        fetchProfile();
    }

    return {
        user,
        accessToken,
        refreshToken,
        loading,
        isLoggedIn,
        userRole,
        userName,
        login,
        fetchProfile,
        logout
    };
})