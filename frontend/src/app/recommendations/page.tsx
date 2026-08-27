'use client';
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
