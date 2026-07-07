import axios from "axios";

const api = axios.create({
    baseURL: 'http://localhost:8443/api',
    headers: {
        'Content-Type': 'application/json'
    }
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true
        
            const refreshToken = localStorage.getItem('refresh_token')
            if (refreshToken) {
                try {
                    const result = await axios.post(api.get('baseURL') + '/auth/refresh', {},
                        {
                            headers: {
                                Authorization: `Bearer ${refreshToken}`
                            }
                        });
                    const newToken = result.data.access_token;
                    localStorage.setItem('access_token', newToken);
                    originalRequest.headers.Authorization = `Bearer ${newToken}`;
                    return api(originalRequest);
                } catch (refreshError) {
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                    globalThis.location.href = '/login';
                    return Promise.reject(refreshError);
                }
            }
        }
        return Promise.reject(error);
    }
)

export default api;