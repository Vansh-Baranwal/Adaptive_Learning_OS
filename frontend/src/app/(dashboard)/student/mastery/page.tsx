"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import api from "@/lib/api";
import type { MasteryResponse } from "@/types";

export default function MasteryPage() {
    const { user } = useAuth();
    const [mastery, setMastery] = useState<MasteryResponse[]>([]);
    const [weakConcepts, setWeakConcepts] = useState<MasteryResponse[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!user) return;
        const sid = user.id;
        Promise.allSettled([
            api.get<MasteryResponse[]>(`/students/${sid}/mastery`),
            api.get(`/mastery/student/${sid}/weak-concepts?threshold=0.5`),
        ]).then(([mRes, wRes]) => {
            if (mRes.status === "fulfilled") setMastery(mRes.value.data);
            if (wRes.status === "fulfilled") setWeakConcepts(wRes.value.data);
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
                <h1 className="text-2xl font-bold text-white">Mastery Tracker</h1>
                <p className="mt-1 text-sm text-gray-400">
                    Detailed Bayesian Knowledge Tracing parameters for each concept.
                </p>
            </div>

            {/* Weak concepts alert */}
            {weakConcepts.length > 0 && (
                <div className="rounded-xl border border-amber-500/20 bg-amber-500/5 p-5">
                    <h3 className="flex items-center gap-2 text-sm font-semibold text-amber-400">
                        <span>⚠️</span> Weak Concepts ({weakConcepts.length})
                    </h3>
                    <p className="mt-1 text-sm text-gray-400">
                        These concepts have mastery below 50%. Focus on these to improve.
                    </p>
                    <div className="mt-3 flex flex-wrap gap-2">
                        {weakConcepts.map((w) => (
                            <span
                                key={w.id}
                                className="rounded-full border border-amber-500/30 bg-amber-500/10 px-3 py-1 text-xs font-medium text-amber-300"
                            >
                                Concept #{w.concept_id} · {(w.p_l * 100).toFixed(0)}%
                            </span>
                        ))}
                    </div>
                </div>
            )}

            {/* Mastery table */}
            <div className="glass-card overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                        <thead>
                            <tr className="border-b border-white/[0.06] text-left text-gray-400">
                                <th className="px-6 py-4 font-medium">Concept</th>
                                <th className="px-6 py-4 font-medium">Mastery (p_l)</th>
                                <th className="px-6 py-4 font-medium">Learn Rate (p_t)</th>
                                <th className="px-6 py-4 font-medium">Guess (p_g)</th>
                                <th className="px-6 py-4 font-medium">Slip (p_s)</th>
                                <th className="px-6 py-4 font-medium">Attempts</th>
                                <th className="px-6 py-4 font-medium">Updated</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-white/[0.04]">
                            {mastery.length === 0 ? (
                                <tr>
                                    <td colSpan={7} className="px-6 py-10 text-center text-gray-500">
                                        No mastery data available yet.
                                    </td>
                                </tr>
                            ) : (
                                mastery.map((m) => (
                                    <tr key={m.id} className="transition-colors hover:bg-white/[0.02]">
                                        <td className="px-6 py-4 font-medium text-white">
                                            Concept #{m.concept_id}
                                        </td>
                                        <td className="px-6 py-4">
                                            <div className="flex items-center gap-3">
                                                <div className="h-2 w-20 overflow-hidden rounded-full bg-white/[0.06]">
                                                    <div
                                                        className={`h-full rounded-full ${m.p_l >= 0.8 ? "bg-emerald-500" : m.p_l >= 0.5 ? "bg-amber-500" : "bg-red-500"}`}
                                                        style={{ width: `${m.p_l * 100}%` }}
                                                    />
                                                </div>
                                                <span className="text-white">{(m.p_l * 100).toFixed(1)}%</span>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 text-gray-300">{m.p_t.toFixed(3)}</td>
                                        <td className="px-6 py-4 text-gray-300">{m.p_g.toFixed(3)}</td>
                                        <td className="px-6 py-4 text-gray-300">{m.p_s.toFixed(3)}</td>
                                        <td className="px-6 py-4 text-gray-300">{m.attempt_count}</td>
                                        <td className="px-6 py-4 text-gray-400">
                                            {new Date(m.last_updated).toLocaleDateString()}
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
