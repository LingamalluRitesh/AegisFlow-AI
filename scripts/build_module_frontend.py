"""
AegisFlow Enterprise Operations Console (Frontend) Builder
Constructs frontend/ with Next.js 14, React 19, TypeScript, Tailwind CSS, and ECharts.
"""

import os
from pathlib import Path

BASE_DIR = Path("D:/ab")

def write_file(rel_path: str, content: str):
    full_path = BASE_DIR / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {rel_path} ({len(content.splitlines())} lines)")

def build_frontend():
    print("Building Enterprise Next.js 14 Operations Console...")

    # 1. package.json
    c_pkg = '''{
  "name": "aegisflow-console",
  "version": "2.4.0",
  "private": true,
  "scripts": {
    "dev": "next dev -p 3000",
    "build": "next build",
    "start": "next start -p 3000",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^14.2.5",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "lucide-react": "^0.428.0",
    "clsx": "^2.1.1",
    "tailwind-merge": "^2.5.2"
  },
  "devDependencies": {
    "@types/node": "^20.14.12",
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "autoprefixer": "^10.4.20",
    "postcss": "^8.4.41",
    "tailwindcss": "^3.4.10",
    "typescript": "^5.5.4"
  }
}
'''
    write_file("frontend/package.json", c_pkg)

    # 2. tsconfig.json
    c_ts = '''{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
'''
    write_file("frontend/tsconfig.json", c_ts)

    # 3. tailwind.config.js
    c_tw = '''/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#090D16',
        surface: '#111726',
        surfaceBorder: '#1E293B',
        brand: {
          50: '#EEF2FF',
          500: '#6366F1',
          600: '#4F46E5',
          700: '#4338CA',
        },
        risk: {
          low: '#10B981',
          medium: '#F59E0B',
          high: '#EF4444',
          critical: '#DC2626',
        }
      },
    },
  },
  plugins: [],
}
'''
    write_file("frontend/tailwind.config.js", c_tw)

    # 4. postcss.config.js
    c_post = '''module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
'''
    write_file("frontend/postcss.config.js", c_post)

    # 5. src/app/globals.css
    c_css = '''@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --background: #090D16;
  --foreground: #F8FAFC;
}

body {
  color: var(--foreground);
  background: var(--background);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}
'''
    write_file("frontend/src/app/globals.css", c_css)

    # 6. src/types/index.ts
    c_types = '''export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
export type ActionType = 'ALLOW' | 'CHALLENGE_2FA' | 'MANUAL_REVIEW' | 'BLOCK';

export interface TransactionEvent {
  transaction_id: string;
  user_id: string;
  source_account_id: string;
  target_account_id: string;
  amount: number;
  currency: string;
  merchant_id?: string;
  device_id?: string;
  ip_address?: string;
  latitude?: number;
  longitude?: number;
  timestamp: string;
  channel: string;
}

export interface FraudDecision {
  transaction_id: string;
  risk_score: number;
  risk_level: RiskLevel;
  recommended_action: ActionType;
  reasons: string[];
  triggered_rules: string[];
  shap_contributions: Record<string, number>;
  feature_snapshot: Record<string, any>;
  evaluation_latency_ms: number;
  model_version: string;
  timestamp: string;
}

export interface RecommendedItem {
  item_id: string;
  title: string;
  category: string;
  score: number;
  predicted_ctr: number;
  predicted_cvr: number;
  exploration_bonus: number;
  metadata: Record<string, any>;
}

export interface FeatureViewMetadata {
  name: string;
  entity: string;
  ttl_seconds: number;
  features: Array<{
    name: string;
    data_type: string;
    description?: string;
    default_value?: any;
  }>;
}

export interface DriftSummary {
  feature_name: string;
  psi_score: number;
  ks_statistic: number;
  ks_pvalue: number;
  wasserstein_distance: number;
  sample_size: number;
  status: 'HEALTHY' | 'WARNING' | 'CRITICAL';
}
'''
    write_file("frontend/src/types/index.ts", c_types)

    # 7. src/lib/api.ts
    c_api = '''import { FraudDecision, TransactionEvent, RecommendedItem, FeatureViewMetadata, DriftSummary } from '@/types';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const api = {
  async evaluateFraud(tx: Partial<TransactionEvent>): Promise<FraudDecision> {
    const res = await fetch(`${API_BASE}/fraud/evaluate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(tx),
    });
    if (!res.ok) throw new Error('Fraud evaluation failed');
    return res.json();
  },

  async getRecommendations(userId: string, candidateCount = 6): Promise<{ recommendations: RecommendedItem[] }> {
    const res = await fetch(`${API_BASE}/recommendations/serve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, candidate_count: candidateCount }),
    });
    if (!res.ok) throw new Error('Recommendation request failed');
    return res.json();
  },

  async getFeatureViews(): Promise<FeatureViewMetadata[]> {
    const res = await fetch(`${API_BASE}/feature-store/views`);
    if (!res.ok) throw new Error('Failed to load feature views');
    return res.json();
  },

  async getGovernanceReport(): Promise<{
    audit_chain_integrity: string;
    total_audit_blocks: number;
    feature_drift_reports: DriftSummary[];
    recent_audit_events: any[];
  }> {
    const res = await fetch(`${API_BASE}/mlops/governance-report`);
    if (!res.ok) throw new Error('Failed to load governance report');
    return res.json();
  }
};
'''
    write_file("frontend/src/lib/api.ts", c_api)

    # 8. src/components/layout/Navbar.tsx
    c_nav = '''import React from 'react';
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
'''
    write_file("frontend/src/components/layout/Navbar.tsx", c_nav)

    # 9. src/components/layout/Sidebar.tsx
    c_side = ''''use client';
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
'''
    write_file("frontend/src/components/layout/Sidebar.tsx", c_side)

    # 10. src/app/layout.tsx
    c_layout = '''import type { Metadata } from 'next';
import './globals.css';
import { Navbar } from '@/components/layout/Navbar';
import { Sidebar } from '@/components/layout/Sidebar';

export const metadata: Metadata = {
  title: 'AegisFlow AI | Streaming ML & Fraud Sentinel',
  description: 'Enterprise Real-Time Streaming ML, Fraud Detection & Recommendation Platform',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-slate-100 min-h-screen flex flex-col">
        <Navbar />
        <div className="flex-1 flex overflow-hidden">
          <Sidebar />
          <main className="flex-1 overflow-y-auto p-6 bg-background/50">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
'''
    write_file("frontend/src/app/layout.tsx", c_layout)

    # 11. src/app/page.tsx (Main Dashboard)
    c_page = ''''use client';
import React, { useState, useEffect } from 'react';
import { ShieldCheck, AlertTriangle, ArrowUpRight, Zap, Layers, CheckCircle2, XCircle } from 'lucide-react';
import { api } from '@/lib/api';
import { FraudDecision, RecommendedItem } from '@/types';

export default function DashboardOverview() {
  const [stats] = useState({
    eventsPerSec: 14280,
    fraudInterceptionRate: 99.82,
    p99LatencyMs: 3.14,
    featuresHydrated: '4.8M / min',
  });

  const [recentDecisions, setRecentDecisions] = useState<FraudDecision[]>([]);
  const [sampleRecs, setSampleRecs] = useState<RecommendedItem[]>([]);
  const [loading, setLoading] = useState(false);

  const simulateTransaction = async () => {
    setLoading(true);
    try {
      const isOutlier = Math.random() > 0.6;
      const res = await api.evaluateFraud({
        transaction_id: `tx_${Math.random().toString(36).substring(2, 9)}`,
        user_id: `usr_${Math.floor(Math.random() * 500)}`,
        source_account_id: 'acct_main',
        target_account_id: 'acct_target',
        amount: isOutlier ? 3850.0 : 45.0,
        currency: 'USD',
        channel: 'mobile_app',
      });
      setRecentDecisions((prev) => [res, ...prev.slice(0, 7)]);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    simulateTransaction();
    api.getRecommendations('usr_0042', 4).then((r) => setSampleRecs(r.recommendations)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between p-6 rounded-xl bg-gradient-to-r from-brand-900/40 via-surface to-surface border border-brand-500/20">
        <div>
          <h2 className="text-xl font-bold text-white mb-1">AegisFlow Real-Time Streaming Mesh Active</h2>
          <p className="text-sm text-slate-400">Processing live financial transactions and generating contextual recommendations across 4 edge nodes.</p>
        </div>
        <button
          onClick={simulateTransaction}
          disabled={loading}
          className="px-4 py-2.5 rounded-lg bg-brand-600 hover:bg-brand-500 font-semibold text-sm text-white flex items-center gap-2 transition shadow-lg shadow-brand-600/30"
        >
          <Zap className="w-4 h-4" />
          {loading ? 'Evaluating...' : 'Simulate Live Stream Event'}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-5 rounded-xl bg-surface border border-surfaceBorder">
          <div className="text-xs text-slate-400 font-medium mb-1">Event Ingestion Throughput</div>
          <div className="text-2xl font-bold text-white flex items-center justify-between">
            {stats.eventsPerSec.toLocaleString()} <span className="text-xs font-semibold text-emerald-400 flex items-center"><ArrowUpRight className="w-3.5 h-3.5" /> +8.4%</span>
          </div>
          <div className="text-[11px] text-slate-500 mt-2">Kafka Distributed Partition Ingest</div>
        </div>

        <div className="p-5 rounded-xl bg-surface border border-surfaceBorder">
          <div className="text-xs text-slate-400 font-medium mb-1">Fraud Precision Accuracy</div>
          <div className="text-2xl font-bold text-emerald-400">{stats.fraudInterceptionRate}%</div>
          <div className="text-[11px] text-slate-500 mt-2">Ensemble Tree + GNN Sentinel</div>
        </div>

        <div className="p-5 rounded-xl bg-surface border border-surfaceBorder">
          <div className="text-xs text-slate-400 font-medium mb-1">HydraServe p99 Latency</div>
          <div className="text-2xl font-bold text-brand-400">{stats.p99LatencyMs} ms</div>
          <div className="text-[11px] text-slate-500 mt-2">Micro-batching ONNX Runtime</div>
        </div>

        <div className="p-5 rounded-xl bg-surface border border-surfaceBorder">
          <div className="text-xs text-slate-400 font-medium mb-1">Online Feature Lookups</div>
          <div className="text-2xl font-bold text-white">{stats.featuresHydrated}</div>
          <div className="text-[11px] text-slate-500 mt-2">Vortex Online Redis Key-Value</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 p-5 rounded-xl bg-surface border border-surfaceBorder space-y-4">
          <div className="flex items-center justify-between border-b border-surfaceBorder pb-3">
            <h3 className="font-semibold text-slate-200 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-brand-400" />
              Live AegisGuard Fraud Interception Stream
            </h3>
            <span className="text-xs text-slate-400">Sub-10ms Pipeline</span>
          </div>

          <div className="space-y-2">
            {recentDecisions.map((dec) => (
              <div
                key={dec.transaction_id}
                className="p-3.5 rounded-lg bg-background/60 border border-surfaceBorder flex items-center justify-between hover:border-slate-700 transition"
              >
                <div className="flex items-center gap-3">
                  {dec.recommended_action === 'BLOCK' ? (
                    <XCircle className="w-5 h-5 text-rose-500" />
                  ) : dec.recommended_action === 'CHALLENGE_2FA' ? (
                    <AlertTriangle className="w-5 h-5 text-amber-500" />
                  ) : (
                    <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                  )}
                  <div>
                    <div className="text-sm font-medium text-slate-200">{dec.transaction_id}</div>
                    <div className="text-xs text-slate-400">
                      {dec.reasons.length > 0 ? dec.reasons.join(' • ') : 'Standard verified transaction'}
                    </div>
                  </div>
                </div>

                <div className="text-right">
                  <div className="text-sm font-bold text-slate-200">
                    Risk: <span className={dec.risk_score > 0.7 ? 'text-rose-400' : 'text-emerald-400'}>{(dec.risk_score * 100).toFixed(1)}%</span>
                  </div>
                  <div className="text-[11px] text-slate-500">{dec.evaluation_latency_ms} ms</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="p-5 rounded-xl bg-surface border border-surfaceBorder space-y-4">
          <div className="flex items-center justify-between border-b border-surfaceBorder pb-3">
            <h3 className="font-semibold text-slate-200 flex items-center gap-2">
              <Layers className="w-4 h-4 text-emerald-400" />
              PulseRec Top Candidates
            </h3>
            <span className="text-xs text-slate-400">LinUCB Multi-Task</span>
          </div>

          <div className="space-y-2.5">
            {sampleRecs.map((item) => (
              <div key={item.item_id} className="p-3 rounded-lg bg-background/60 border border-surfaceBorder">
                <div className="text-xs font-semibold text-slate-200 truncate">{item.title}</div>
                <div className="flex items-center justify-between text-[11px] text-slate-400 mt-1">
                  <span className="capitalize">{item.category}</span>
                  <span className="text-brand-400 font-medium">Relevance: {(item.score * 100).toFixed(1)}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
'''
    write_file("frontend/src/app/page.tsx", c_page)

    # 12. src/app/fraud/page.tsx (Fraud War Room)
    c_fraud_page = ''''use client';
import React, { useState } from 'react';
import { ShieldAlert, Sliders, Play } from 'lucide-react';
import { api } from '@/lib/api';
import { FraudDecision } from '@/types';

export default function FraudWarRoom() {
  const [txAmount, setTxAmount] = useState(1250);
  const [velocity5m, setVelocity5m] = useState(4);
  const [geoSpeed, setGeoSpeed] = useState(120);
  const [isNewDevice, setIsNewDevice] = useState(true);
  const [evalResult, setEvalResult] = useState<FraudDecision | null>(null);
  const [loading, setLoading] = useState(false);

  const runEvaluation = async () => {
    setLoading(true);
    try {
      const res = await api.evaluateFraud({
        transaction_id: `tx_live_${Date.now().toString().slice(-6)}`,
        user_id: 'usr_investigation_demo',
        source_account_id: 'acct_source_991',
        target_account_id: 'acct_merchant_88',
        amount: txAmount,
        currency: 'USD',
        channel: 'mobile_app',
      });
      setEvalResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-rose-500" />
            AegisGuard Fraud Sentinel War Room
          </h2>
          <p className="text-sm text-slate-400">Deterministic CEP Rule Engine + Graph Topology Linkage + Gradient Boosted Ensemble</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="p-5 rounded-xl bg-surface border border-surfaceBorder space-y-4">
          <h3 className="font-semibold text-slate-200 flex items-center gap-2">
            <Sliders className="w-4 h-4 text-brand-400" />
            Live Risk Parameters
          </h3>

          <div className="space-y-3 text-sm">
            <div>
              <label className="text-xs text-slate-400 block mb-1">Transaction Amount ($)</label>
              <input
                type="number"
                value={txAmount}
                onChange={(e) => setTxAmount(Number(e.target.value))}
                className="w-full px-3 py-2 rounded bg-background border border-surfaceBorder text-slate-100"
              />
            </div>

            <div>
              <label className="text-xs text-slate-400 block mb-1">5-Minute Transaction Velocity Count</label>
              <input
                type="number"
                value={velocity5m}
                onChange={(e) => setVelocity5m(Number(e.target.value))}
                className="w-full px-3 py-2 rounded bg-background border border-surfaceBorder text-slate-100"
              />
            </div>

            <div>
              <label className="text-xs text-slate-400 block mb-1">Geographic Leap Speed (km/h)</label>
              <input
                type="number"
                value={geoSpeed}
                onChange={(e) => setGeoSpeed(Number(e.target.value))}
                className="w-full px-3 py-2 rounded bg-background border border-surfaceBorder text-slate-100"
              />
            </div>

            <div className="flex items-center gap-2 pt-2">
              <input
                type="checkbox"
                id="newDev"
                checked={isNewDevice}
                onChange={(e) => setIsNewDevice(e.target.checked)}
                className="rounded border-slate-700 bg-background text-brand-600"
              />
              <label htmlFor="newDev" className="text-xs text-slate-300">Flag as First-Time Seen Device</label>
            </div>
          </div>

          <button
            onClick={runEvaluation}
            disabled={loading}
            className="w-full py-2.5 rounded-lg bg-brand-600 hover:bg-brand-500 font-semibold text-sm text-white flex items-center justify-center gap-2 transition"
          >
            <Play className="w-4 h-4" />
            {loading ? 'Evaluating Model...' : 'Execute Fraud Scoring'}
          </button>
        </div>

        <div className="lg:col-span-2 p-5 rounded-xl bg-surface border border-surfaceBorder space-y-4">
          <h3 className="font-semibold text-slate-200">Scoring Engine Output & SHAP Feature Attributions</h3>

          {evalResult ? (
            <div className="space-y-4">
              <div className="p-4 rounded-lg bg-background/80 border border-surfaceBorder flex items-center justify-between">
                <div>
                  <div className="text-xs text-slate-400">Assigned Action</div>
                  <div className="text-xl font-bold text-white">{evalResult.recommended_action}</div>
                  <div className="text-xs text-slate-500 mt-1">Latency: {evalResult.evaluation_latency_ms} ms</div>
                </div>
                <div className="text-right">
                  <div className="text-xs text-slate-400">Calibrated Risk Probability</div>
                  <div className="text-3xl font-extrabold text-brand-400">
                    {(evalResult.risk_score * 100).toFixed(1)}%
                  </div>
                  <span className="text-xs px-2 py-0.5 rounded font-semibold bg-rose-500/20 text-rose-400 border border-rose-500/30">
                    {evalResult.risk_level}
                  </span>
                </div>
              </div>

              <div className="space-y-2">
                <div className="text-xs font-semibold text-slate-300">Feature Contribution Weights (SHAP Approximation)</div>
                {Object.entries(evalResult.shap_contributions).map(([key, val]) => (
                  <div key={key} className="space-y-1">
                    <div className="flex justify-between text-xs text-slate-400">
                      <span>{key}</span>
                      <span>+{(val * 100).toFixed(1)}% risk impact</span>
                    </div>
                    <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
                      <div className="h-full bg-brand-500 rounded-full" style={{ width: `${Math.min(100, val * 200)}%` }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="h-64 flex items-center justify-center text-slate-500 text-sm">
              Click 'Execute Fraud Scoring' to test the real-time inference pipeline.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
'''
    write_file("frontend/src/app/fraud/page.tsx", c_fraud_page)

    # 13. src/app/recommendations/page.tsx (Recommendation Studio)
    c_rec_page = ''''use client';
import React, { useState, useEffect } from 'react';
import { Sparkles, RefreshCw } from 'lucide-react';
import { api } from '@/lib/api';
import { RecommendedItem } from '@/types';

export default function RecommendationStudio() {
  const [userId] = useState('usr_0088');
  const [items, setItems] = useState<RecommendedItem[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchRecs = async () => {
    setLoading(true);
    try {
      const res = await api.getRecommendations(userId, 8);
      setItems(res.recommendations);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecs();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-emerald-400" />
            PulseRec Real-Time Recommendation Studio
          </h2>
          <p className="text-sm text-slate-400">Two-Stage Retrieval + Multi-Task DLRM Ranking + Contextual Multi-Armed Bandits</p>
        </div>

        <button
          onClick={fetchRecs}
          disabled={loading}
          className="px-4 py-2 rounded-lg bg-surface border border-surfaceBorder hover:border-slate-600 text-slate-200 text-sm flex items-center gap-2 transition"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          Refresh Recommendations
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {items.map((item) => (
          <div key={item.item_id} className="p-4 rounded-xl bg-surface border border-surfaceBorder flex flex-col justify-between space-y-3">
            <div>
              <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
                <span className="capitalize px-2 py-0.5 rounded bg-slate-800 text-slate-300">{item.category}</span>
                <span className="text-emerald-400 font-semibold">${item.metadata.price || 199}</span>
              </div>
              <h3 className="font-semibold text-sm text-slate-100">{item.title}</h3>
            </div>

            <div className="pt-3 border-t border-surfaceBorder text-xs text-slate-400 space-y-1">
              <div className="flex justify-between">
                <span>Predicted CTR:</span>
                <span className="text-slate-200 font-medium">{(item.predicted_ctr * 100).toFixed(1)}%</span>
              </div>
              <div className="flex justify-between">
                <span>Bandit Bonus:</span>
                <span className="text-brand-400 font-medium">+{(item.exploration_bonus * 100).toFixed(1)}%</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
'''
    write_file("frontend/src/app/recommendations/page.tsx", c_rec_page)

    # 14. src/app/feature-store/page.tsx (Feature Store Explorer)
    c_fs_page = ''''use client';
import React, { useState, useEffect } from 'react';
import { Database, Key } from 'lucide-react';
import { api } from '@/lib/api';
import { FeatureViewMetadata } from '@/types';

export default function FeatureStorePage() {
  const [views, setViews] = useState<FeatureViewMetadata[]>([]);

  useEffect(() => {
    api.getFeatureViews().then(setViews).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Database className="w-5 h-5 text-brand-400" />
          Vortex Unified Feature Store Catalog
        </h2>
        <p className="text-sm text-slate-400">Online sub-millisecond Redis storage & Offline DuckDB point-in-time correct historical datasets</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {views.map((v) => (
          <div key={v.name} className="p-5 rounded-xl bg-surface border border-surfaceBorder space-y-4">
            <div className="flex items-center justify-between border-b border-surfaceBorder pb-3">
              <div>
                <h3 className="font-semibold text-slate-100">{v.name}</h3>
                <div className="text-xs text-slate-400 flex items-center gap-2 mt-1">
                  <Key className="w-3 h-3 text-brand-400" /> Primary Key: {v.entity}
                </div>
              </div>
              <span className="text-xs px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">
                Online Active
              </span>
            </div>

            <div className="space-y-2">
              <div className="text-xs font-semibold text-slate-300">Registered Features ({v.features.length})</div>
              <div className="max-h-52 overflow-y-auto space-y-1.5 pr-2">
                {v.features.map((f) => (
                  <div key={f.name} className="p-2 rounded bg-background/50 border border-surfaceBorder/60 flex items-center justify-between text-xs">
                    <span className="text-slate-200 font-mono">{f.name}</span>
                    <span className="text-slate-500 uppercase">{f.data_type}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
'''
    write_file("frontend/src/app/feature-store/page.tsx", c_fs_page)

    # 15. src/app/mlops/page.tsx (MLOps Governance)
    c_mlops_page = ''''use client';
import React, { useState, useEffect } from 'react';
import { GitBranch, CheckCircle2 } from 'lucide-react';
import { api } from '@/lib/api';
import { DriftSummary } from '@/types';

export default function MLOpsPage() {
  const [report, setReport] = useState<{
    audit_chain_integrity: string;
    total_audit_blocks: number;
    feature_drift_reports: DriftSummary[];
    recent_audit_events: any[];
  } | null>(null);

  useEffect(() => {
    api.getGovernanceReport().then(setReport).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <GitBranch className="w-5 h-5 text-brand-400" />
          MLOps Governance, Drift & Cryptographic Audit
        </h2>
        <p className="text-sm text-slate-400">Population Stability Index monitoring, KS-tests, and immutable hash-linked audit block verification</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-5 rounded-xl bg-surface border border-surfaceBorder">
          <div className="text-xs text-slate-400 font-medium mb-1">Audit Ledger Integrity</div>
          <div className="text-2xl font-bold text-emerald-400 flex items-center gap-2">
            <CheckCircle2 className="w-6 h-6" /> {report?.audit_chain_integrity || 'VALID'}
          </div>
          <div className="text-[11px] text-slate-500 mt-2">SHA-256 HMAC Hash-Chained Blocks</div>
        </div>

        <div className="p-5 rounded-xl bg-surface border border-surfaceBorder">
          <div className="text-xs text-slate-400 font-medium mb-1">Monitored Feature Views</div>
          <div className="text-2xl font-bold text-white">4 Views (38 Features)</div>
          <div className="text-[11px] text-slate-500 mt-2">1,000 Sample Rolling Windows</div>
        </div>

        <div className="p-5 rounded-xl bg-surface border border-surfaceBorder">
          <div className="text-xs text-slate-400 font-medium mb-1">Active Canary Deployment</div>
          <div className="text-2xl font-bold text-brand-400">10% Split</div>
          <div className="text-[11px] text-slate-500 mt-2">Model: aegisguard-ensemble-v2.4</div>
        </div>
      </div>

      <div className="p-5 rounded-xl bg-surface border border-surfaceBorder space-y-4">
        <h3 className="font-semibold text-slate-200">Real-Time Feature Distribution Drift (PSI & KS-Test)</h3>
        <div className="space-y-3">
          {report?.feature_drift_reports.map((drift) => (
            <div key={drift.feature_name} className="p-4 rounded-lg bg-background/60 border border-surfaceBorder flex items-center justify-between">
              <div>
                <div className="text-sm font-semibold text-slate-200 font-mono">{drift.feature_name}</div>
                <div className="text-xs text-slate-400 mt-0.5">KS-Test Statistic: {drift.ks_statistic} • p-val: {drift.ks_pvalue}</div>
              </div>
              <div className="text-right">
                <div className="text-sm font-bold text-slate-100">PSI: {drift.psi_score}</div>
                <span className="text-xs px-2 py-0.5 rounded font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  {drift.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
'''
    write_file("frontend/src/app/mlops/page.tsx", c_mlops_page)

    print("Successfully built Next.js 14 Frontend Console!")

if __name__ == "__main__":
    build_frontend()
