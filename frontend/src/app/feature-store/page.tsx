'use client';
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
