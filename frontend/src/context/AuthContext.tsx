"use client";

import React, { createContext, useContext, useEffect, useState, useCallback } from "react";
import api from "@/lib/api";
import type { UserResponse, UserCreate, Token } from "@/types";

interface AuthContextType {
    user: UserResponse | null;
    token: string | null;
    loading: boolean;
    isAuthenticated: boolean;
    login: (email: string, password: string) => Promise<void>;
    register: (data: UserCreate) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<UserResponse | null>(null);
    const [token, setToken] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);

    // Hydrate user on mount
    useEffect(() => {
        const storedToken = localStorage.getItem("access_token");
        if (storedToken) {
            setToken(storedToken);
            api
                .get<UserResponse>("/auth/me")
                .then((res) => setUser(res.data))
                .catch(() => {
                    localStorage.removeItem("access_token");
                    setToken(null);
                })
                .finally(() => setLoading(false));
        } else {
            setLoading(false);
        }
    }, []);

    const login = useCallback(async (email: string, password: string) => {
        // Backend uses OAuth2PasswordRequestForm → send form-data
        const params = new URLSearchParams();
        params.append("username", email);
        params.append("password", password);

        const { data } = await api.post<Token>("/auth/login", params, {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
        });

        localStorage.setItem("access_token", data.access_token);
        setToken(data.access_token);

        // Fetch user profile
        const meRes = await api.get<UserResponse>("/auth/me", {
            headers: { Authorization: `Bearer ${data.access_token}` },
        });
        setUser(meRes.data);
    }, []);

    const register = useCallback(async (data: UserCreate) => {
        await api.post<UserResponse>("/auth/register", data);
    }, []);

    const logout = useCallback(() => {
        localStorage.removeItem("access_token");
        setToken(null);
        setUser(null);
        window.location.href = "/login";
    }, []);

    return (
        <AuthContext.Provider
            value={{
                user,
                token,
                loading,
                isAuthenticated: !!token && !!user,
                login,
                register,
                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error("useAuth must be used within AuthProvider");
    return ctx;
}
