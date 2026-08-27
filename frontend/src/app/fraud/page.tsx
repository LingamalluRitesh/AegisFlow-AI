'use client';
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
