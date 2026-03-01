"use client";

import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

interface Props {
    children: React.ReactNode;
    allowedRoles?: ("student" | "teacher")[];
}

export default function ProtectedRoute({ children, allowedRoles }: Props) {
    const { isAuthenticated, loading, user } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!loading && !isAuthenticated) {
            router.replace("/login");
        }
        if (
            !loading &&
            isAuthenticated &&
            allowedRoles &&
            user &&
            !allowedRoles.includes(user.role)
        ) {
            // Redirect to correct dashboard
            router.replace(user.role === "student" ? "/student" : "/teacher");
        }
    }, [loading, isAuthenticated, user, allowedRoles, router]);

    if (loading) {
        return (
            <div className="flex h-screen items-center justify-center bg-gray-950">
                <div className="flex flex-col items-center gap-4">
                    <div className="h-10 w-10 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent" />
                    <span className="text-sm text-gray-400">Loading…</span>
                </div>
            </div>
        );
    }

    if (!isAuthenticated) return null;
    if (allowedRoles && user && !allowedRoles.includes(user.role)) return null;

    return <>{children}</>;
}
