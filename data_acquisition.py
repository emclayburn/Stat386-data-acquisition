import pandas as pd
from nba_api.stats.endpoints import LeagueStandings
import time

START_YEAR = 2010
END_YEAR = 2025

seasons = [f'{i}-{i+1-2000}' for i in range(START_YEAR, END_YEAR)]

all_seasons_df = []

for season in seasons:
    standings = LeagueStandings(season=season, season_type='Regular Season')
    season_df = standings.get_data_frames()[0]
    season_df['SEASON_YEAR_FULL'] = season
    all_seasons_df.append(season_df)
    time.sleep(1) 
        
df_final = pd.concat(all_seasons_df, ignore_index=True)

filename = 'nba_team_standings_historical.csv'
df_final.to_csv(filename, index=False)