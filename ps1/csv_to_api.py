import pandas as pd
import requests
import numpy as np
import json

# =======================
# Configuration - Change as needed
# =======================
API_URL = "http://localhost:8000/predict_batch"  # URL of your FastAPI batch predict endpoint
CSV_FILE = "HACKATHON_PREDICTION_DATA.csv"                        # Your CSV filename/path

EXPECTED_FEATURE_COLUMNS = [
    'ACCT_AGE', 'LIMIT', 'OUTS', 'ACCT_RESIDUAL_TENURE', 'LOAN_TENURE', 'INSTALAMT', 'SI_FLG',
    'AGE', 'VINTAGE', 'KYC_SCR', 'LOCKER_HLDR_IND', 'UID_FLG', 'KYC_FLG', 'INB_FLG', 'EKYC_FLG',
    'ONEMNTHCR', 'ONEMNTHSDR', 'ONEMNTHOUTSTANGBAL', 'ONEMNTHAVGMTD', 'ONEMNTHAVGQTD', 'ONEMNTHAVGYTD',
    'TWOMNTHSCR', 'TWOMNTHSDR', 'TWOMNTHOUTSTANGBAL', 'TWOMNTHAVGMTD', 'TWOMNTHAVGQTD', 'TWOMNTHAVGYTD',
    'THREEMNTHSCR', 'THREEMNTHSDR', 'THREEMNTHOUTSTANGBAL', 'THREEMNTHAVGMTD', 'THREEMNTHAVGQTD', 'THREEMNTHAVGYTD',
    'FOURMNTHSCR', 'FOURMNTHSDR', 'FOURMNTHOUTSTANGBAL', 'FOURMNTHAVGMTD', 'FOURMNTHAVGQTD', 'FOURMNTHAVGYTD',
    'FIVEMNTHSCR', 'FIVEMNTHSDR', 'FIVEMNTHOUTSTANGBAL', 'FIVEMNTHAVGMTD', 'FIVEMNTHAVGQTD', 'FIVEMNTHAVGYTD',
    'SIXMNTHSCR', 'SIXMNTHSDR', 'SIXMNTHOUTSTANGBAL', 'SIXMNTHAVGMTD', 'SIXMNTHAVGQTD', 'SIXMNTHAVGYTD',
    'SEVENMNTHSCR', 'SEVENMNTHSDR', 'SEVENMNTHOUTSTANGBAL', 'SEVENMNTHAVGMTD', 'SEVENMNTHAVGQTD', 'SEVENMNTHAVGYTD',
    'EIGHTMNTHSCR', 'EIGHTMNTHSDR', 'EIGHTMNTHOUTSTANGBAL', 'EIGHTMNTHAVGMTD', 'EIGHTMNTHAVGQTD', 'EIGHTMNTHAVGYTD',
    'NINEMNTHSCR', 'NINEMNTHSDR', 'NINEMNTHOUTSTANGBAL', 'NINEMNTHAVGMTD', 'NINEMNTHAVGQTD', 'NINEMNTHAVGYTD',
    'TENMNTHSCR', 'TENMNTHSDR', 'TENMNTHOUTSTANGBAL', 'TENMNTHAVGMTD', 'TENMNTHAVGQTD', 'TENMNTHAVGYTD',
    'ELEVENMNTHSCR', 'ELEVENMNTHSDR', 'ELEVENMNTHOUTSTANGBAL', 'ELEVENMNTHAVGMTD', 'ELEVENMNTHAVGQTD', 'ELEVENMNTHAVGYTD',
    'TWELVEMNTHSCR', 'TWELVEMNTHSDR', 'TWELVEMNTHOUTSTANGBAL', 'TWELVEMNTHAVGMTD', 'TWELVEMNTHAVGQTD', 'TWELVEMNTHAVGYTD',
    'NO_LONS', 'ALL_LON_LIMIT', 'ALL_LON_OUTS', 'ALL_LON_MAX_IRAC', 'OLDEST_LON_TAKEN', 'LATEST_LON_TAKEN',
    'LATEST_RESIDUAL_TENURE', 'OLDEST_RESIDUAL_TENURE', 'POP_CODE', 'NO_ENQ', 'FIRST_NPA_TENURE', 'CUST_NO_OF_TIMES_NPA',
    'LATEST_NPA_TENURE', 'NO_YRS_NPA', 'LATEST_RG3_TENURE', 'NO_YRS_RG3', 'TOT_IRAC_CHNG', 'TIMES_IRAC_SLIP',
    'TIMES_IRAC_UPR', 'LAST_1_YR_RG4', 'LAST_3_YR_RG4', 'LAST_1_YR_RG3', 'LAST_1_YR_RG2', 'LAST_1_YR_RG1',
    'CRIFF_11', 'CRIFF_22', 'CRIFF_33', 'CRIFF_44', 'CRIFF_55', 'CRIFF_66', 'TOTAL_CRIFF1', 'DEC_CRIFFCHNG1',
    'PRI_NO_OF_ACCTS1', 'PRI_ACTIVE_ACCTS1', 'PRI_OVERDUE_ACCTS1', 'PRI_CURRENT_BALANCE1', 'PRI_SANCTIONED_AMOUNT1',
    'PRI_DISBURSED_AMOUNT1', 'PRIMARY_INSTAL_AMT1', 'NEW_ACCTS_IN_LAST_SIX_MONTHS1', 'DELINQUENT_ACCTS_IN_LAST_SIX_MONTHS1',
    'AVERAGE_ACCT_AGE1', 'CREDIT_HISTORY_LENGTH1', 'NO_OF_INQUIRIES1', 'INCOME_BAND1', 'AGREG_GROUP', 'PRODUCT_TYPE',
    'LATEST_CR_DAYS', 'LATEST_DR_DAYS', 'TIME_PERIOD'
]
medians_df = pd.read_csv('feature_medians.csv', index_col=0)
feature_medians = medians_df.iloc[:, 0]
def load_and_prepare_data(csv_file):
    """
    Load CSV and prepare data payload for the API:
    - Filters and reorders expected features;
    - Converts each row into {"data": {...}} dictionary.
    """
    df = pd.read_csv(csv_file)

    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    for col in feature_medians.index:
        if col in df.columns:
            median_value = feature_medians.loc[col]
            df[col].fillna(median_value, inplace=True)

    missing_columns = set(EXPECTED_FEATURE_COLUMNS) - set(df.columns)
    if missing_columns:
        raise ValueError(f"CSV is missing expected columns: {missing_columns}")

    # Filter and reorder columns exactly as expected
    df = df[EXPECTED_FEATURE_COLUMNS]

    # Convert each row to dict {"data": {...}} for API input
    records = df.to_dict(orient="records")
    api_payload = [{"data": record} for record in records]

    return api_payload


def send_batch_prediction_request(payload):
    """
    Sends a POST request to the /predict_batch endpoint with given payload.
    """
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with API: {e}")
        return None


def main():
    print(f"Loading data from {CSV_FILE}...")
    try:
        batch_data = load_and_prepare_data(CSV_FILE)
        print(f"Loaded {len(batch_data)} records from CSV.")

        print(f"Sending batch prediction request to {API_URL} ...")
        results = send_batch_prediction_request(batch_data)

        if results is not None:
            # Try to extract 0/1 predictions from the API response
            # Assume response is a list of dicts with a key like 'prediction' or similar
            # Try to handle both list of dicts and list of values
            predictions = []
            if isinstance(results, list):
                for item in results:
                    if isinstance(item, dict):
                        # Try common keys
                        for key in ['prediction', 'pred', 'output', 'label', 'result']:
                            if key in item:
                                predictions.append(item[key])
                                break
                        else:
                            # If no known key, try to use the first value
                            if len(item) > 0:
                                predictions.append(list(item.values())[0])
                    else:
                        predictions.append(item)
            else:
                print("Unexpected API response format.")
                return

            # Save predictions to CSV
            output_df = pd.DataFrame({'prediction': predictions})
            output_csv = 'predictions_output.csv'
            output_df.to_csv(output_csv, index=False)
            print(f"Predictions saved to {output_csv}")
        else:
            print("Failed to get predictions from the API.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
