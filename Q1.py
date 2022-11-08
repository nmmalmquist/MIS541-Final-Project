import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import math
import numpy as np
# tim
# logistical regression with y (win true or false) being dependent variable and x being
# the ratio of two to three point shots

# isWinner ~ ratio
# isWinner ~ ratio + year

# for every single game


def main():
    df = get_data()
    fgm_df = two_pointers_made_by_game(df)
    fga_df = two_pointers_attempted(df)
    print(fgm_df)
    plot_fgm(fgm_df)


def get_data():
    df = pd.read_csv('games_details.csv', sep=',')
    return df


def two_pointers_made_by_game(df):
    df = df.groupby(['GAME_ID', 'TEAM_ID'])['FGM'].mean().to_frame()
    df = df.dropna()
    return df


def two_pointers_attempted(df):
    df.set_index('ID', inplace=True)
    df = df.dropna()
    df = df.reset_index()
    return df


def plot_fgm(fgm_df):
    plt.figure()
    fgm_df.plot(kind='bar')
    plt.title('Average Field Goals Made by Game')
    plt.xlabel('Game')
    plt.ylabel('Average Made')
    plt.yticks(np.arange(0, 15, 1))
    plt.xticks(np.arange(0, len(fgm_df.index)), labels=fgm_df.index)
    plt.xticks(rotation=0)
    plt.legend(loc='upper left')
    plt.show()


main()
