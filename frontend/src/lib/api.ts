import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: { "Content-Type": "application/json" },
});

// ── Request interceptor: attach JWT ──
api.interceptors.request.use((config) => {
    if (typeof window !== "undefined") {
        const token = localStorage.getItem("access_token");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
    }
    return config;
});

// ── Response interceptor: redirect on 401 ──
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401 && typeof window !== "undefined") {
            // Don't redirect if already on auth pages
            if (
                !window.location.pathname.includes("/login") &&
                !window.location.pathname.includes("/register")
            ) {
                localStorage.removeItem("access_token");
                window.location.href = "/login";
            }
        }
        return Promise.reject(error);
    }
);

export default api;
