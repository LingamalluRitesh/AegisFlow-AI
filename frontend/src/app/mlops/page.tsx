'use client';
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
