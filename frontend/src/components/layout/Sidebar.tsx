'use client';
import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, ShieldAlert, Sparkles, Database, GitBranch } from 'lucide-react';

const navigation = [
  { name: 'Overview Console', href: '/', icon: LayoutDashboard },
  { name: 'Fraud War Room', href: '/fraud', icon: ShieldAlert },
  { name: 'Recommendation Studio', href: '/recommendations', icon: Sparkles },
  { name: 'Vortex Feature Store', href: '/feature-store', icon: Database },
  { name: 'MLOps & Governance', href: '/mlops', icon: GitBranch },
];

export const Sidebar = () => {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-surfaceBorder bg-surface/30 p-4 flex flex-col justify-between">
      <div className="space-y-1">
        <div className="px-3 py-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
          Subsystems
        </div>
        {navigation.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition ${
                isActive
                  ? 'bg-brand-600 text-white shadow-lg shadow-brand-600/20'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-surface'
              }`}
            >
              <Icon className="w-4 h-4" />
              {item.name}
            </Link>
          );
        })}
      </div>

      <div className="p-3 rounded-lg bg-surface border border-surfaceBorder text-xs text-slate-400">
        <div className="flex items-center justify-between mb-1">
          <span className="font-medium text-slate-200">Cluster Status</span>
          <span className="text-emerald-400 font-semibold">100% OK</span>
        </div>
        <p className="text-[11px] text-slate-500">6 Microservices Healthy</p>
      </div>
    </aside>
  );
};
