"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import Link from "next/link";
import type { UserCreate } from "@/types";

export default function RegisterPage() {
    const { register } = useAuth();
    const router = useRouter();
    const [form, setForm] = useState<UserCreate>({
        email: "",
        password: "",
        first_name: "",
        last_name: "",
        role: "student",
        department: "",
    });
    const [error, setError] = useState("");
    const [submitting, setSubmitting] = useState(false);

    const set = (key: keyof UserCreate, val: string) =>
        setForm((prev) => ({ ...prev, [key]: val }));

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setSubmitting(true);
        try {
            const payload = { ...form };
            if (payload.role !== "teacher") delete payload.department;
            await register(payload);
            router.push("/login");
        } catch (err: unknown) {
            const msg =
                (err as { response?: { data?: { detail?: string } } })?.response?.data
                    ?.detail ?? "Registration failed. Please try again.";
            setError(typeof msg === "string" ? msg : JSON.stringify(msg));
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-gray-950 px-4 py-12">
            {/* Background decorations */}
            <div className="pointer-events-none fixed inset-0 overflow-hidden">
                <div className="absolute -left-32 -top-32 h-96 w-96 rounded-full bg-emerald-600/10 blur-[120px]" />
                <div className="absolute -bottom-32 -right-32 h-96 w-96 rounded-full bg-indigo-600/10 blur-[120px]" />
            </div>

            <div className="animate-fade-in relative w-full max-w-md">
                {/* Brand */}
                <div className="mb-8 text-center">
                    <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 text-xl font-bold text-white shadow-lg shadow-emerald-500/25">
                        A
                    </div>
                    <h1 className="text-2xl font-bold text-white">Create your account</h1>
                    <p className="mt-1 text-sm text-gray-400">
                        Join Adaptive Learning OS
                    </p>
                </div>

                {/* Card */}
                <div className="glass-card p-8">
                    <form onSubmit={handleSubmit} className="space-y-4">
                        {error && (
                            <div className="rounded-lg border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-400">
                                {error}
                            </div>
                        )}

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label htmlFor="first_name" className="mb-1.5 block text-sm font-medium text-gray-300">
                                    First Name
                                </label>
                                <input
                                    id="first_name"
                                    required
                                    value={form.first_name}
                                    onChange={(e) => set("first_name", e.target.value)}
                                    className="w-full rounded-lg border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm text-white placeholder-gray-500 outline-none transition-colors focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/25"
                                    placeholder="Jane"
                                />
                            </div>
                            <div>
                                <label htmlFor="last_name" className="mb-1.5 block text-sm font-medium text-gray-300">
                                    Last Name
                                </label>
                                <input
                                    id="last_name"
                                    required
                                    value={form.last_name}
                                    onChange={(e) => set("last_name", e.target.value)}
                                    className="w-full rounded-lg border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm text-white placeholder-gray-500 outline-none transition-colors focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/25"
                                    placeholder="Doe"
                                />
                            </div>
                        </div>

                        <div>
                            <label htmlFor="reg-email" className="mb-1.5 block text-sm font-medium text-gray-300">
                                Email
                            </label>
                            <input
                                id="reg-email"
                                type="email"
                                required
                                value={form.email}
                                onChange={(e) => set("email", e.target.value)}
                                className="w-full rounded-lg border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm text-white placeholder-gray-500 outline-none transition-colors focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/25"
                                placeholder="you@example.com"
                            />
                        </div>

                        <div>
                            <label htmlFor="reg-password" className="mb-1.5 block text-sm font-medium text-gray-300">
                                Password
                            </label>
                            <input
                                id="reg-password"
                                type="password"
                                required
                                value={form.password}
                                onChange={(e) => set("password", e.target.value)}
                                className="w-full rounded-lg border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm text-white placeholder-gray-500 outline-none transition-colors focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/25"
                                placeholder="••••••••"
                            />
                        </div>

                        <div>
                            <label htmlFor="role" className="mb-1.5 block text-sm font-medium text-gray-300">
                                I am a…
                            </label>
                            <div className="grid grid-cols-2 gap-3">
                                {(["student", "teacher"] as const).map((r) => (
                                    <button
                                        key={r}
                                        type="button"
                                        onClick={() => set("role", r)}
                                        className={`rounded-lg border px-4 py-2.5 text-sm font-medium capitalize transition-all ${form.role === r
                                                ? "border-indigo-500/50 bg-indigo-500/15 text-indigo-400"
                                                : "border-white/10 bg-white/[0.02] text-gray-400 hover:border-white/20 hover:text-white"
                                            }`}
                                    >
                                        {r}
                                    </button>
                                ))}
                            </div>
                        </div>

                        {form.role === "teacher" && (
                            <div className="animate-fade-in">
                                <label htmlFor="department" className="mb-1.5 block text-sm font-medium text-gray-300">
                                    Department <span className="text-gray-500">(optional)</span>
                                </label>
                                <input
                                    id="department"
                                    value={form.department ?? ""}
                                    onChange={(e) => set("department", e.target.value)}
                                    className="w-full rounded-lg border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm text-white placeholder-gray-500 outline-none transition-colors focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/25"
                                    placeholder="Computer Science"
                                />
                            </div>
                        )}

                        <button
                            type="submit"
                            disabled={submitting}
                            className="w-full rounded-lg bg-gradient-to-r from-emerald-500 to-teal-600 px-4 py-2.5 text-sm font-semibold text-white shadow-lg shadow-emerald-500/25 transition-all hover:shadow-emerald-500/40 disabled:cursor-not-allowed disabled:opacity-60"
                        >
                            {submitting ? (
                                <span className="flex items-center justify-center gap-2">
                                    <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                                    Creating account…
                                </span>
                            ) : (
                                "Create account"
                            )}
                        </button>
                    </form>

                    <p className="mt-6 text-center text-sm text-gray-400">
                        Already have an account?{" "}
                        <Link
                            href="/login"
                            className="font-medium text-indigo-400 transition-colors hover:text-indigo-300"
                        >
                            Sign in
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
}
