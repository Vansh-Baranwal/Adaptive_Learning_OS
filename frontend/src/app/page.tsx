"use client";

import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function Home() {
  const { isAuthenticated, loading, user } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      if (!isAuthenticated) {
        router.replace("/login");
      } else {
        router.replace(user?.role === "teacher" ? "/teacher" : "/student");
      }
    }
  }, [loading, isAuthenticated, user, router]);

  return (
    <div className="flex h-screen items-center justify-center bg-gray-950">
      <div className="flex flex-col items-center gap-4">
        <div className="h-10 w-10 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent" />
        <span className="text-sm text-gray-400">Redirecting…</span>
      </div>
    </div>
  );
}
