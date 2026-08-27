export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
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
