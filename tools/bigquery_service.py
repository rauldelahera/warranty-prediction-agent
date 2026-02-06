"""BigQuery Service for data access."""
from google.cloud import bigquery
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BIGQUERY, ENVIRONMENT

def query_bigquery(query: str) -> pd.DataFrame:
    """
    Execute BigQuery query and return DataFrame.
    
    Cloud (GCP): Uses service account automatically
    Local: Uses your Google credentials - you must request BigQuery access via DAP first!
           After DAP approval, run: gcloud auth application-default login
    
    Args:
        query: SQL query string
    
    Returns:
        Query results as pandas DataFrame
    """
    if ENVIRONMENT == "local":
        # Local: use your Google account credentials (requires DAP access)
        client = bigquery.Client(project=BIGQUERY['project'])
    else:
        # Cloud: use service account (automatic)
        client = bigquery.Client()
    print("Executing BigQuery query...")
    try:
        result = client.query(query).result()
        print("Query executed.")
        result_df = result.to_dataframe()
        print(f"Retrieved {len(result_df)} rows")
        return result_df
    except Exception as e:
        print(f"BigQuery error: {type(e).__name__}: {str(e)}")
        raise

def get_warranty_claims(plant: str = "COLOGNE PLANT BUILD") -> pd.DataFrame:
    """
    Get warranty claims data for a specific plant.
    
    Example query showing BigQuery data access.

    for local dev u need to change the table name to the useracccess Tables like so :
    #FROM `prj-dfad-1242-uapd-p-1242.bq_aws_fdp_dwc_vw.qai_clm_del_vw` 

    """
    query = f"""
    WITH

clm AS (
    SELECT
        2025 AS mdl_yr,
        clm_key,
        vin_cd,
        1 AS repair,
        rpr_cntry_cd,
        prt_num_causl_base_cd
    FROM `prj-dfdl-625-aws-p-625.bq_625_aws_lnd_lc_vw.clm_25_vw`
),

veh AS (
    SELECT
        2025 AS mdl_yr,
        vin_cd
    FROM `prj-dfdl-625-aws-p-625.bq_625_aws_lnd_lc_vw.veh_25_vw`
    WHERE
        veh_line_cd = "C/FU"
)

SELECT
    clm.*
FROM
    clm
INNER JOIN veh
ON clm.vin_cd=veh.vin_cd
LIMIT 1000
    """
 
    return query_bigquery(query)

