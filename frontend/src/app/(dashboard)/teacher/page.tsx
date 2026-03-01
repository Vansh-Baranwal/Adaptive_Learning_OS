"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import api from "@/lib/api";

interface AnalyticsData {
    [key: string]: unknown;
}

export default function TeacherDashboard() {
    const { user } = useAuth();
    const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
    const [weakConcepts, setWeakConcepts] = useState<unknown[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!user) return;
        const tid = user.id;
        Promise.allSettled([
            api.get(`/teachers/${tid}/analytics`),
            api.get(`/teachers/${tid}/students/weak-concepts?threshold=0.5`),
        ]).then(([aRes, wRes]) => {
            if (aRes.status === "fulfilled") setAnalytics(aRes.value.data);
            if (wRes.status === "fulfilled") setWeakConcepts(wRes.value.data as unknown[]);
            setLoading(false);
        });
    }, [user]);

    if (loading) {
        return (
            <div className="flex h-64 items-center justify-center">
                <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent" />
            </div>
        );
    }

    return (
        <div className="animate-fade-in space-y-8">
            <div>
                <h1 className="text-2xl font-bold text-white">Teacher Dashboard</h1>
                <p className="mt-1 text-sm text-gray-400">
                    Overview of student performance and analytics.
                </p>
            </div>

            {/* Quick stats */}
            <div className="stagger grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
                <div className="animate-slide-up glass-card glass-card-hover border border-indigo-500/20 bg-gradient-to-br from-indigo-500/20 to-violet-500/20 p-5">
                    <div className="flex items-center justify-between">
                        <p className="text-sm font-medium text-gray-400">Analytics Loaded</p>
                        <span className="text-xl">📊</span>
                    </div>
                    <p className="mt-2 text-3xl font-bold text-white">
                        {analytics ? "Yes" : "No Data"}
                    </p>
                </div>
                <div className="animate-slide-up glass-card glass-card-hover border border-amber-500/20 bg-gradient-to-br from-amber-500/20 to-orange-500/20 p-5">
                    <div className="flex items-center justify-between">
                        <p className="text-sm font-medium text-gray-400">Weak Concepts Found</p>
                        <span className="text-xl">⚠️</span>
                    </div>
                    <p className="mt-2 text-3xl font-bold text-white">
                        {Array.isArray(weakConcepts) ? weakConcepts.length : 0}
                    </p>
                </div>
                <div className="animate-slide-up glass-card glass-card-hover border border-emerald-500/20 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 p-5">
                    <div className="flex items-center justify-between">
                        <p className="text-sm font-medium text-gray-400">Role</p>
                        <span className="text-xl">👨‍🏫</span>
                    </div>
                    <p className="mt-2 text-3xl font-bold capitalize text-white">
                        {user?.role}
                    </p>
                </div>
            </div>

            {/* Analytics raw data */}
            {analytics && (
                <div className="glass-card p-6">
                    <h2 className="mb-4 text-lg font-semibold text-white">Analytics Data</h2>
                    <pre className="max-h-80 overflow-auto rounded-lg bg-white/[0.02] p-4 text-sm text-gray-300">
                        {JSON.stringify(analytics, null, 2)}
                    </pre>
                </div>
            )}

            {/* Weak concepts */}
            {Array.isArray(weakConcepts) && weakConcepts.length > 0 && (
                <div className="glass-card p-6">
                    <h2 className="mb-4 text-lg font-semibold text-white">
                        Students&apos; Weak Concepts
                    </h2>
                    <pre className="max-h-80 overflow-auto rounded-lg bg-white/[0.02] p-4 text-sm text-gray-300">
                        {JSON.stringify(weakConcepts, null, 2)}
                    </pre>
                </div>
            )}
        </div>
    );
}
