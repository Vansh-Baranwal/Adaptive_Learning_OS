"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import api from "@/lib/api";
import type { AssignmentCreate, AssignmentResponse } from "@/types";

export default function AssignmentsPage() {
    const { user } = useAuth();
    const [assignments, setAssignments] = useState<AssignmentResponse[]>([]);
    const [loading, setLoading] = useState(true);
    const [showForm, setShowForm] = useState(false);
    const [editId, setEditId] = useState<number | null>(null);
    const [formError, setFormError] = useState("");
    const [submitting, setSubmitting] = useState(false);
    const [form, setForm] = useState({
        title: "",
        description: "",
        concept_id: "",
        due_date: "",
    });

    const fetchAssignments = () => {
        api
            .get<AssignmentResponse[]>("/assignments/")
            .then((res) => setAssignments(res.data))
            .catch(() => { })
            .finally(() => setLoading(false));
    };

    useEffect(() => {
        fetchAssignments();
    }, []);

    const resetForm = () => {
        setForm({ title: "", description: "", concept_id: "", due_date: "" });
        setEditId(null);
        setShowForm(false);
        setFormError("");
    };

    const handleEdit = (a: AssignmentResponse) => {
        setForm({
            title: a.title,
            description: a.description ?? "",
            concept_id: String(a.concept_id),
            due_date: a.due_date ? a.due_date.slice(0, 16) : "",
        });
        setEditId(a.id);
        setShowForm(true);
    };

    const handleDelete = async (id: number) => {
        if (!confirm("Delete this assignment?")) return;
        try {
            await api.delete(`/assignments/${id}`);
            setAssignments((prev) => prev.filter((a) => a.id !== id));
        } catch {
            alert("Failed to delete assignment.");
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!user) return;
        setSubmitting(true);
        setFormError("");
        const payload: AssignmentCreate = {
            title: form.title,
            description: form.description || undefined,
            concept_id: Number(form.concept_id),
            teacher_id: user.id,
            due_date: form.due_date ? new Date(form.due_date).toISOString() : undefined,
        };

        try {
            if (editId) {
                await api.put(`/assignments/${editId}`, payload);
            } else {
                await api.post("/assignments/", payload);
            }
            resetForm();
            fetchAssignments();
        } catch (err: unknown) {
            const msg =
                (err as { response?: { data?: { detail?: string } } })?.response?.data
                    ?.detail ?? "Failed to save assignment.";
            setFormError(typeof msg === "string" ? msg : JSON.stringify(msg));
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className="animate-fade-in space-y-8">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-white">Assignments</h1>
                    <p className="mt-1 text-sm text-gray-400">
                        Create, edit, and manage assignments for your students.
                    </p>
                </div>
                <button
                    onClick={() => {
                        resetForm();
                        setShowForm(true);
                    }}
                    className="rounded-lg bg-gradient-to-r from-indigo-500 to-violet-600 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-indigo-500/25 transition-all hover:shadow-indigo-500/40"
                >
                    + New Assignment
                </button>
            </div>

            {/* Form */}
            {showForm && (
                <div className="animate-fade-in glass-card max-w-2xl p-6">
                    <h3 className="mb-4 text-lg font-semibold text-white">
                        {editId ? "Edit Assignment" : "New Assignment"}
                    </h3>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label htmlFor="title" className="mb-1.5 block text-sm font-medium text-gray-300">
                                Title
                            </label>
                            <input
                                id="title"
                                required
                                value={form.title}
                                onChange={(e) => setForm((p) => ({ ...p, title: e.target.value }))}
                                className="w-full rounded-lg border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm text-white outline-none focus:border-indigo-500/50"
                                placeholder="Assignment title"
                            />
                        </div>
                        <div>
                            <label htmlFor="desc" className="mb-1.5 block text-sm font-medium text-gray-300">
                                Description
                            </label>
                            <textarea
                                id="desc"
                                rows={3}
                                value={form.description}
                                onChange={(e) => setForm((p) => ({ ...p, description: e.target.value }))}
                                className="w-full rounded-lg border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm text-white outline-none focus:border-indigo-500/50"
                                placeholder="Optional description"
                            />
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label htmlFor="concept" className="mb-1.5 block text-sm font-medium text-gray-300">
                                    Concept ID
                                </label>
                                <input
                                    id="concept"
                                    type="number"
                                    min={1}
                                    required
                                    value={form.concept_id}
                                    onChange={(e) => setForm((p) => ({ ...p, concept_id: e.target.value }))}
                                    className="w-full rounded-lg border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm text-white outline-none focus:border-indigo-500/50"
                                    placeholder="1"
                                />
                            </div>
                            <div>
                                <label htmlFor="due" className="mb-1.5 block text-sm font-medium text-gray-300">
                                    Due Date <span className="text-gray-500">(optional)</span>
                                </label>
                                <input
                                    id="due"
                                    type="datetime-local"
                                    value={form.due_date}
                                    onChange={(e) => setForm((p) => ({ ...p, due_date: e.target.value }))}
                                    className="w-full rounded-lg border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm text-white outline-none focus:border-indigo-500/50"
                                />
                            </div>
                        </div>

                        {formError && (
                            <div className="rounded-lg border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-400">
                                {formError}
                            </div>
                        )}

                        <div className="flex gap-3">
                            <button
                                type="submit"
                                disabled={submitting}
                                className="rounded-lg bg-gradient-to-r from-indigo-500 to-violet-600 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-indigo-500/25 transition-all hover:shadow-indigo-500/40 disabled:opacity-60"
                            >
                                {submitting ? "Saving…" : editId ? "Update" : "Create"}
                            </button>
                            <button
                                type="button"
                                onClick={resetForm}
                                className="rounded-lg border border-white/10 px-5 py-2.5 text-sm text-gray-400 transition-colors hover:bg-white/[0.04]"
                            >
                                Cancel
                            </button>
                        </div>
                    </form>
                </div>
            )}

            {/* Table */}
            <div className="glass-card overflow-hidden">
                {loading ? (
                    <div className="flex h-32 items-center justify-center">
                        <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent" />
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm">
                            <thead>
                                <tr className="border-b border-white/[0.06] text-left text-gray-400">
                                    <th className="px-6 py-4 font-medium">ID</th>
                                    <th className="px-6 py-4 font-medium">Title</th>
                                    <th className="px-6 py-4 font-medium">Concept</th>
                                    <th className="px-6 py-4 font-medium">Due Date</th>
                                    <th className="px-6 py-4 font-medium">Created</th>
                                    <th className="px-6 py-4 font-medium">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-white/[0.04]">
                                {assignments.length === 0 ? (
                                    <tr>
                                        <td colSpan={6} className="px-6 py-10 text-center text-gray-500">
                                            No assignments yet. Create your first one!
                                        </td>
                                    </tr>
                                ) : (
                                    assignments.map((a) => (
                                        <tr key={a.id} className="transition-colors hover:bg-white/[0.02]">
                                            <td className="px-6 py-4 text-gray-300">#{a.id}</td>
                                            <td className="px-6 py-4 font-medium text-white">{a.title}</td>
                                            <td className="px-6 py-4 text-gray-300">#{a.concept_id}</td>
                                            <td className="px-6 py-4 text-gray-400">
                                                {a.due_date ? new Date(a.due_date).toLocaleString() : "—"}
                                            </td>
                                            <td className="px-6 py-4 text-gray-400">
                                                {new Date(a.created_at).toLocaleDateString()}
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="flex gap-2">
                                                    <button
                                                        onClick={() => handleEdit(a)}
                                                        className="rounded-md px-3 py-1 text-xs font-medium text-indigo-400 transition-colors hover:bg-indigo-500/10"
                                                    >
                                                        Edit
                                                    </button>
                                                    <button
                                                        onClick={() => handleDelete(a.id)}
                                                        className="rounded-md px-3 py-1 text-xs font-medium text-red-400 transition-colors hover:bg-red-500/10"
                                                    >
                                                        Delete
                                                    </button>
                                                </div>
                                            </td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
}
