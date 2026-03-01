"use client";

import { useState } from "react";
import api from "@/lib/api";
import type { ConceptCreate, ConceptResponse } from "@/types";

export default function ConceptsPage() {
    const [form, setForm] = useState<ConceptCreate>({
        name: "",
        description: "",
        difficulty_level: 1,
        prerequisite_id: null,
    });
    const [created, setCreated] = useState<ConceptResponse | null>(null);
    const [prereqs, setPrereqs] = useState<ConceptResponse[]>([]);
    const [dependents, setDependents] = useState<ConceptResponse[]>([]);
    const [lookupId, setLookupId] = useState("");
    const [submitting, setSubmitting] = useState(false);
    const [lookupLoading, setLookupLoading] = useState(false);
    const [error, setError] = useState("");

    const handleCreate = async (e: React.FormEvent) => {
        e.preventDefault();
        setSubmitting(true);
        setError("");
        setCreated(null);
        try {
            const payload: ConceptCreate = {
                ...form,
                prerequisite_id: form.prerequisite_id || null,
            };
            const res = await api.post<ConceptResponse>("/concepts/", payload);
            setCreated(res.data);
            setForm({ name: "", description: "", difficulty_level: 1, prerequisite_id: null });
        } catch (err: unknown) {
            const msg =
                (err as { response?: { data?: { detail?: string } } })?.response?.data
                    ?.detail ?? "Failed to create concept.";
            setError(typeof msg === "string" ? msg : JSON.stringify(msg));
        } finally {
            setSubmitting(false);
        }
    };

    const handleLookup = async () => {
        if (!lookupId) return;
        setLookupLoading(true);
        setPrereqs([]);
        setDependents([]);
        try {
            const [pRes, dRes] = await Promise.allSettled([
                api.get<ConceptResponse[]>(`/concepts/${lookupId}/prerequisites`),
                api.get<ConceptResponse[]>(`/concepts/${lookupId}/dependents`),
            ]);
            if (pRes.status === "fulfilled") setPrereqs(pRes.value.data);
            if (dRes.status === "fulfilled") setDependents(dRes.value.data);
        } catch {
            /* ignore */
        } finally {
            setLookupLoading(false);
        }
    };

    return (
        <div className="animate-fade-in space-y-8">
            <div>
                <h1 className="text-2xl font-bold text-white">Concepts</h1>
                <p className="mt-1 text-sm text-gray-400">
                    Create concepts and explore prerequisite / dependent chains.
                </p>
            </div>

            {/* Create form */}
            <div className="glass-card max-w-2xl p-6">
                <h3 className="mb-4 text-lg font-semibold text-white">Create Concept</h3>
                <form onSubmit={handleCreate} className="space-y-4">
                    <div className="grid gap-4 sm:grid-cols-2">
                        <div>
                            <label className="mb-1.5 block text-sm font-medium text-gray-300">Name</label>
                            <input
                                required
                                value={form.name}
                                onChange={(e) => setForm((p) => ({ ...p, name: e.target.value }))}
                                className="w-full rounded-lg border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm text-white outline-none focus:border-indigo-500/50"
                                placeholder="e.g. Linear Algebra"
                            />
                        </div>
                        <div>
                            <label className="mb-1.5 block text-sm font-medium text-gray-300">Difficulty (1-5)</label>
                            <input
                                type="number"
                                min={1}
                                max={5}
                                value={form.difficulty_level}
                                onChange={(e) => setForm((p) => ({ ...p, difficulty_level: Number(e.target.value) }))}
                                className="w-full rounded-lg border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm text-white outline-none focus:border-indigo-500/50"
                            />
                        </div>
                    </div>
                    <div>
                        <label className="mb-1.5 block text-sm font-medium text-gray-300">Description</label>
                        <textarea
                            rows={2}
                            value={form.description ?? ""}
                            onChange={(e) => setForm((p) => ({ ...p, description: e.target.value }))}
                            className="w-full rounded-lg border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm text-white outline-none focus:border-indigo-500/50"
                            placeholder="Optional description"
                        />
                    </div>
                    <div>
                        <label className="mb-1.5 block text-sm font-medium text-gray-300">
                            Prerequisite Concept ID <span className="text-gray-500">(optional)</span>
                        </label>
                        <input
                            type="number"
                            min={1}
                            value={form.prerequisite_id ?? ""}
                            onChange={(e) =>
                                setForm((p) => ({
                                    ...p,
                                    prerequisite_id: e.target.value ? Number(e.target.value) : null,
                                }))
                            }
                            className="w-full rounded-lg border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm text-white outline-none focus:border-indigo-500/50"
                            placeholder="Leave empty if none"
                        />
                    </div>

                    {error && (
                        <div className="rounded-lg border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-400">
                            {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={submitting}
                        className="rounded-lg bg-gradient-to-r from-indigo-500 to-violet-600 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-indigo-500/25 transition-all hover:shadow-indigo-500/40 disabled:opacity-60"
                    >
                        {submitting ? "Creating…" : "Create Concept"}
                    </button>
                </form>

                {created && (
                    <div className="mt-4 animate-fade-in rounded-lg border border-emerald-500/20 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-400">
                        ✅ Created concept &quot;{created.name}&quot; (ID: {created.id})
                    </div>
                )}
            </div>

            {/* Prerequisite / Dependent Lookup */}
            <div className="glass-card max-w-2xl p-6">
                <h3 className="mb-4 text-lg font-semibold text-white">Concept Graph Lookup</h3>
                <div className="flex items-end gap-4">
                    <div className="flex-1">
                        <label className="mb-1.5 block text-sm font-medium text-gray-300">Concept ID</label>
                        <input
                            type="number"
                            min={1}
                            value={lookupId}
                            onChange={(e) => setLookupId(e.target.value)}
                            className="w-full rounded-lg border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm text-white outline-none focus:border-indigo-500/50"
                            placeholder="e.g. 1"
                        />
                    </div>
                    <button
                        onClick={handleLookup}
                        disabled={lookupLoading || !lookupId}
                        className="rounded-lg border border-white/10 px-5 py-2.5 text-sm font-medium text-gray-300 transition-colors hover:bg-white/[0.04] disabled:opacity-50"
                    >
                        {lookupLoading ? "Loading…" : "Lookup"}
                    </button>
                </div>

                {(prereqs.length > 0 || dependents.length > 0) && (
                    <div className="mt-6 grid gap-6 sm:grid-cols-2">
                        <div>
                            <h4 className="mb-2 text-sm font-semibold text-gray-400">Prerequisites</h4>
                            {prereqs.length === 0 ? (
                                <p className="text-sm text-gray-500">None</p>
                            ) : (
                                <ul className="space-y-2">
                                    {prereqs.map((c) => (
                                        <li key={c.id} className="rounded-lg border border-white/[0.06] bg-white/[0.02] p-3 text-sm">
                                            <span className="font-medium text-white">{c.name}</span>
                                            <span className="ml-2 text-gray-500">#{c.id} · Level {c.difficulty_level}</span>
                                        </li>
                                    ))}
                                </ul>
                            )}
                        </div>
                        <div>
                            <h4 className="mb-2 text-sm font-semibold text-gray-400">Dependents</h4>
                            {dependents.length === 0 ? (
                                <p className="text-sm text-gray-500">None</p>
                            ) : (
                                <ul className="space-y-2">
                                    {dependents.map((c) => (
                                        <li key={c.id} className="rounded-lg border border-white/[0.06] bg-white/[0.02] p-3 text-sm">
                                            <span className="font-medium text-white">{c.name}</span>
                                            <span className="ml-2 text-gray-500">#{c.id} · Level {c.difficulty_level}</span>
                                        </li>
                                    ))}
                                </ul>
                            )}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
