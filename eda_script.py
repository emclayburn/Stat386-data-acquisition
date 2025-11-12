import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_clean_data():
    df_main = pd.read_csv("nba_team_standings_historical.csv")

    df_3pt = pd.read_csv("nba_3pt_attempts_historical.csv")
    df_3pt["FG3A_PG"] = df_3pt["FG3A"] / df_3pt["GP"]

    CORE_FEATURES = [
        'SEASON_YEAR_FULL','TeamID','TeamName','WINS','WinPCT',
        'PointsPG','DiffPointsPG','AheadAtHalf','HOME','ROAD'
    ]

    df = df_main[CORE_FEATURES].copy()
    df["WinPCT"] = pd.to_numeric(df["WinPCT"], errors="coerce")

    home = df["HOME"].str.split("-", expand=True)
    df["Home_Wins"] = pd.to_numeric(home[0], errors="coerce")
    df["Home_Losses"] = pd.to_numeric(home[1], errors="coerce")

    road = df["ROAD"].str.split("-", expand=True)
    df["Road_Wins"] = pd.to_numeric(road[0], errors="coerce")
    df["Road_Losses"] = pd.to_numeric(road[1], errors="coerce")

    df = df.drop(columns=["HOME", "ROAD"])

    df_final = pd.merge(
        df,
        df_3pt[["TEAM_ID","SEASON_YEAR_FULL","FG3A_PG"]],
        left_on=["TeamID","SEASON_YEAR_FULL"],
        right_on=["TEAM_ID","SEASON_YEAR_FULL"],
        how="left"
    )

    df_final = df_final.drop(columns=["TEAM_ID"])

    return df_final



def plot_points_vs_winpct(df):
    X_VAR = "PointsPG"
    Y_VAR = "WinPCT"

    correlation = df[X_VAR].corr(df[Y_VAR])

    plt.figure(figsize=(10,6))
    plt.scatter(df[X_VAR], df[Y_VAR], alpha=0.6)
    z = np.polyfit(df[X_VAR], df[Y_VAR], 1)
    plt.plot(df[X_VAR], np.poly1d(z)(df[X_VAR]), "r--")

    plt.title(f"Points Per Game vs Win % (r = {correlation:.3f})")
    plt.xlabel("Points Per Game")
    plt.ylabel("Win %")
    plt.grid(True)
    plt.show()


def plot_diff_vs_winpct(df):
    X = "DiffPointsPG"
    Y = "WinPCT"

    correlation = df[X].corr(df[Y])

    plt.figure(figsize=(10,6))
    plt.scatter(df[X], df[Y], alpha=0.6)
    z = np.polyfit(df[X], df[Y], 1)
    plt.plot(df[X], np.poly1d(z)(df[X]), "r--")

    plt.title(f"Point Differential vs Win % (r = {correlation:.3f})")
    plt.xlabel("Point Differential")
    plt.ylabel("Win %")
    plt.grid(True)
    plt.show()


def plot_home_vs_road(df):
    avg_home = df["Home_Wins"].mean()
    avg_road = df["Road_Wins"].mean()

    plt.bar(["Home Wins","Road Wins"], [avg_home, avg_road], color=["blue","gray"])
    plt.title(f"Home vs Road Performance (Avg Home Advantage = {avg_home - avg_road:.2f} wins)")
    plt.ylabel("Average Wins")
    plt.show()


def plot_points_and_3pa_over_time():
    df = pd.read_csv("nba_clean_for_eda.csv")

    df2 = df.groupby("SEASON_YEAR_FULL").agg(
        Avg_PointsPG=("PointsPG","mean"),
        Avg_FG3A_PG=("FG3A_PG","mean")
    ).reset_index()

    seasons = df2["SEASON_YEAR_FULL"]

    fig, ax1 = plt.subplots(figsize=(12,6))

    ax1.plot(seasons, df2["Avg_PointsPG"], marker="o", label="Points per Game", color="blue")
    ax1.set_ylabel("Points Per Game", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")
    ax1.tick_params(axis="x", rotation=45)

    ax2 = ax1.twinx()
    ax2.plot(seasons, df2["Avg_FG3A_PG"], linestyle="--", marker="s", color="red", label="3PA per Game")
    ax2.set_ylabel("3PA Per Game", color="red")
    ax2.tick_params(axis="y", labelcolor="red")

    plt.title("Points vs 3-Point Attempts Over Time")
    fig.tight_layout()
    plt.show()
