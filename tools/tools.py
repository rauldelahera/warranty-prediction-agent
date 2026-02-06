import traceback
import sys
from tools.bigquery_service import query_bigquery
from google.cloud import bigquery
from config import BIGQUERY
import re

# Cache for prediction results to prevent duplicate BigQuery calls
_prediction_cache = {}

# ============================================
# WARRANTY PREDICTION TOOL (ML Model)
# ============================================

def predict_warranty_cost(vin: str) -> str:
    """Predict warranty claim probability for a specific vehicle VIN using ML model.
    The response has this format
Prediction: prediction
Probability: d.d% chance of warranty claim
Risk Level: level-of RISK

Recommendation: recomendation text."""
    
    print("predict_warranty_cost called with VIN:", vin)

    # Validate VIN format (17 alphanumeric characters)
    vin = vin.strip().upper()
    if not re.match(r'^[A-HJ-NPR-Z0-9]{17}$', vin):
        return f"Invalid VIN format. VINs must be exactly 17 alphanumeric characters. You provided: {vin}"
    
    # Check cache first
    if vin in _prediction_cache:
        print(f"Returning cached prediction for VIN {vin}")
        return _prediction_cache[vin]
    
    # Build the ML prediction query
    query = f"""
    SELECT
      vin,
      predicted_has_warranty_claim,
      predicted_has_warranty_claim_probs
    FROM
        ML.PREDICT(MODEL `{BIGQUERY['project']}.warranty_models.claim_occurrence_model`,
        (
        SELECT
          *
        FROM
          `{BIGQUERY['project']}.warranty_data.training_data`
        WHERE
          vin = '{vin}'
        )
      )
    """
    
    try:
        df = query_bigquery(query)
        print("predict_warranty_cost executed query")
        print(df)
        if df.empty:
            print("predict_warranty_cost query returned no data")
            return f"No data found for VIN: {vin}. Please verify the VIN is correct and exists in our quality data system."
        
        print(f"predict_warranty_cost Query executed. Rows returned: {len(df)}")

        # Extract prediction results
        row = df.iloc[0]
        print("predict_warranty_cost Retrieved row:", row.to_dict())

        predicted_claim = row['predicted_has_warranty_claim']
        probs = row['predicted_has_warranty_claim_probs']
        
        # Parse probability (it's typically a struct/list with [prob_no_claim, prob_claim])
        # Assuming the second value is probability of having a claim
        # if isinstance(probs, (list, tuple)) and len(probs) >= 2:
        #     prob_claim = float(probs[1]['prob']) if isinstance(probs[1], dict) else float(probs[1])
        # else:
        #     prob_claim = 0.5  # Fallback
        probs = row['predicted_has_warranty_claim_probs']

        # Extract probabilities
        prob_claim = None
        prob_false = None

        for prob_entry in probs:
            if prob_entry['label'] == True:
                prob_claim = prob_entry['prob']
            elif prob_entry['label'] == False:
                prob_false = prob_entry['prob']
        
        print(f"Prediction for VIN {vin}: {predicted_claim} with probability {prob_claim}")
        # Determine risk level
        if prob_claim >= 0.7:
            risk_level = "HIGH RISK"
            recommendation = "This vehicle has a high likelihood of warranty claims. Recommend thorough quality inspection and proactive maintenance planning."
        elif prob_claim >= 0.4:
            risk_level = "MEDIUM RISK"
            recommendation = "This vehicle shows moderate warranty risk. Standard quality checks recommended."
        else:
            risk_level = "LOW RISK"
            recommendation = "This vehicle has a low probability of warranty claims. Routine quality process should be sufficient."
        
        # Format response
        response = f"""
Warranty Prediction for VIN: {vin}

Prediction: {"Will likely have warranty claim" if predicted_claim == 1 else "Unlikely to have warranty claim"}
Probability: {prob_claim*100:.1f}% chance of warranty claim
Risk Level: {risk_level}

Recommendation: {recommendation}
"""
        print(f"Generated prediction response for VIN {vin}")
        print (response)
        
        # Cache the result
        _prediction_cache[vin] = response.strip()
        
        return response.strip()
    
    except Exception as e:
        # Print comprehensive error information
        print("=" * 80)
        print("EXCEPTION CAUGHT IN predict_warranty_cost")
        print("=" * 80)
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception Message: {str(e)}")
        print(f"Exception Args: {e.args}")
        print("\nFull Traceback:")
        print("-" * 80)
        traceback.print_exc(file=sys.stdout)
        print("-" * 80)
        print(f"VIN that caused error: {vin}")
        print("=" * 80)
        error_msg = str(e)
        if "403" in error_msg or "permission" in error_msg.lower():
            return "ERROR: Cannot access ML model. Check your BigQuery permissions and verify the model exists."
        elif "404" in error_msg or "not found" in error_msg.lower():
            return f"ERROR: ML model or training data table not found. Please verify the model exists. Error: {error_msg}"
        else:
            return f"Prediction failed: {error_msg}"


def predict_warranty_total_cost(vin: str) -> str:
    """Predict warranty claim total cost for a specific vehicle VIN using ML model.
    The response has this format
    Total cost: AMOUNT USD
    """
    
    print("predict_warranty_total_cost called with VIN:", vin)

    # Validate VIN format (17 alphanumeric characters)
    vin = vin.strip().upper()
    if not re.match(r'^[A-HJ-NPR-Z0-9]{17}$', vin):
        print("Invalid VIN format detected")
        return f"Invalid VIN format. VINs must be exactly 17 alphanumeric characters. You provided: {vin}"

    query = f"""
        SELECT
        vin,
        -- The raw predicted log value
        predicted_log_total_cost,
        -- The predicted value converted back to dollars
        ROUND(EXP(predicted_log_total_cost) - 1, 2) AS predicted_cost_usd,
        -- The actual value converted back to dollars (if comparing)
        ROUND(EXP(log_total_cost) - 1, 2) AS actual_cost_usd
        FROM
        ML.PREDICT(MODEL `{BIGQUERY['project']}.warranty_models.total_cost_model`, (
            -- This subquery provides the features for prediction
            -- It must have the same column names/types as the training data
            SELECT * FROM `{BIGQUERY['project']}.warranty_data.cost_training_data` WHERE vin = '{vin}'
        ))
    """
    
    try:
        df = query_bigquery(query)
        print("predict_warranty_total_cost executed query")
        print(df)
        if df.empty:
            print("predict_warranty_total_cost query returned no data")
            return f"No data found for VIN: {vin}. Please verify the VIN is correct and exists in our quality data system."
        
        print(f"predict_warranty_total_cost Query executed. Rows returned: {len(df)}")

        # Extract prediction results
        row = df.iloc[0]
        print("predict_warranty_total_cost Retrieved row:", row.to_dict())

        predicted_cost = row['predicted_cost_usd']
        
        print(f"Total Cost Prediction for VIN {vin}: ${predicted_cost:.2f} USD")
        
        # Format response
        response = f"""
        Total cost: ${predicted_cost:.2f} USD
        """
        print (response)
        return response.strip()

    except Exception as e:
        # Print comprehensive error information
        print("=" * 80)
        print("EXCEPTION CAUGHT IN predict_warranty_total_cost")
        print("=" * 80)
        print(f"Exception Type: {type(e).__name__}")
        print(f"Exception Message: {str(e)}")
        print(f"Exception Args: {e.args}")
        print("\nFull Traceback:")
        print("-" * 80)
        traceback.print_exc(file=sys.stdout)
        print("-" * 80)
        print(f"VIN that caused error: {vin}")
        print("=" * 80)
        error_msg = str(e)
        if "403" in error_msg or "permission" in error_msg.lower():
            return "ERROR: Cannot access ML model. Check your BigQuery permissions and verify the model exists."
        elif "404" in error_msg or "not found" in error_msg.lower():
            return f"ERROR: ML model or training data table not found. Please verify the model exists. Error: {error_msg}"
        else:
            return f"Prediction failed: {error_msg}"