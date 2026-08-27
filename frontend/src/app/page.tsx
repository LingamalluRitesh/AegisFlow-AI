'use client';
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
