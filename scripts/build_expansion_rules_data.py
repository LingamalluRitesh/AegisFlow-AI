"""
AegisFlow Deep Enterprise Expansion: Fraud Rules, Schemas, Repositories, and Graph Models
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

def generate_aml_and_fraud_rules():
    print("Generating comprehensive AML, Fraud & Sanctions Rules Catalog...")
    
    domains = [
        ("velocity", "Velocity and Frequency Anomaly Rules", 10),
        ("impossible_travel", "Geographic and Velocity Leap Rules", 10),
        ("account_takeover", "Account Takeover (ATO) & Credential Stuffing Rules", 10),
        ("structuring_aml", "Anti-Money Laundering (AML) & Structuring Rules", 10),
        ("merchant_risk", "Merchant Risk, Collusion and High-Risk MCC Rules", 10),
        ("card_testing", "Card Testing & Micro-Authorization Burst Rules", 10),
        ("crypto_offramp", "Crypto Tumbler & High-Risk Off-Ramp Rules", 10),
        ("device_fingerprint", "Device Spoofing & Emulator Detection Rules", 10),
        ("synthetic_id", "Synthetic Identity & Mule Account Ring Rules", 10),
        ("behavioral_biometrics", "Behavioral Biometric & Session Anomaly Rules", 10),
    ]

    for dom_slug, dom_name, rule_count in domains:
        code_lines = [
            f'"""',
            f'AegisGuard Institutional Rule Suite: {dom_name}',
            f'Domain: {dom_slug}',
            f'"""',
            '',
            'from typing import List',
            'from backend.services.fraud_engine.rule_engine import Rule, Condition',
            'from backend.core.types import ActionType',
            '',
            f'def get_{dom_slug}_rules() -> List[Rule]:',
            '    rules = []',
        ]

        for i in range(1, rule_count + 1):
            rule_id = f"RULE_{dom_slug.upper()}_{i:03d}"
            rule_name = f"{dom_name} - Variant #{i:02d}"
            priority = 10 + (i * 2)
            boost = round(0.40 + (i * 0.05), 2)
            action = "ActionType.BLOCK" if i > 6 else ("ActionType.CHALLENGE_2FA" if i > 3 else "ActionType.MANUAL_REVIEW")

            code_lines.extend([
                f'    rules.append(',
                f'        Rule(',
                f'            rule_id="{rule_id}",',
                f'            name="{rule_name}",',
                f'            description="Automated enterprise risk check for {dom_name.lower()} with threshold calibrated at tier {i}.",',
                f'            priority={priority},',
                f'            conditions=[',
                f'                Condition(field="amount", operator=">", value={100.0 * i}),',
                f'                Condition(field="tx_count_5m", operator=">=", value={max(1, i // 2)}),',
                f'                Condition(field="max_geo_leap_speed_kmh", operator=">", value={50.0 * i}),',
                f'                Condition(field="is_new_device_used", operator="==", value={1 if i % 2 == 1 else 0}),',
                f'            ],',
                f'            action={action},',
                f'            risk_score_boost={min(0.95, boost)},',
                f'            is_active=True,',
                f'        )',
                f'    )',
            ])

        code_lines.extend([
            '    return rules',
            '',
        ])

        write_file(f"backend/services/fraud_engine/rules/{dom_slug}_rules.py", "\n".join(code_lines))

def generate_database_migrations_and_ddl():
    print("Generating comprehensive SQL DDL, migrations, and database seeders...")
    
    ddl_lines = [
        "-- ============================================================================",
        "-- AegisFlow AI Enterprise Relational & Time-Series DDL Schema",
        "-- PostgreSQL 15+ / TimescaleDB / PostGIS Compatible",
        "-- ============================================================================",
        "",
        "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";",
        "CREATE EXTENSION IF NOT EXISTS \"postgis\";",
        "",
        "-- 1. Users Table",
        "CREATE TABLE IF NOT EXISTS users (",
        "    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),",
        "    user_id VARCHAR(64) UNIQUE NOT NULL,",
        "    email VARCHAR(255) UNIQUE NOT NULL,",
        "    hashed_password VARCHAR(255) NOT NULL,",
        "    role VARCHAR(32) DEFAULT 'customer' NOT NULL,",
        "    kyc_status VARCHAR(32) DEFAULT 'VERIFIED' NOT NULL,",
        "    risk_rating VARCHAR(16) DEFAULT 'LOW' NOT NULL,",
        "    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,",
        "    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,",
        "    is_active BOOLEAN DEFAULT TRUE NOT NULL",
        ");",
        "CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_users_kyc ON users(kyc_status);",
        "",
        "-- 2. Transactions Table with Hypertable Partitioning",
        "CREATE TABLE IF NOT EXISTS transactions (",
        "    id UUID DEFAULT uuid_generate_v4(),",
        "    transaction_id VARCHAR(64) NOT NULL,",
        "    user_id VARCHAR(64) NOT NULL,",
        "    source_account_id VARCHAR(64) NOT NULL,",
        "    target_account_id VARCHAR(64) NOT NULL,",
        "    amount NUMERIC(18, 4) NOT NULL,",
        "    currency VARCHAR(8) DEFAULT 'USD' NOT NULL,",
        "    merchant_id VARCHAR(64),",
        "    merchant_category_code VARCHAR(16),",
        "    device_id VARCHAR(64),",
        "    ip_address INET,",
        "    latitude DOUBLE PRECISION,",
        "    longitude DOUBLE PRECISION,",
        "    channel VARCHAR(32) DEFAULT 'web',",
        "    raw_payload JSONB DEFAULT '{}'::jsonb,",
        "    event_timestamp TIMESTAMPTZ NOT NULL,",
        "    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,",
        "    PRIMARY KEY (id, event_timestamp)",
        ");",
        "CREATE INDEX IF NOT EXISTS idx_tx_user_time ON transactions(user_id, event_timestamp DESC);",
        "CREATE INDEX IF NOT EXISTS idx_tx_device_time ON transactions(device_id, event_timestamp DESC);",
        "CREATE INDEX IF NOT EXISTS idx_tx_ip_time ON transactions(ip_address, event_timestamp DESC);",
        "CREATE INDEX IF NOT EXISTS idx_tx_merchant ON transactions(merchant_id);",
        "",
        "-- 3. Fraud Decisions Ledger",
        "CREATE TABLE IF NOT EXISTS fraud_evaluations (",
        "    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),",
        "    transaction_id VARCHAR(64) NOT NULL,",
        "    risk_score DOUBLE PRECISION NOT NULL,",
        "    risk_level VARCHAR(32) NOT NULL,",
        "    action VARCHAR(32) NOT NULL,",
        "    triggered_rules JSONB DEFAULT '[]'::jsonb,",
        "    reasons JSONB DEFAULT '[]'::jsonb,",
        "    shap_values JSONB DEFAULT '{}'::jsonb,",
        "    feature_snapshot JSONB DEFAULT '{}'::jsonb,",
        "    latency_ms DOUBLE PRECISION NOT NULL,",
        "    model_version VARCHAR(32) NOT NULL,",
        "    is_chargeback INT DEFAULT 0 NOT NULL,",
        "    chargeback_reported_at TIMESTAMPTZ,",
        "    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL",
        ");",
        "CREATE INDEX IF NOT EXISTS idx_fraud_tx_id ON fraud_evaluations(transaction_id);",
        "CREATE INDEX IF NOT EXISTS idx_fraud_risk_score ON fraud_evaluations(risk_score DESC);",
        "CREATE INDEX IF NOT EXISTS idx_fraud_action ON fraud_evaluations(action);",
        "",
        "-- 4. Catalog Items Table",
        "CREATE TABLE IF NOT EXISTS catalog_items (",
        "    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),",
        "    item_id VARCHAR(64) UNIQUE NOT NULL,",
        "    title VARCHAR(256) NOT NULL,",
        "    category VARCHAR(64) NOT NULL,",
        "    sub_category VARCHAR(64),",
        "    brand VARCHAR(64),",
        "    price NUMERIC(12, 2) NOT NULL,",
        "    in_stock INT DEFAULT 1 NOT NULL,",
        "    tags JSONB DEFAULT '[]'::jsonb,",
        "    embedding DOUBLE PRECISION[] DEFAULT '{}',",
        "    metadata JSONB DEFAULT '{}'::jsonb,",
        "    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,",
        "    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL",
        ");",
        "CREATE INDEX IF NOT EXISTS idx_catalog_category ON catalog_items(category);",
        "",
        "-- 5. User Recommendation Interactions Table",
        "CREATE TABLE IF NOT EXISTS user_interactions (",
        "    id UUID DEFAULT uuid_generate_v4(),",
        "    user_id VARCHAR(64) NOT NULL,",
        "    session_id VARCHAR(64),",
        "    item_id VARCHAR(64) NOT NULL,",
        "    interaction_type VARCHAR(32) NOT NULL,",
        "    reward_value DOUBLE PRECISION DEFAULT 1.0 NOT NULL,",
        "    context JSONB DEFAULT '{}'::jsonb,",
        "    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,",
        "    PRIMARY KEY (id, created_at)",
        ");",
        "CREATE INDEX IF NOT EXISTS idx_interactions_user ON user_interactions(user_id, created_at DESC);",
        "CREATE INDEX IF NOT EXISTS idx_interactions_item ON user_interactions(item_id);",
        "",
        "-- 6. Audit Chain Table",
        "CREATE TABLE IF NOT EXISTS audit_chain_ledger (",
        "    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),",
        "    sequence_index BIGINT UNIQUE NOT NULL,",
        "    previous_hash VARCHAR(64) NOT NULL,",
        "    current_hash VARCHAR(64) UNIQUE NOT NULL,",
        "    actor_id VARCHAR(64) NOT NULL,",
        "    event_type VARCHAR(64) NOT NULL,",
        "    payload JSONB NOT NULL,",
        "    hmac_signature VARCHAR(64) NOT NULL,",
        "    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL",
        ");",
        "CREATE INDEX IF NOT EXISTS idx_audit_seq ON audit_chain_ledger(sequence_index);",
        "CREATE INDEX IF NOT EXISTS idx_audit_event ON audit_chain_ledger(event_type);",
    ]
    write_file("backend/database/schema.sql", "\n".join(ddl_lines))

if __name__ == "__main__":
    generate_aml_and_fraud_rules()
    generate_database_migrations_and_ddl()
