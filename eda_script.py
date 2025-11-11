import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = 'nba_team_standings_historical.csv'
df = pd.read_csv(file_path)

CORE_FEATURES = [
    'SEASON_YEAR_FULL',
    'TeamID',
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

# Point differential and its impact on winning percentage
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the cleaned data (if not already loaded)
file_path = 'nba_clean_for_eda.csv'
df = pd.read_csv(file_path)

# --- 1. Define Variables for Analysis (Point Differential) ---
X_VAR_DIFF = 'DiffPointsPG'
Y_VAR = 'WinPCT'

# --- 2. Calculate the Correlation Coefficient ($r$) ---
# This measures how closely WinPCT relates to the margin of victory/loss
correlation_diff = df[X_VAR_DIFF].corr(df[Y_VAR])

print(f"--- Correlation Analysis for {X_VAR_DIFF} vs. {Y_VAR} ---")
print(f"The Pearson correlation coefficient (r) is: {correlation_diff:.4f}")

# --- 3. Generate the Scatter Plot ---
plt.figure(figsize=(10, 6))

# Create the scatter plot
plt.scatter(df[X_VAR_DIFF], df[Y_VAR], alpha=0.6, s=50)

# Add title and labels (The correlation value will be extremely high)
plt.title(f'NBA Success vs. Scoring Margin (2010-11 to 2023-24)\nCorrelation (r): {correlation_diff:.4f}', fontsize=14)
plt.xlabel('Point Differential Per Game (DiffPointsPG)', fontsize=12)
plt.ylabel('Winning Percentage (WinPCT)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add a simple linear trend line
z = np.polyfit(df[X_VAR_DIFF], df[Y_VAR], 1)
p = np.poly1d(z)
plt.plot(df[X_VAR_DIFF], p(df[X_VAR_DIFF]), "r--", label=f'Trend Line')

# --- 4. Save the Plot ---
plot_filename = 'eda_diffpoints_vs_winpct.png'
plt.savefig(plot_filename)
plt.close()

print(f"\nScatter plot saved as: {plot_filename}")

# 3 Point data
import pandas as pd
import numpy as np

main_file_path = 'nba_team_standings_historical.csv'
df_main = pd.read_csv(main_file_path)

three_pt_file_path = 'nba_3pt_attempts_historical.csv'
df_3pt = pd.read_csv(three_pt_file_path)

df_3pt['FG3A_PG'] = df_3pt['FG3A'] / df_3pt['GP']

CORE_FEATURES = [
    'SEASON_YEAR_FULL',
    'TeamID',
    'TeamName',
    'WINS', 
    'WinPCT',
    'PointsPG',
    'DiffPointsPG',
    'AheadAtHalf',
    'HOME',
    'ROAD'
]

df_filtered = df_main[CORE_FEATURES].copy()

df_filtered['WinPCT'] = pd.to_numeric(df_filtered['WinPCT'], errors='coerce')

home_split = df_filtered['HOME'].str.split('-', expand=True)
df_filtered['Home_Wins'] = pd.to_numeric(home_split[0], errors='coerce')
df_filtered['Home_Losses'] = pd.to_numeric(home_split[1], errors='coerce')

road_split = df_filtered['ROAD'].str.split('-', expand=True)
df_filtered['Road_Wins'] = pd.to_numeric(road_split[0], errors='coerce')
df_filtered['Road_Losses'] = pd.to_numeric(road_split[1], errors='coerce')

df_filtered = df_filtered.drop(columns=['HOME', 'ROAD'])

df_final = pd.merge(
    df_filtered, 
    df_3pt[['TEAM_ID', 'SEASON_YEAR_FULL', 'FG3A_PG']],
    left_on=['TeamID', 'SEASON_YEAR_FULL'], 
    right_on=['TEAM_ID', 'SEASON_YEAR_FULL'], 
    how='left'
)

df_final = df_final.drop(columns=['TEAM_ID'])

final_filename = 'nba_clean_for_eda.csv'
df_final.to_csv(final_filename, index=False)

print("\n--- Final Data Preparation Complete ---")
print(f"Cleaned dataset saved to {final_filename}")
print(f"New column 'FG3A_PG' added successfully.")
print("Sample of final features:")
print(df_final[['SEASON_YEAR_FULL', 'TeamName', 'WinPCT', 'PointsPG', 'FG3A_PG']].head())

# modeling the relationship between PointsPG and FG3A_PG over time

import pandas as pd
import matplotlib.pyplot as plt

# Load the FINAL clean data (it now contains the merged FG3A_PG column)
df_final = pd.read_csv('nba_clean_for_eda.csv')

# Aggregation (Group by Season for Averaging)
df_combined_avg = df_final.groupby('SEASON_YEAR_FULL').agg(
    Avg_PointsPG=('PointsPG', 'mean'),
    Avg_FG3A_PG=('FG3A_PG', 'mean')
).reset_index()

# Extract the season year for cleaner plotting labels
df_combined_avg['Season_End_Year'] = df_combined_avg['SEASON_YEAR_FULL'].str.split('-').str[1]
x_labels = df_combined_avg['Season_End_Year'].tolist()

# Create the Dual-Axis Plot
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot 1 (Primary Y-Axis: Points Per Game)
color1 = 'tab:blue'
ax1.set_xlabel('NBA Season End Year', fontsize=12)
ax1.set_ylabel('Avg. Points Per Game (PointsPG)', color=color1, fontsize=12)
ax1.plot(x_labels, df_combined_avg['Avg_PointsPG'], marker='o', linestyle='-', color=color1, label='Avg. PointsPG')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.tick_params(axis='x', rotation=45)

# Plot 2 (Secondary Y-Axis: 3-Point Attempts)
ax2 = ax1.twinx()
color2 = 'tab:red'
ax2.set_ylabel('Avg. 3-Point Attempts Per Game (FG3A_PG)', color=color2, fontsize=12)
ax2.plot(x_labels, df_combined_avg['Avg_FG3A_PG'], marker='s', linestyle='--', color=color2, label='Avg. FG3A_PG')
ax2.tick_params(axis='y', labelcolor=color2)
ax2.grid(axis='y', linestyle=':', alpha=0.5, color=color2)

# Title and Legend
plt.title('The Evolving NBA: Points Per Game vs. 3-Point Attempts Over Time', fontsize=16)
fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.95))

plt.tight_layout()
plot_filename = 'eda_points_vs_3pt_time_series_combined.png'
plt.savefig(plot_filename)
plt.close()