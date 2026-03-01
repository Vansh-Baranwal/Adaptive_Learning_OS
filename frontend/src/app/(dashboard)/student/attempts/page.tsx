"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import api from "@/lib/api";
import type { AttemptResponse } from "@/types";

export default function AttemptsPage() {
    const { user } = useAuth();
    const [attempts, setAttempts] = useState<AttemptResponse[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!user) return;
        api
            .get<AttemptResponse[]>(`/students/${user.id}/attempts`)
            .then((res) => setAttempts(res.data))
            .catch(() => { })
            .finally(() => setLoading(false));
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
                <h1 className="text-2xl font-bold text-white">My Attempts</h1>
                <p className="mt-1 text-sm text-gray-400">
                    Review all your past assignment submissions and scores.
                </p>
            </div>

            <div className="glass-card overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                        <thead>
                            <tr className="border-b border-white/[0.06] text-left text-gray-400">
                                <th className="px-6 py-4 font-medium">ID</th>
                                <th className="px-6 py-4 font-medium">Assignment</th>
                                <th className="px-6 py-4 font-medium">Concept</th>
                                <th className="px-6 py-4 font-medium">Content</th>
                                <th className="px-6 py-4 font-medium">Score</th>
                                <th className="px-6 py-4 font-medium">Submitted</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-white/[0.04]">
                            {attempts.length === 0 ? (
                                <tr>
                                    <td colSpan={6} className="px-6 py-10 text-center text-gray-500">
                                        You haven&apos;t submitted any attempts yet.
                                    </td>
                                </tr>
                            ) : (
                                attempts.map((a) => (
                                    <tr key={a.id} className="transition-colors hover:bg-white/[0.02]">
                                        <td className="px-6 py-4 text-gray-300">#{a.id}</td>
                                        <td className="px-6 py-4 font-medium text-white">
                                            Assignment #{a.assignment_id}
                                        </td>
                                        <td className="px-6 py-4 text-gray-300">#{a.concept_id}</td>
                                        <td className="max-w-[200px] truncate px-6 py-4 text-gray-400">
                                            {a.content}
                                        </td>
                                        <td className="px-6 py-4">
                                            {a.score !== null ? (
                                                <span
                                                    className={`inline-flex rounded-full px-2.5 py-0.5 text-xs font-semibold ${a.score >= 0.8
                                                            ? "bg-emerald-500/15 text-emerald-400"
                                                            : a.score >= 0.5
                                                                ? "bg-amber-500/15 text-amber-400"
                                                                : "bg-red-500/15 text-red-400"
                                                        }`}
                                                >
                                                    {(a.score * 100).toFixed(0)}%
                                                </span>
                                            ) : (
                                                <span className="text-gray-500">Pending</span>
                                            )}
                                        </td>
                                        <td className="px-6 py-4 text-gray-400">
                                            {new Date(a.submitted_at).toLocaleString()}
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
