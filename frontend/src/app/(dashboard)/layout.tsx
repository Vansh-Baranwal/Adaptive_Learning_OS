"use client";

import Sidebar from "@/components/Sidebar";
import ProtectedRoute from "@/components/ProtectedRoute";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
    return (
        <ProtectedRoute>
            <div className="flex min-h-screen bg-gray-950">
                <Sidebar />
                <main className="ml-64 flex-1 p-8">{children}</main>
            </div>
        </ProtectedRoute>
    );
}
