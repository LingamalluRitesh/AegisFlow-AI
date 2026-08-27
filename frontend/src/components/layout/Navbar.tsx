import React from 'react';
import { ShieldCheck, Cpu, Bell } from 'lucide-react';

export const Navbar = () => {
  return (
    <header className="h-16 border-b border-surfaceBorder bg-surface/50 backdrop-blur px-6 flex items-center justify-between sticky top-0 z-50">
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-lg bg-brand-600/20 border border-brand-500/30 text-brand-500">
          <ShieldCheck className="w-6 h-6" />
        </div>
        <div>
          <h1 className="font-bold text-lg text-slate-100 flex items-center gap-2">
            AegisFlow AI <span className="text-xs px-2 py-0.5 rounded bg-brand-500/10 text-brand-400 border border-brand-500/20">Enterprise v2.4</span>
          </h1>
          <p className="text-xs text-slate-400">Streaming ML, Fraud Sentinel & Recommendation Mesh</p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          Stream Pipeline: 12,450 eps
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-300 text-xs">
          <Cpu className="w-3.5 h-3.5" />
          p99 Latency: 3.2ms
        </div>
        <button className="p-2 rounded-lg bg-surface border border-surfaceBorder text-slate-300 hover:text-white hover:border-slate-600 transition">
          <Bell className="w-4 h-4" />
        </button>
      </div>
    </header>
  );
};
