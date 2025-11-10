import pandas as pd

file_path = 'nba_team_standings_historical.csv'
df = pd.read_csv(file_path)

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

home_split = df_filtered['HOME'].str.split('-', expand=True)
df_filtered['Home_Wins'] = pd.to_numeric(home_split[0], errors='coerce')
df_filtered['Home_Losses'] = pd.to_numeric(home_split[1], errors='coerce')

road_split = df_filtered['ROAD'].str.split('-', expand=True)
df_filtered['Road_Wins'] = pd.to_numeric(road_split[0], errors='coerce')
df_filtered['Road_Losses'] = pd.to_numeric(road_split[1], errors='coerce')

df_filtered = df_filtered.drop(columns=['HOME', 'ROAD'])

df_filtered.to_csv('nba_clean_for_eda.csv', index=False)