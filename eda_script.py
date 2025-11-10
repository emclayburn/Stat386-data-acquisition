import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

# Does scoring more points per game correlate with a higher winning percentage?
new_filename = 'nba_clean_for_eda.csv'
df_final = pd.read_csv(new_filename)

X_VAR = 'PointsPG'
Y_VAR = 'WinPCT'

correlation = df[X_VAR].corr(df[Y_VAR])

plt.figure(figsize=(10, 6))

plt.scatter(df[X_VAR], df[Y_VAR], alpha=0.6, s=50)

plt.title(f'NBA Success vs. Offensive Efficiency (2010-11 to 2023-24)\nCorrelation (r): {correlation:.4f}', fontsize=14)
plt.xlabel('Points Per Game (PointsPG)', fontsize=12)
plt.ylabel('Winning Percentage (WinPCT)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

z = np.polyfit(df[X_VAR], df[Y_VAR], 1)
p = np.poly1d(z)
plt.plot(df[X_VAR], p(df[X_VAR]), "r--", label=f'Trend Line')

plot_filename = 'eda_points_vs_winpct.png'
plt.savefig(plot_filename)
plt.close()

# Increase in pace of game/transitioning to the three point line
file_path = 'nba_clean_for_eda.csv'
df = pd.read_csv(file_path)

df_season_avg = df.groupby('SEASON_YEAR_FULL')['PointsPG'].mean().reset_index()

df_season_avg.columns = ['Season', 'Avg_PointsPG']

plt.figure(figsize=(12, 6))

plt.plot(df_season_avg['Season'], df_season_avg['Avg_PointsPG'], marker='o', linestyle='-', color='tab:blue')

plt.title('Average NBA Team Points Per Game Over Time (2010-11 to 2023-24)', fontsize=16)
plt.xlabel('NBA Season', fontsize=12)
plt.ylabel('Average Points Per Game (PointsPG)', fontsize=12)

plt.xticks(rotation=45, ha='right')

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

plot_filename = 'eda_points_pg_time_series.png'
plt.savefig(plot_filename)
plt.close()

# --- Situational Analysis: Home-Court Advantage ---
file_path = 'nba_clean_for_eda.csv'
df = pd.read_csv(file_path)

avg_home_wins = df['Home_Wins'].mean()
avg_road_wins = df['Road_Wins'].mean()

home_advantage_wins = avg_home_wins - avg_road_wins

print("--- Situational Analysis: Home-Court Advantage ---")
print(f"Average Home Wins (per season): {avg_home_wins:.2f}")
print(f"Average Road Wins (per season): {avg_road_wins:.2f}")
print(f"Average Home-Court Advantage (Difference): {home_advantage_wins:.2f} wins")

labels = ['Average Home Wins', 'Average Road Wins']
wins = [avg_home_wins, avg_road_wins]

plt.figure(figsize=(8, 6))
plt.bar(labels, wins, color=['darkblue', 'gray'])

for i, win_count in enumerate(wins):
    plt.text(i, win_count + 0.5, f'{win_count:.2f}', ha='center', fontsize=12)

plt.title('Home vs. Road Wins (NBA 2010-11 to 2023-24)', fontsize=14)
plt.ylabel('Average Wins Per Team Per Season', fontsize=12)
plt.xlabel(f'Average Home-Court Advantage: {home_advantage_wins:.2f} Wins', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.5)

plot_filename = 'eda_home_road_comparison.png'
plt.savefig(plot_filename)
plt.close()