import pandas as pd

file_path = 'nba_team_standings_historical.csv'
df = pd.read_csv(file_path)

# --- 1. Define Your Motivating Question ---
# Example Question: "Is offensive efficiency (PointsPG) a better predictor of success (WinPCT) in the modern NBA than defensive efficiency?"

# --- 2. Select Your 5+ Core Features for Analysis ---
# Based on the column list you provided, these are great candidates for EDA:

CORE_FEATURES = [
    'SEASON_YEAR_FULL',
    'TeamName',        
    'WINS',          
    'WinPCT',          
    'PointsPG',     
    'DiffPointsPG',    
    'AheadAtHalf',     
    'HOME',
    'ROAD'
]

df_filtered = df[CORE_FEATURES].copy()

df_filtered['WinPCT'] = pd.to_numeric(df_filtered['WinPCT'], errors='coerce')

print("--- Filtered Data Head ---")
print(df_filtered.head())
print(f"\nTotal rows for analysis: {len(df_filtered)}")
print(f"Columns for analysis: {df_filtered.columns.tolist()}")

df_filtered.to_csv('nba_clean_for_eda.csv', index=False)