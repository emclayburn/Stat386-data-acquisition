import pandas as pd
from nba_api.stats.endpoints import LeagueDashTeamStats
import time

START_YEAR = 2010
END_YEAR = 2025
seasons = [f'{i}-{i+1-2000}' for i in range(START_YEAR, END_YEAR)]

all_3pt_df = []

print(f"Starting acquisition for 3-point stats, seasons {seasons[0]} through {seasons[-1]}...")

for season in seasons:
    try:
        team_stats = LeagueDashTeamStats(season=season)
        
        season_df = team_stats.get_data_frames()[0]
        
        df_filtered = season_df[['TEAM_ID', 'GP', 'FG3A']].copy()
        
        df_filtered['SEASON_YEAR_FULL'] = f'{season}'
        
        all_3pt_df.append(df_filtered)
        print(f"Successfully retrieved 3PT data for {season}.")
        
    except Exception as e:
        print(f"Skipping 3PT data for season {season}. Error: {e}")
        
    time.sleep(1) 
        
if not all_3pt_df:
    print("\nFATAL: No 3PT data could be retrieved.")
else:
    df_3pt_final = pd.concat(all_3pt_df, ignore_index=True)
    filename = 'nba_3pt_attempts_historical.csv'
    df_3pt_final.to_csv(filename, index=False)
    print("\n--- 3PT Acquisition Complete ---")
    print(f"Total Observations: {len(df_3pt_final)}")
    print(f"Data saved to {filename}. Ready for merging.")