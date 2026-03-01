import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProviderWrapper } from "@/components/AuthProviderWrapper";

const inter = Inter({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "ALOS · Adaptive Learning OS",
  description:
    "Predictive Mastery Intelligence Platform — Track, predict, and improve student learning outcomes.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} antialiased`}>
        <AuthProviderWrapper>{children}</AuthProviderWrapper>
      </body>
    </html>
  );
}
