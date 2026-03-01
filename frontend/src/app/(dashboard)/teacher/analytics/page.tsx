"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import api from "@/lib/api";

interface AnalyticsData {
    [key: string]: unknown;
}

export default function AnalyticsPage() {
    const { user } = useAuth();
    const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
    const [weakConcepts, setWeakConcepts] = useState<unknown[]>([]);
    const [threshold, setThreshold] = useState("0.5");
    const [loading, setLoading] = useState(true);

    const fetchData = (t: string) => {
        if (!user) return;
        const tid = user.id;
        setLoading(true);
        Promise.allSettled([
            api.get(`/teachers/${tid}/analytics`),
            api.get(`/teachers/${tid}/students/weak-concepts?threshold=${t}`),
        ]).then(([aRes, wRes]) => {
            if (aRes.status === "fulfilled") setAnalytics(aRes.value.data);
            if (wRes.status === "fulfilled") setWeakConcepts(wRes.value.data as unknown[]);
            setLoading(false);
        });
    };

    useEffect(() => {
        fetchData(threshold);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [user]);

    const handleThresholdChange = () => fetchData(threshold);

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
                <h1 className="text-2xl font-bold text-white">Analytics</h1>
                <p className="mt-1 text-sm text-gray-400">
                    Detailed analytics and weak concept analysis across all your students.
                </p>
            </div>

            {/* Threshold control */}
            <div className="glass-card max-w-md p-5">
                <h3 className="mb-3 text-sm font-semibold text-gray-400">Weak Concept Threshold</h3>
                <div className="flex items-end gap-3">
                    <div className="flex-1">
                        <input
                            type="range"
                            min={0}
                            max={1}
                            step={0.05}
                            value={threshold}
                            onChange={(e) => setThreshold(e.target.value)}
                            className="w-full accent-indigo-500"
                        />
                        <div className="mt-1 flex justify-between text-xs text-gray-500">
                            <span>0%</span>
                            <span className="font-medium text-indigo-400">
                                {(Number(threshold) * 100).toFixed(0)}%
                            </span>
                            <span>100%</span>
                        </div>
                    </div>
                    <button
                        onClick={handleThresholdChange}
                        className="rounded-lg border border-white/10 px-4 py-2 text-sm text-gray-300 transition-colors hover:bg-white/[0.04]"
                    >
                        Apply
                    </button>
                </div>
            </div>

            {/* Analytics */}
            {analytics && (
                <div className="glass-card p-6">
                    <h2 className="mb-4 text-lg font-semibold text-white">Teacher Analytics</h2>
                    <pre className="max-h-96 overflow-auto rounded-lg bg-white/[0.02] p-4 text-sm text-gray-300">
                        {JSON.stringify(analytics, null, 2)}
                    </pre>
                </div>
            )}

            {/* Weak concepts */}
            <div className="glass-card p-6">
                <h2 className="mb-4 text-lg font-semibold text-white">
                    Weak Concepts (threshold: {(Number(threshold) * 100).toFixed(0)}%)
                </h2>
                {Array.isArray(weakConcepts) && weakConcepts.length > 0 ? (
                    <pre className="max-h-96 overflow-auto rounded-lg bg-white/[0.02] p-4 text-sm text-gray-300">
                        {JSON.stringify(weakConcepts, null, 2)}
                    </pre>
                ) : (
                    <p className="text-sm text-gray-500">
                        No weak concepts found at this threshold.
                    </p>
                )}
            </div>
        </div>
    );
}
