"use client";

import { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import api from "@/lib/api";
import type { MasteryPrediction } from "@/types";

export default function PredictPage() {
    const { user } = useAuth();
    const [conceptId, setConceptId] = useState("");
    const [prediction, setPrediction] = useState<MasteryPrediction | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handlePredict = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!user || !conceptId) return;
        setLoading(true);
        setError("");
        setPrediction(null);
        try {
            const res = await api.get<MasteryPrediction>(
                `/mastery/student/${user.id}/predict/${conceptId}`
            );
            setPrediction(res.data);
        } catch {
            setError("Failed to get prediction. Make sure the concept ID is valid.");
        } finally {
            setLoading(false);
        }
    };

    const pct = prediction ? prediction.predicted_mastery * 100 : 0;

    return (
        <div className="animate-fade-in space-y-8">
            <div>
                <h1 className="text-2xl font-bold text-white">Mastery Prediction</h1>
                <p className="mt-1 text-sm text-gray-400">
                    Predict your future mastery level for any concept using our BKT model.
                </p>
            </div>

            {/* Form */}
            <div className="glass-card max-w-lg p-6">
                <form onSubmit={handlePredict} className="flex items-end gap-4">
                    <div className="flex-1">
                        <label htmlFor="concept-id" className="mb-1.5 block text-sm font-medium text-gray-300">
                            Concept ID
                        </label>
                        <input
                            id="concept-id"
                            type="number"
                            min={1}
                            required
                            value={conceptId}
                            onChange={(e) => setConceptId(e.target.value)}
                            className="w-full rounded-lg border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm text-white placeholder-gray-500 outline-none transition-colors focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/25"
                            placeholder="e.g. 1"
                        />
                    </div>
                    <button
                        type="submit"
                        disabled={loading}
                        className="rounded-lg bg-gradient-to-r from-indigo-500 to-violet-600 px-6 py-2.5 text-sm font-semibold text-white shadow-lg shadow-indigo-500/25 transition-all hover:shadow-indigo-500/40 disabled:opacity-60"
                    >
                        {loading ? "Predicting…" : "Predict"}
                    </button>
                </form>
            </div>

            {error && (
                <div className="max-w-lg rounded-lg border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-400">
                    {error}
                </div>
            )}

            {/* Result */}
            {prediction && (
                <div className="animate-slide-up glass-card max-w-lg p-8">
                    <h3 className="mb-6 text-center text-sm font-medium text-gray-400">
                        Predicted Mastery — Concept #{prediction.concept_id}
                    </h3>
                    <div className="flex flex-col items-center">
                        {/* Radial gauge */}
                        <div className="relative flex h-40 w-40 items-center justify-center">
                            <svg viewBox="0 0 100 100" className="h-full w-full -rotate-90">
                                <circle
                                    cx="50" cy="50" r="42"
                                    fill="none"
                                    stroke="rgba(255,255,255,0.06)"
                                    strokeWidth="10"
                                />
                                <circle
                                    cx="50" cy="50" r="42"
                                    fill="none"
                                    stroke={pct >= 80 ? "#10b981" : pct >= 50 ? "#f59e0b" : "#ef4444"}
                                    strokeWidth="10"
                                    strokeLinecap="round"
                                    strokeDasharray={`${(pct / 100) * 264} 264`}
                                    className="transition-all duration-1000"
                                />
                            </svg>
                            <span className="absolute text-3xl font-bold text-white">
                                {pct.toFixed(0)}%
                            </span>
                        </div>
                        <p className="mt-4 text-sm text-gray-400">
                            {pct >= 80
                                ? "🎉 On track to master this concept!"
                                : pct >= 50
                                    ? "📈 Getting there — keep practicing."
                                    : "💪 More practice needed. Don't give up!"}
                        </p>
                    </div>
                </div>
            )}
        </div>
    );
}
