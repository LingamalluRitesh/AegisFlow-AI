/**
 * AegisFlow TypeScript Client SDK
 * Browser and Node.js client for real-time fraud scoring and recommendations.
 */

export interface TransactionPayload {
  transaction_id: string;
  user_id: string;
  source_account_id: string;
  target_account_id: string;
  amount: number;
  currency?: string;
  device_id?: string;
  ip_address?: string;
}

export interface FraudDecision {
  transaction_id: string;
  risk_score: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  recommended_action: 'ALLOW' | 'CHALLENGE_2FA' | 'MANUAL_REVIEW' | 'BLOCK';
  reasons: string[];
  evaluation_latency_ms: number;
}

export class AegisFlowClient {
  private endpoint: string;
  private apiKey?: string;

  constructor(endpoint = 'http://localhost:8000/api/v1', apiKey?: string) {
    this.endpoint = endpoint.replace(/\/$/, '');
    this.apiKey = apiKey;
  }

  async evaluateFraud(tx: TransactionPayload): Promise<FraudDecision> {
    const res = await fetch(`${this.endpoint}/fraud/evaluate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(this.apiKey ? { Authorization: `Bearer ${this.apiKey}` } : {}),
      },
      body: JSON.stringify(tx),
    });
    if (!res.ok) throw new Error(`AegisFlow Error: ${res.statusText}`);
    return res.json();
  }
}
