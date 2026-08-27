// Package aegisflow provides the official high-performance Go client SDK for AegisFlow.
package aegisflow

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

// TransactionPayload represents a financial transaction to be scored in real time.
type TransactionPayload struct {
	TransactionID   string  `json:"transaction_id"`
	UserID          string  `json:"user_id"`
	SourceAccountID string  `json:"source_account_id"`
	TargetAccountID string  `json:"target_account_id"`
	Amount          float64 `json:"amount"`
	Currency        string  `json:"currency"`
	DeviceID        string  `json:"device_id,omitempty"`
	IPAddress       string  `json:"ip_address,omitempty"`
}

// FraudDecision represents the sub-10ms evaluation output from AegisGuard.
type FraudDecision struct {
	TransactionID       string             `json:"transaction_id"`
	RiskScore           float64            `json:"risk_score"`
	RiskLevel           string             `json:"risk_level"`
	RecommendedAction   string             `json:"recommended_action"`
	Reasons             []string           `json:"reasons"`
	EvaluationLatencyMS float64            `json:"evaluation_latency_ms"`
	SHAPContributions   map[string]float64 `json:"shap_contributions"`
}

// Client provides an HTTP client interface with connection pooling.
type Client struct {
	Endpoint   string
	APIKey     string
	HTTPClient *http.Client
}

// NewClient initializes a new AegisFlow SDK client instance.
func NewClient(endpoint, apiKey string) *Client {
	return &Client{
		Endpoint: endpoint,
		APIKey:   apiKey,
		HTTPClient: &http.Client{
			Timeout: 5 * time.Second,
			Transport: &http.Transport{
				MaxIdleConns:        100,
				MaxIdleConnsPerHost: 20,
				IdleConnTimeout:     90 * time.Second,
			},
		},
	}
}

// EvaluateFraud sends a transaction for real-time fraud scoring.
func (c *Client) EvaluateFraud(ctx context.Context, tx TransactionPayload) (*FraudDecision, error) {
	data, err := json.Marshal(tx)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal transaction payload: %w", err)
	}

	req, err := http.NewRequestWithContext(ctx, http.MethodPost, c.Endpoint+"/fraud/evaluate", bytes.NewReader(data))
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	req.Header.Set("Content-Type", "application/json")
	if c.APIKey != "" {
		req.Header.Set("Authorization", "Bearer "+c.APIKey)
	}

	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("http request failed: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("aegisflow server returned status %d", resp.StatusCode)
	}

	var decision FraudDecision
	if err := json.NewDecoder(resp.Body).Decode(&decision); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	return &decision, nil
}
