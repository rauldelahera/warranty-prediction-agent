-- BigQuery Setup for Warranty Prediction Agent
-- This script creates datasets, sample training data, and ML models

-- Create datasets
CREATE SCHEMA IF NOT EXISTS `warranty-prediction-demo.warranty_data`
OPTIONS(
  description="Training data for warranty prediction models",
  location="US"
);

CREATE SCHEMA IF NOT EXISTS `warranty-prediction-demo.warranty_models`
OPTIONS(
  description="ML models for warranty predictions",
  location="US"
);

-- Create sample training data table
CREATE OR REPLACE TABLE `warranty-prediction-demo.warranty_data.training_data` AS
SELECT
  CONCAT('1HGBH41JXMN10', LPAD(CAST(n AS STRING), 4, '0')) AS vin,
  CASE WHEN MOD(n, 3) = 0 THEN TRUE ELSE FALSE END AS has_warranty_claim,
  CAST(2020 + MOD(n, 5) AS INT64) AS model_year,
  ['Honda', 'Toyota', 'Ford', 'Chevrolet', 'BMW'][MOD(n, 5)] AS make,
  ['Sedan', 'SUV', 'Truck', 'Coupe'][MOD(n, 4)] AS vehicle_type,
  CAST(15000 + (n * 123) AS INT64) AS mileage,
  ['CA', 'TX', 'NY', 'FL', 'IL'][MOD(n, 5)] AS state,
  CASE WHEN MOD(n, 3) = 0 THEN CAST((n * 47) AS FLOAT64) ELSE 0.0 END AS total_claim_cost
FROM UNNEST(GENERATE_ARRAY(1, 1000)) AS n;

-- Create cost training data (for vehicles with claims)
CREATE OR REPLACE TABLE `warranty-prediction-demo.warranty_data.cost_training_data` AS
SELECT
  vin,
  model_year,
  make,
  vehicle_type,
  mileage,
  state,
  total_claim_cost
FROM `warranty-prediction-demo.warranty_data.training_data`
WHERE has_warranty_claim = TRUE;

-- Create warranty claim occurrence model (Classification)
CREATE OR REPLACE MODEL `warranty-prediction-demo.warranty_models.claim_occurrence_model`
OPTIONS(
  model_type='LOGISTIC_REG',
  input_label_cols=['has_warranty_claim']
) AS
SELECT
  model_year,
  make,
  vehicle_type,
  mileage,
  state,
  has_warranty_claim
FROM `warranty-prediction-demo.warranty_data.training_data`;

-- Create total cost prediction model (Regression)
CREATE OR REPLACE MODEL `warranty-prediction-demo.warranty_models.total_cost_model`
OPTIONS(
  model_type='LINEAR_REG',
  input_label_cols=['total_claim_cost']
) AS
SELECT
  model_year,
  make,
  vehicle_type,
  mileage,
  state,
  total_claim_cost
FROM `warranty-prediction-demo.warranty_data.cost_training_data`;
