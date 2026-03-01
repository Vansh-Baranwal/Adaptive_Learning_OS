"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import api from "@/lib/api";
import type { AssignmentResponse, AttemptResponse } from "@/types";

export default function SubmitPage() {
    const { user } = useAuth();
    const [assignments, setAssignments] = useState<AssignmentResponse[]>([]);
    const [assignmentId, setAssignmentId] = useState("");
    const [content, setContent] = useState("");
    const [result, setResult] = useState<AttemptResponse | null>(null);
    const [loading, setLoading] = useState(false);
    const [listLoading, setListLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        api
            .get<AssignmentResponse[]>("/assignments/")
            .then((res) => setAssignments(res.data))
            .catch(() => { })
            .finally(() => setListLoading(false));
    }, []);

    const selectedAssignment = assignments.find(
        (a) => a.id === Number(assignmentId)
    );

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!user || !selectedAssignment) return;
        setLoading(true);
        setError("");
        setResult(null);
        try {
            const res = await api.post<AttemptResponse>("/attempts/", {
                content,
                student_id: user.id,
                assignment_id: selectedAssignment.id,
                concept_id: selectedAssignment.concept_id,
            });
            setResult(res.data);
            setContent("");
        } catch (err: unknown) {
            const msg =
                (err as { response?: { data?: { detail?: string } } })?.response?.data
                    ?.detail ?? "Submission failed.";
            setError(typeof msg === "string" ? msg : JSON.stringify(msg));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="animate-fade-in space-y-8">
            <div>
                <h1 className="text-2xl font-bold text-white">Submit Work</h1>
                <p className="mt-1 text-sm text-gray-400">
                    Select an assignment and submit your response for AI evaluation.
                </p>
            </div>

            <div className="glass-card max-w-2xl p-6">
                <form onSubmit={handleSubmit} className="space-y-5">
                    <div>
                        <label htmlFor="assignment" className="mb-1.5 block text-sm font-medium text-gray-300">
                            Assignment
                        </label>
                        {listLoading ? (
                            <div className="flex h-10 items-center text-sm text-gray-500">Loading assignments…</div>
                        ) : (
                            <select
                                id="assignment"
                                required
                                value={assignmentId}
                                onChange={(e) => setAssignmentId(e.target.value)}
                                className="w-full rounded-lg border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm text-white outline-none transition-colors focus:border-indigo-500/50"
                            >
                                <option value="" className="bg-gray-900">Select an assignment…</option>
                                {assignments.map((a) => (
                                    <option key={a.id} value={a.id} className="bg-gray-900">
                                        {a.title} (Concept #{a.concept_id})
                                    </option>
                                ))}
                            </select>
                        )}
                    </div>

                    <div>
                        <label htmlFor="content" className="mb-1.5 block text-sm font-medium text-gray-300">
                            Your Response
                        </label>
                        <textarea
                            id="content"
                            required
                            rows={8}
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                            className="w-full rounded-lg border border-white/10 bg-white/[0.04] px-4 py-3 text-sm text-white placeholder-gray-500 outline-none transition-colors focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/25"
                            placeholder="Write your answer here…"
                        />
                    </div>

                    {error && (
                        <div className="rounded-lg border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-400">
                            {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={loading || !assignmentId}
                        className="rounded-lg bg-gradient-to-r from-indigo-500 to-violet-600 px-6 py-2.5 text-sm font-semibold text-white shadow-lg shadow-indigo-500/25 transition-all hover:shadow-indigo-500/40 disabled:cursor-not-allowed disabled:opacity-60"
                    >
                        {loading ? (
                            <span className="flex items-center gap-2">
                                <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                                Submitting…
                            </span>
                        ) : (
                            "Submit Attempt"
                        )}
                    </button>
                </form>
            </div>

            {/* Result */}
            {result && (
                <div className="animate-slide-up glass-card max-w-2xl p-6">
                    <h3 className="mb-4 text-lg font-semibold text-white">
                        ✅ Attempt Submitted!
                    </h3>
                    <div className="grid gap-4 sm:grid-cols-3">
                        <div className="rounded-lg border border-white/[0.06] bg-white/[0.02] p-4">
                            <p className="text-xs text-gray-500">Attempt ID</p>
                            <p className="mt-1 text-lg font-bold text-white">#{result.id}</p>
                        </div>
                        <div className="rounded-lg border border-white/[0.06] bg-white/[0.02] p-4">
                            <p className="text-xs text-gray-500">Score</p>
                            <p className="mt-1 text-lg font-bold text-white">
                                {result.score !== null ? `${(result.score * 100).toFixed(0)}%` : "Pending"}
                            </p>
                        </div>
                        <div className="rounded-lg border border-white/[0.06] bg-white/[0.02] p-4">
                            <p className="text-xs text-gray-500">Submitted</p>
                            <p className="mt-1 text-sm font-medium text-white">
                                {new Date(result.submitted_at).toLocaleString()}
                            </p>
                        </div>
                    </div>
                    {result.evaluation && (
                        <div className="mt-4 rounded-lg border border-white/[0.06] bg-white/[0.02] p-4">
                            <p className="mb-2 text-xs text-gray-500">Evaluation Feedback</p>
                            <pre className="text-sm text-gray-300 whitespace-pre-wrap">
                                {JSON.stringify(result.evaluation, null, 2)}
                            </pre>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
