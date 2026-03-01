"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import api from "@/lib/api";
import type { MasteryResponse, AttemptResponse } from "@/types";

/* ── helper: mastery color ── */
function masteryColor(p: number) {
    if (p >= 0.8) return "from-emerald-500 to-teal-500";
    if (p >= 0.5) return "from-amber-500 to-orange-500";
    return "from-red-500 to-rose-500";
}

function masteryLabel(p: number) {
    if (p >= 0.8) return "Mastered";
    if (p >= 0.5) return "In Progress";
    return "Needs Work";
}

export default function StudentDashboard() {
    const { user } = useAuth();
    const [mastery, setMastery] = useState<MasteryResponse[]>([]);
    const [attempts, setAttempts] = useState<AttemptResponse[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!user) return;
        const studentId = user.id; // user_id maps to student lookup in backend
        Promise.allSettled([
            api.get<MasteryResponse[]>(`/students/${studentId}/mastery`),
            api.get<AttemptResponse[]>(`/students/${studentId}/attempts`),
        ]).then(([mRes, aRes]) => {
            if (mRes.status === "fulfilled") setMastery(mRes.value.data);
            if (aRes.status === "fulfilled") setAttempts(aRes.value.data);
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

    const avgMastery = mastery.length
        ? mastery.reduce((a, m) => a + m.p_l, 0) / mastery.length
        : 0;
    const masteredCount = mastery.filter((m) => m.p_l >= 0.8).length;
    const weakCount = mastery.filter((m) => m.p_l < 0.5).length;
    const avgScore = attempts.length
        ? attempts.reduce((a, t) => a + (t.score ?? 0), 0) / attempts.length
        : 0;

    return (
        <div className="animate-fade-in space-y-8">
            {/* Header */}
            <div>
                <h1 className="text-2xl font-bold text-white">Student Dashboard</h1>
                <p className="mt-1 text-sm text-gray-400">
                    Welcome back! Here&apos;s your learning overview.
                </p>
            </div>

            {/* Stats cards */}
            <div className="stagger grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
                {[
                    {
                        label: "Concepts Tracked",
                        value: mastery.length,
                        icon: "📊",
                        gradient: "from-indigo-500/20 to-violet-500/20",
                        border: "border-indigo-500/20",
                    },
                    {
                        label: "Mastered",
                        value: masteredCount,
                        icon: "🏆",
                        gradient: "from-emerald-500/20 to-teal-500/20",
                        border: "border-emerald-500/20",
                    },
                    {
                        label: "Needs Work",
                        value: weakCount,
                        icon: "⚠️",
                        gradient: "from-amber-500/20 to-orange-500/20",
                        border: "border-amber-500/20",
                    },
                    {
                        label: "Avg Score",
                        value: `${(avgScore * 100).toFixed(0)}%`,
                        icon: "🎯",
                        gradient: "from-cyan-500/20 to-blue-500/20",
                        border: "border-cyan-500/20",
                    },
                ].map((card) => (
                    <div
                        key={card.label}
                        className={`animate-slide-up glass-card glass-card-hover border ${card.border} bg-gradient-to-br ${card.gradient} p-5`}
                    >
                        <div className="flex items-center justify-between">
                            <p className="text-sm font-medium text-gray-400">{card.label}</p>
                            <span className="text-xl">{card.icon}</span>
                        </div>
                        <p className="mt-2 text-3xl font-bold text-white">{card.value}</p>
                    </div>
                ))}
            </div>

            {/* Mastery overview */}
            <div className="glass-card p-6">
                <h2 className="mb-4 text-lg font-semibold text-white">Concept Mastery</h2>
                {mastery.length === 0 ? (
                    <p className="text-sm text-gray-500">
                        No mastery data yet. Start submitting work to track progress.
                    </p>
                ) : (
                    <div className="space-y-4">
                        {mastery.map((m) => (
                            <div key={m.id}>
                                <div className="mb-1 flex items-center justify-between text-sm">
                                    <span className="text-gray-300">
                                        Concept #{m.concept_id}
                                    </span>
                                    <span className={`font-medium ${m.p_l >= 0.8 ? "text-emerald-400" : m.p_l >= 0.5 ? "text-amber-400" : "text-red-400"}`}>
                                        {(m.p_l * 100).toFixed(0)}% — {masteryLabel(m.p_l)}
                                    </span>
                                </div>
                                <div className="mastery-bar">
                                    <div
                                        className={`mastery-bar-fill bg-gradient-to-r ${masteryColor(m.p_l)}`}
                                        style={{ width: `${Math.max(m.p_l * 100, 2)}%` }}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Overall progress */}
            <div className="glass-card flex items-center gap-6 p-6">
                <div className="relative flex h-24 w-24 items-center justify-center">
                    <svg viewBox="0 0 100 100" className="h-full w-full -rotate-90">
                        <circle cx="50" cy="50" r="42" fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="8" />
                        <circle
                            cx="50" cy="50" r="42" fill="none"
                            stroke="url(#grad)" strokeWidth="8"
                            strokeLinecap="round"
                            strokeDasharray={`${avgMastery * 264} 264`}
                        />
                        <defs>
                            <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stopColor="#6366f1" />
                                <stop offset="100%" stopColor="#8b5cf6" />
                            </linearGradient>
                        </defs>
                    </svg>
                    <span className="absolute text-lg font-bold text-white">
                        {(avgMastery * 100).toFixed(0)}%
                    </span>
                </div>
                <div>
                    <h3 className="text-lg font-semibold text-white">Overall Mastery</h3>
                    <p className="text-sm text-gray-400">
                        Across {mastery.length} concepts · {attempts.length} total attempts
                    </p>
                </div>
            </div>
        </div>
    );
}
