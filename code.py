import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_DIR = os.path.join(BASE_DIR, '..', 'archive')
INPUT_FILES = [
    os.path.join(ARCHIVE_DIR, 'DY18.parquet'),
    os.path.join(ARCHIVE_DIR, 'DY19.parquet'),
    os.path.join(ARCHIVE_DIR, 'DY20.parquet')
]
OUTPUT_FILE = os.path.join(BASE_DIR, 'segmentation_results.csv')

METRICS = {
    'Tot_Clms': 'sum',
    'Tot_Drug_Cst': 'sum',
    'Tot_Day_Suply': 'sum',
    'Tot_Benes': 'sum',
    'GE65_Tot_Clms': 'sum',
    'GE65_Tot_Drug_Cst': 'sum'
}

def load_and_aggregate():
    cols = ['Prscrbr_NPI'] + list(METRICS.keys())
    
    dfs = []
    for file_path in INPUT_FILES:
        try:
            df = pd.read_parquet(file_path, columns=cols)
            dfs.append(df)
        except FileNotFoundError:
            print(f"  Warning: Could not find {file_path}")
    
    if not dfs:
        print("Error: No data files found!")
        return None
    
    df_all = pd.concat(dfs, ignore_index=True)
    
    df_grouped = df_all.groupby('Prscrbr_NPI').agg(METRICS).reset_index()
    return df_grouped

def calculate_features(df):
    df = df[df['Tot_Clms'] > 10].copy()
    # 1. Cost Efficiency (Cost per Claim)
    df['Avg_Cost_Per_Claim'] = df['Tot_Drug_Cst'] / df['Tot_Clms']
    # 2. Elderly Reliance (GE65 Claims / Total Claims)
    df['Elderly_Claim_Rate'] = df['GE65_Tot_Clms'] / df['Tot_Clms']
    # 3. Patient Intensity (Claims per Beneficiary)
    df['Claims_Per_Patient'] = df['Tot_Clms'] / df['Tot_Benes']
    # 4. Cost Intensity (Cost per Patient)
    df['Cost_Per_Patient'] = df['Tot_Drug_Cst'] / df['Tot_Benes']
    # 5. Day Supply Avg
    df['Avg_Day_Supply'] = df['Tot_Day_Suply'] / df['Tot_Clms']
    features = ['Avg_Cost_Per_Claim', 'Elderly_Claim_Rate', 'Claims_Per_Patient', 'Cost_Per_Patient', 'Avg_Day_Supply']
    df[features] = df[features].replace([np.inf, -np.inf], np.nan).fillna(0)
    return df, features

def apply_ai_models(df, features):
    X = df[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # SEGMENTATION (K-MEANS)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['Cluster_ID'] = kmeans.fit_predict(X_scaled)
    
    # ANOMALY DETECTION (ISOLATION FOREST)
    iso_forest = IsolationForest(contamination=0.01, random_state=42)
    df['Anomaly_Flag_Raw'] = iso_forest.fit_predict(X_scaled)
    raw_scores = iso_forest.decision_function(X_scaled)
    df['AI_Anomaly_Score'] = ((raw_scores.max() - raw_scores) / (raw_scores.max() - raw_scores.min())) * 100
    return df

def calculate_risk_score(df):
    df['Norm_Cost'] = df['Avg_Cost_Per_Claim'].rank(pct=True) * 100
    df['Norm_Elderly'] = df['Elderly_Claim_Rate'].rank(pct=True) * 100
    df['Norm_Claims_Per_Patient'] = df['Claims_Per_Patient'].rank(pct=True) * 100
    
    df['Final_Risk_Score'] = (
        (0.5 * df['AI_Anomaly_Score']) + 
        (0.25 * df['Norm_Cost']) + 
        (0.25 * df['Norm_Elderly'])
    )
    
    conditions = [
        (df['Final_Risk_Score'] >= 80),
        (df['Final_Risk_Score'] >= 50),
        (df['Final_Risk_Score'] < 50)
    ]
    choices = ['High Risk', 'Medium Risk', 'Low Risk']
    df['Risk_Category'] = np.select(conditions, choices, default='Low Risk')
    
    return df

def main():
    df_grouped = load_and_aggregate()
    if df_grouped is None: return

    df_features, feature_names = calculate_features(df_grouped)
    df_ai = apply_ai_models(df_features, feature_names)
    df_final = calculate_risk_score(df_ai)
    
    export_cols = [
        'Prscrbr_NPI', 'Tot_Clms', 'Tot_Drug_Cst', 
        'Avg_Cost_Per_Claim', 'Claims_Per_Patient', 'Elderly_Claim_Rate',
        'Cluster_ID', 'AI_Anomaly_Score', 'Final_Risk_Score', 'Risk_Category',
        'Norm_Cost', 'Norm_Elderly', 'Norm_Claims_Per_Patient'
    ]
    
    print(f"Exporting {len(df_final)} prescribers to {OUTPUT_FILE}...")
    df_final[export_cols].to_csv(OUTPUT_FILE, index=False)

if __name__ == "__main__":
    main()
