"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

export default function HomePage() {
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  return (
    <div className="flex flex-col min-h-screen bg-[#000000] overflow-hidden selection:bg-emerald-500/30">
      {/* 1. Cinematic Hero Section */}
      <section className="relative pt-32 pb-20 md:pt-48 md:pb-32 overflow-hidden flex flex-col items-center justify-center min-h-[90vh]">
        {/* Abstract Animated Background */}
        <div className="absolute inset-0 z-0 pointer-events-none">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-emerald-500/10 rounded-full blur-[120px] opacity-50 animate-pulse" style={{ animationDuration: '4s' }} />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-violet-500/10 rounded-full blur-[100px] opacity-30 animate-pulse" style={{ animationDuration: '6s', animationDelay: '1s' }} />
          {/* Subtle Grid overlay */}
          <div className="absolute inset-0 bg-[linear-gradient(to_right,#ffffff05_1px,transparent_1px),linear-gradient(to_bottom,#ffffff05_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]" />
        </div>

        <div className="relative z-10 max-w-5xl mx-auto px-6 text-center flex flex-col items-center">
          {/* Version Badge */}
          <div className="animate-fade-in mb-8 opacity-0" style={{ animationDelay: "0.1s", animationFillMode: "forwards" }}>
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-white/10 bg-white/[0.03] backdrop-blur-md shadow-2xl overflow-hidden relative group cursor-default transition-transform hover:scale-105 duration-300">
              <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/10 to-violet-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              <span className="relative text-sm font-medium text-white/80 tracking-wide">VulnGuard Engine v3.0 Core Online</span>
            </div>
          </div>

          <h1 className="text-5xl md:text-7xl lg:text-8xl font-black font-heading tracking-tighter leading-[1.05] mb-6 animate-fade-in opacity-0 text-white" style={{ animationDelay: "0.2s", animationFillMode: "forwards" }}>
            Ship code that
            <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-white via-emerald-200 to-white/60">
              hackers hate.
            </span>
          </h1>

          <p className="text-lg md:text-xl text-white/60 max-w-2xl mx-auto mb-12 animate-fade-in opacity-0 leading-relaxed font-light" style={{ animationDelay: "0.3s", animationFillMode: "forwards" }}>
            An enterprise-grade autonomous engine that <span className="text-violet-400 font-medium tracking-wide">simulates cyber attacks</span>, <span className="text-amber-400 font-medium tracking-wide">identifies vulnerabilities</span>, and <span className="text-emerald-400 font-medium tracking-wide">merges AI-generated secure patches</span> before you deploy.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center w-full sm:w-auto animate-fade-in opacity-0" style={{ animationDelay: "0.4s", animationFillMode: "forwards" }}>
            <Link href="/scan" className="relative group inline-flex items-center justify-center px-8 py-4 font-semibold text-white transition-all duration-300 bg-white/5 border border-white/10 rounded-xl overflow-hidden hover:scale-[1.02] hover:bg-white/10 hover:shadow-[0_0_40px_-10px_rgba(16,185,129,0.3)] min-w-[200px]">
              <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/20 to-violet-500/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <span className="relative flex items-center gap-2">
                Deploy Scanner
                <svg className="w-4 h-4 transition-transform group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </span>
            </Link>
            <Link href="/dashboard" className="px-8 py-4 font-semibold text-white/70 transition-all duration-300 hover:text-white min-w-[200px]">
              View Architecture &rarr;
            </Link>
          </div>
        </div>

        {/* Abstract Visual Dashboard Rep */}
        <div className="w-full max-w-5xl mx-auto mt-24 px-6 relative z-10 animate-fade-in opacity-0" style={{ animationDelay: "0.6s", animationFillMode: "forwards" }}>
          <div className="relative rounded-2xl border border-white/10 bg-[#09090b]/80 backdrop-blur-2xl shadow-2xl overflow-hidden aspect-[16/10] md:aspect-[21/9] flex flex-col">
            {/* Fake Window Header */}
            <div className="h-10 border-b border-white/10 px-4 flex items-center gap-2 bg-white/[0.02]">
              <div className="w-3 h-3 rounded-full bg-rose-500/80"></div>
              <div className="w-3 h-3 rounded-full bg-amber-500/80"></div>
              <div className="w-3 h-3 rounded-full bg-emerald-500/80"></div>
              <div className="ml-4 text-xs font-mono text-white/40">vulnguard/core-engine</div>
            </div>
            {/* Fake Body */}
            <div className="flex-1 p-4 md:p-6 flex flex-col gap-3 font-mono text-xs md:text-sm relative overflow-hidden">
              <div className="absolute right-0 top-0 bottom-0 w-32 md:w-64 bg-gradient-to-l from-[#09090b]/80 to-transparent pointer-events-none"></div>

              <div className="text-emerald-500/80 flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> [SYS] Initiating deep scan sequence...</div>

              {mounted && (
                <div className="text-white/40 pl-4 border-l border-white/10 animate-fade-in opacity-0" style={{ animationDelay: "1s", animationFillMode: "forwards" }}>
                  Analyzing 1,402,845 LOC across 48 repositories.
                </div>
              )}

              {mounted && (
                <div className="text-white/60 mt-2 animate-fade-in opacity-0" style={{ animationDelay: "1.5s", animationFillMode: "forwards" }}>
                  Targeting SQLi, XSS, SSRF vectors...
                </div>
              )}

              {mounted && (
                <div className="flex items-center gap-4 mt-2 animate-fade-in opacity-0" style={{ animationDelay: "1.8s", animationFillMode: "forwards" }}>
                  <div className="h-2 w-48 md:w-64 bg-white/10 rounded-full overflow-hidden">
                    <div className="h-full bg-emerald-500 w-[65%] shadow-[0_0_10px_rgba(16,185,129,0.5)] relative">
                      <div className="absolute inset-0 bg-white/20 animate-pulse"></div>
                    </div>
                  </div>
                  <span className="text-emerald-500">65%</span>
                </div>
              )}

              {mounted && (
                <div className="mt-4 text-rose-400 font-semibold max-w-fit px-2 py-1 bg-rose-500/10 border border-rose-500/20 rounded flex items-center gap-2 animate-fade-in opacity-0" style={{ animationDelay: "2.5s", animationFillMode: "forwards" }}>
                  <svg className="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                  <span className="truncate">[CRITICAL] Hardcoded AWS Credentials detected in `utils/auth.ts:145`</span>
                </div>
              )}

              {mounted && (
                <div className="mt-2 text-violet-400 pl-4 border-l border-violet-500/30 animate-fade-in opacity-0" style={{ animationDelay: "3.5s", animationFillMode: "forwards" }}>
                  Synthesizing patch... generating secure Secrets Manager implementation...
                </div>
              )}

              {mounted && (
                <div className="mt-2 text-emerald-500 flex items-center gap-2 animate-fade-in opacity-0" style={{ animationDelay: "4.5s", animationFillMode: "forwards" }}>
                  <svg className="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                  Patch auto-merged to branch `sec-fix-aws-creds`. Security score +15.
                </div>
              )}
            </div>
          </div>
          {/* Glow under dashboard */}
          <div className="absolute -inset-4 md:-inset-10 bg-gradient-to-r from-emerald-500/10 via-violet-500/10 to-emerald-500/10 blur-[80px] md:blur-[120px] -z-10 rounded-[4rem] opacity-50"></div>
        </div>
      </section>

      {/* 2. Social Proof */}
      <section className="py-16 md:py-20 border-y border-white/5 bg-white/[0.01] animate-fade-in opacity-0" style={{ animationDelay: "0.8s", animationFillMode: "forwards" }}>
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p className="text-xs font-semibold text-white/40 tracking-widest uppercase mb-10">Securing hyper-growth engineering teams</p>
          <div className="flex flex-wrap justify-center items-center gap-10 md:gap-20 opacity-50 grayscale hover:grayscale-0 transition-all duration-700">
            {['ACME CORP', 'NEXTGEN', 'QUANTUM_SEC', 'DATASTACK', 'NEXUS', 'SYNAPSE'].map((brand, i) => (
              <span key={i} className="text-xl md:text-2xl font-black font-heading tracking-tighter text-white/80 select-none hover:text-white transition-colors duration-300 cursor-default">{brand}</span>
            ))}
          </div>
        </div>
      </section>

      {/* 3. Bento Grid Features */}
      <section className="py-24 md:py-32 relative z-10 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16 md:mb-24 animate-fade-in opacity-0" style={{ animationFillMode: "forwards" }}>
            <h2 className="text-4xl md:text-6xl font-bold font-heading mb-6 tracking-tight text-white leading-tight">An <span className="text-transparent bg-clip-text bg-gradient-to-r from-white via-neutral-200 to-neutral-500">intelligence layer</span><br />for your codebase.</h2>
            <p className="text-xl text-white/50 max-w-2xl mx-auto leading-relaxed">Stop managing endless alert fatigue. Start <span className="text-emerald-400 font-medium">fixing vulnerabilities</span> at the speed of thought.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 auto-rows-[auto] md:auto-rows-[340px]">
            {/* Large Card */}
            <div className="md:col-span-2 group relative rounded-[2rem] border border-white/10 bg-[#09090b]/50 p-8 md:p-10 overflow-hidden hover:border-white/20 transition-all duration-500 flex flex-col justify-between hover:shadow-[0_0_80px_-20px_rgba(255,255,255,0.05)] animate-fade-in opacity-0" style={{ animationDelay: "0.2s", animationFillMode: "forwards" }}>
              <div className="absolute inset-0 bg-gradient-to-br from-white/[0.03] to-transparent pointer-events-none"></div>
              {/* Abstract element inside */}
              <div className="absolute right-0 bottom-0 w-[500px] h-[500px] bg-emerald-500/5 blur-[120px] rounded-full group-hover:bg-emerald-500/10 transition-colors duration-700 translate-x-1/3 translate-y-1/3"></div>

              <div className="relative z-10">
                <div className="w-14 h-14 rounded-2xl bg-white/10 border border-white/10 flex items-center justify-center text-white backdrop-blur-md shadow-lg mb-8 group-hover:scale-110 transition-transform duration-500 group-hover:bg-white/15">
                  <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
                  </svg>
                </div>
                <h3 className="text-3xl font-bold font-heading text-white mb-4 tracking-tight">Semantic AI Engine</h3>
                <p className="text-white/60 text-lg leading-relaxed max-w-md">Our proprietary model doesn't just look for regex matches. It understands the deep context, data flow, and business logic of your application to surface complex attack vectors that rules-based engines miss.</p>
              </div>
            </div>

            {/* Medium Card 1 */}
            <div className="group relative rounded-[2rem] border border-white/10 bg-[#09090b]/50 p-8 md:p-10 overflow-hidden hover:border-white/20 transition-all duration-500 flex flex-col justify-between hover:shadow-[0_0_80px_-20px_rgba(139,92,246,0.1)] animate-fade-in opacity-0" style={{ animationDelay: "0.4s", animationFillMode: "forwards" }}>
              <div className="absolute top-0 right-0 w-48 h-48 bg-violet-500/10 blur-[60px] rounded-full group-hover:bg-violet-500/20 transition-colors duration-700 -translate-y-1/2 translate-x-1/3"></div>
              <div className="relative z-10">
                <div className="w-14 h-14 rounded-2xl bg-violet-500/10 border border-violet-500/20 flex items-center justify-center text-violet-400 backdrop-blur-md shadow-lg mb-8 group-hover:scale-110 transition-transform duration-500 group-hover:bg-violet-500/20">
                  <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m0-10.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.75c0 5.592 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.57-.598-3.751h-.152c-3.196 0-6.1-1.249-8.25-3.286zm0 13.036h.008v.008H12v-.008z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold font-heading text-white mb-3 tracking-tight">Adversarial Simulation</h3>
                <p className="text-white/60">Watch AI construct multi-step payloads to exploit your specific network configuration dynamically.</p>
              </div>
            </div>

            {/* Medium Card 2 */}
            <div className="group relative rounded-[2rem] border border-white/10 bg-[#09090b]/50 p-8 md:p-10 overflow-hidden hover:border-white/20 transition-all duration-500 flex flex-col justify-between hover:shadow-[0_0_80px_-20px_rgba(16,185,129,0.1)] animate-fade-in opacity-0" style={{ animationDelay: "0.6s", animationFillMode: "forwards" }}>
              <div className="absolute top-0 left-0 w-48 h-48 bg-emerald-500/10 blur-[60px] rounded-full group-hover:bg-emerald-500/20 transition-colors duration-700 -translate-x-1/3 -translate-y-1/3"></div>
              <div className="relative z-10">
                <div className="w-14 h-14 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 backdrop-blur-md shadow-lg mb-8 group-hover:scale-110 transition-transform duration-500 group-hover:bg-emerald-500/20">
                  <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M11.42 15.17l-5.1-5.1m0 0l5.1-5.1m-5.1 5.1h11.13M4.93 19.07A10 10 0 1119.07 4.93 10 10 0 014.93 19.07z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold font-heading text-white mb-3 tracking-tight">Automated Remediation</h3>
                <p className="text-white/60">Stop waiting on engineering tickets. Generate production-ready PRs with verified security patches applied.</p>
              </div>
            </div>

            {/* Wide Bottom Card */}
            <div className="md:col-span-2 group relative rounded-[2rem] border border-white/10 bg-[#09090b]/50 p-8 md:p-10 overflow-hidden hover:border-white/20 transition-all duration-500 flex flex-col md:flex-row items-start md:items-center justify-between gap-8 md:gap-0 hover:shadow-[0_0_80px_-20px_rgba(255,255,255,0.05)] animate-fade-in opacity-0" style={{ animationDelay: "0.8s", animationFillMode: "forwards" }}>
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-full bg-gradient-to-t from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700 rounded-full blur-[100px]"></div>
              <div className="relative z-10 max-w-lg">
                <h3 className="text-2xl font-bold font-heading text-white mb-4 tracking-tight">CI/CD Native Pipeline</h3>
                <p className="text-white/60 text-lg leading-relaxed">Integrates seamlessly into GitHub Actions, GitLab CI, and Bitbucket. Block vulnerable deployments automatically before they reach production.</p>
              </div>
              <div className="relative z-10 hidden md:flex flex-col gap-4 opacity-50 group-hover:opacity-100 transition-opacity duration-500 border border-white/10 bg-black/40 p-6 rounded-2xl w-64 backdrop-blur-md">
                <div className="flex items-center gap-3"><div className="w-2 h-2 rounded-full bg-white/20"></div><div className="h-2 w-32 bg-white/10 rounded-full"></div></div>
                <div className="flex items-center gap-3"><div className="w-2 h-2 rounded-full bg-white/20"></div><div className="h-2 w-48 bg-white/10 rounded-full"></div></div>
                <div className="flex items-center gap-3"><div className="w-2 h-2 rounded-full bg-emerald-500"></div><div className="h-2 w-24 bg-emerald-500/30 rounded-full"></div></div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* 4. Impact / Scale Section */}
      <section className="py-24 md:py-32 border-y border-white/5 bg-gradient-to-b from-[#09090b] to-[#000000]">
        <div className="max-w-6xl mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12 md:gap-0 divide-y md:divide-y-0 md:divide-x divide-white/10 text-center animate-fade-in opacity-0" style={{ animationFillMode: "forwards" }}>
            <div className="pt-8 md:pt-0 group cursor-default">
              <div className="text-5xl md:text-7xl font-bold font-heading text-white mb-4 tracking-tighter group-hover:scale-105 transition-transform duration-300">Zero</div>
              <div className="text-white/40 font-semibold tracking-[0.2em] uppercase text-xs md:text-sm group-hover:text-emerald-400 transition-colors">False Positives (Avg)</div>
            </div>
            <div className="pt-8 md:pt-0 group cursor-default">
              <div className="text-5xl md:text-7xl font-bold font-heading text-white mb-4 tracking-tighter group-hover:scale-105 transition-transform duration-300">&lt; 50<span className="text-3xl md:text-4xl">ms</span></div>
              <div className="text-white/40 font-semibold tracking-[0.2em] uppercase text-xs md:text-sm group-hover:text-violet-400 transition-colors">Inference Latency</div>
            </div>
            <div className="pt-8 md:pt-0 group cursor-default">
              <div className="text-5xl md:text-7xl font-bold font-heading text-white mb-4 tracking-tighter group-hover:scale-105 transition-transform duration-300">100<span className="text-3xl md:text-4xl">%</span></div>
              <div className="text-white/40 font-semibold tracking-[0.2em] uppercase text-xs md:text-sm group-hover:text-amber-400 transition-colors">Automated Triage</div>
            </div>
          </div>
        </div>
      </section>

      {/* 5. Final CTA */}
      <section className="py-32 md:py-48 relative overflow-hidden flex items-center justify-center">
        {/* Deep background glow */}
        <div className="absolute inset-0 bg-emerald-500/5 [mask-image:radial-gradient(ellipse_at_center,black,transparent_70%)] pointer-events-none"></div>
        <div className="absolute inset-x-0 bottom-0 h-px bg-gradient-to-r from-transparent via-emerald-500/30 to-transparent"></div>

        <div className="max-w-4xl mx-auto px-6 text-center relative z-10 flex flex-col items-center">
          <h2 className="text-4xl md:text-7xl font-bold font-heading text-white mb-8 tracking-tighter leading-[1.1] animate-fade-in opacity-0" style={{ animationFillMode: "forwards" }}>Ready to lock down your architecture?</h2>
          <div className="flex flex-col gap-6 items-center animate-fade-in opacity-0" style={{ animationDelay: "0.2s", animationFillMode: "forwards" }}>
            <Link href="/scan" className="group relative inline-flex items-center justify-center px-12 py-5 font-bold text-black transition-all duration-300 bg-white rounded-2xl overflow-hidden hover:scale-105 shadow-[0_0_80px_-15px_rgba(255,255,255,0.4)]">
              <span className="absolute inset-0 w-full h-full bg-gradient-to-br from-white via-white to-neutral-300 transition-all duration-300"></span>
              <span className="relative z-10 flex items-center gap-2 text-lg">
                Get Started for Free
                <svg className="w-5 h-5 transition-transform group-hover:rotate-45" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
              </span>
            </Link>
            <div className="text-white/40 text-sm font-medium tracking-wide">No credit card required. Cancel anytime.</div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 py-12 px-6 bg-[#000000]">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between text-sm">
          <div className="flex items-center gap-2 mb-4 md:mb-0">
            <div className="w-6 h-6 rounded bg-white flex items-center justify-center">
              <svg className="w-4 h-4 text-black" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
              </svg>
            </div>
            <span className="font-bold text-white font-heading tracking-tight">VulnGuard AI</span>
          </div>
          <p className="text-white/40 mb-4 md:mb-0 md:absolute md:left-1/2 md:-translate-x-1/2">
            © 2026 VulnGuard Security. All rights reserved.
          </p>
          <div className="flex items-center gap-8 text-white/50">
            <a href="#" className="hover:text-white transition-colors">Documentation</a>
            <a href="#" className="hover:text-white transition-colors">GitHub</a>
            <a href="#" className="hover:text-white transition-colors">Twitter</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
