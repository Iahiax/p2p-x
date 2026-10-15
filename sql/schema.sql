CREATE TABLE user_wallets (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(64),
  network VARCHAR(50),
  address VARCHAR(100),
  encrypted_private_key TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE fiat_wallets (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(64),
  currency VARCHAR(10),
  balance NUMERIC DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_levels (
  user_id VARCHAR(64) PRIMARY KEY,
  level INT DEFAULT 1,
  xp NUMERIC DEFAULT 0,
  multiplier NUMERIC DEFAULT 1.0
);

CREATE TABLE mining_rewards (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(64),
  amount NUMERIC,
  currency VARCHAR(10),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE aml_alerts (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(64),
  type VARCHAR(100),
  details TEXT,
  score NUMERIC,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE liquidity_pools (
  id SERIAL PRIMARY KEY,
  asset VARCHAR(20),
  balance NUMERIC,
  min_required NUMERIC
);

CREATE TABLE swap_operations (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(64),
  src_network VARCHAR(50),
  dst_network VARCHAR(50),
  src_token VARCHAR(20),
  dst_token VARCHAR(20),
  amount NUMERIC,
  chosen_protocol VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE invoices (
  id SERIAL PRIMARY KEY,
  invoice_id VARCHAR(64),
  user_id VARCHAR(64),
  amount NUMERIC,
  status VARCHAR(20),
  invoice_url TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE otc_providers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  region VARCHAR(50),
  min_amount NUMERIC,
  max_amount NUMERIC,
  reliability_score NUMERIC
);

CREATE TABLE networks (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50),
  chain_id VARCHAR(50),
  rpc_url VARCHAR(200),
  explorer_url VARCHAR(200)
);

CREATE TABLE tokens (
  id SERIAL PRIMARY KEY,
  symbol VARCHAR(20),
  name VARCHAR(50),
  network_id INT REFERENCES networks(id),
  contract_address VARCHAR(100),
  decimals INT
);
