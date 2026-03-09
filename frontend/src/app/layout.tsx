import type { Metadata } from "next";
import { DM_Sans, Outfit } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";

const dmSans = DM_Sans({
  subsets: ["latin"],
  variable: "--font-inter", // keeping variable name to match globals.css without breaking other things
  display: "swap",
});

const outfit = Outfit({
  subsets: ["latin"],
  variable: "--font-jakarta", // keeping variable name
  display: "swap",
});

export const metadata: Metadata = {
  title: "VulnGuard AI — AI-Powered Vulnerability Scanner",
  description:
    "Scan GitHub repositories for security vulnerabilities, get AI-powered attack simulations, and receive secure code fixes.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning className={`${dmSans.variable} ${outfit.variable}`}>
      <body className="antialiased bg-[#000000] text-white min-h-screen selection:bg-emerald-500/30 font-sans" suppressHydrationWarning>

        <Navbar />

        <main className="relative z-10 w-full">
          {children}
        </main>
      </body>
    </html>
  );
}
