"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import Link from "next/link";

export default function LoginPage() {
    const { login, isAuthenticated, user, loading } = useAuth();
    const router = useRouter();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [submitting, setSubmitting] = useState(false);

    // Redirect if already logged in
    if (!loading && isAuthenticated && user) {
        router.replace(user.role === "teacher" ? "/teacher" : "/student");
        return null;
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setSubmitting(true);
        try {
            await login(email, password);
        } catch (err: unknown) {
            const msg =
                (err as { response?: { data?: { detail?: string } } })?.response?.data
                    ?.detail ?? "Login failed. Please check your credentials.";
            setError(msg);
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-gray-950 px-4">
            {/* Background decorations */}
            <div className="pointer-events-none fixed inset-0 overflow-hidden">
                <div className="absolute -left-32 -top-32 h-96 w-96 rounded-full bg-indigo-600/10 blur-[120px]" />
                <div className="absolute -bottom-32 -right-32 h-96 w-96 rounded-full bg-violet-600/10 blur-[120px]" />
            </div>

            <div className="animate-fade-in relative w-full max-w-md">
                {/* Brand */}
                <div className="mb-8 text-center">
                    <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-500 to-violet-600 text-xl font-bold text-white shadow-lg shadow-indigo-500/25">
                        A
                    </div>
                    <h1 className="text-2xl font-bold text-white">Welcome back</h1>
                    <p className="mt-1 text-sm text-gray-400">
                        Sign in to Adaptive Learning OS
                    </p>
                </div>

                {/* Card */}
                <div className="glass-card p-8">
                    <form onSubmit={handleSubmit} className="space-y-5">
                        {error && (
                            <div className="rounded-lg border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-400">
                                {error}
                            </div>
                        )}

                        <div>
                            <label htmlFor="email" className="mb-1.5 block text-sm font-medium text-gray-300">
                                Email
                            </label>
                            <input
                                id="email"
                                type="email"
                                required
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full rounded-lg border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm text-white placeholder-gray-500 outline-none transition-colors focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/25"
                                placeholder="you@example.com"
                            />
                        </div>

                        <div>
                            <label htmlFor="password" className="mb-1.5 block text-sm font-medium text-gray-300">
                                Password
                            </label>
                            <input
                                id="password"
                                type="password"
                                required
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full rounded-lg border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm text-white placeholder-gray-500 outline-none transition-colors focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/25"
                                placeholder="••••••••"
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={submitting}
                            className="w-full rounded-lg bg-gradient-to-r from-indigo-500 to-violet-600 px-4 py-2.5 text-sm font-semibold text-white shadow-lg shadow-indigo-500/25 transition-all hover:shadow-indigo-500/40 disabled:cursor-not-allowed disabled:opacity-60"
                        >
                            {submitting ? (
                                <span className="flex items-center justify-center gap-2">
                                    <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                                    Signing in…
                                </span>
                            ) : (
                                "Sign in"
                            )}
                        </button>
                    </form>

                    <p className="mt-6 text-center text-sm text-gray-400">
                        Don&apos;t have an account?{" "}
                        <Link
                            href="/register"
                            className="font-medium text-indigo-400 transition-colors hover:text-indigo-300"
                        >
                            Create one
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
}
