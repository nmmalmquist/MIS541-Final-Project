import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import math
import numpy as np

#3FGA from 2010 to 2021 line chart -> show the change in avg 3pt attemps over last 10 years per game

#group by team and see which teams has more success vs a higher % of 3s?

#relationship btwn points scored in a game and 3 point FG % in that game
    #linear regression: points ~ FG3PCNT

#group 3pt % into two categories 0 for less than 50% and 1 greater, find out where we want to set this
    #

#does making more 3pt FGs win more games?
    #logistical regression:  isWinner ~ 3FGM per game

#does a higher 3pt FG % win more games?
    #logistical regression: isWinner ~ 3FG%

def main():
    df = get_data()
    df = organize_data(df)
    print(df.columns)
    df["isWinner"] = df.apply(lambda x: add_is_winner_column(x.TEAM_ID,x.HOME_TEAM_ID,x.HOME_TEAM_WINS), axis=1)
    df = df.drop(["HOME_TEAM_ID", "VISITOR_TEAM_ID", "HOME_TEAM_WINS"], axis=1)
    
    #adding new column for 3pt% over course of the game 
    df['FG%_3PT'] = (df['FG3M']/df['FG3A'])
    plot_attempt_line_by_year(df)
    #df.to_excel('outputnewdf.xlsx', index=False)
     



def get_data():
    game_details_df = pd.read_csv('games_details.csv', sep=',')
    game_details_df = game_details_df[["GAME_ID", "TEAM_ID", "FGM", "FGA","FG3M","FG3A","FTM","FTA"]]
    games_df = pd.read_csv('games.csv', sep=',')[["GAME_ID","SEASON","HOME_TEAM_ID","VISITOR_TEAM_ID", "HOME_TEAM_WINS"]]
    teams_df = pd.read_csv('teams.csv', sep=',')[["TEAM_ID","NICKNAME","CITY"]]
    df_combined = pd.merge(game_details_df, games_df, on='GAME_ID', how='outer')
    df_combined = pd.merge(df_combined, teams_df, on='TEAM_ID', how='outer')
    return df_combined

def organize_data(df):
    df_game_consolidated = df.groupby(["GAME_ID", "TEAM_ID","SEASON","HOME_TEAM_ID","VISITOR_TEAM_ID", "HOME_TEAM_WINS", "NICKNAME", "CITY"]).sum()
    df_game_consolidated = df_game_consolidated.reset_index()
    df_game_consolidated = df_game_consolidated.dropna(subset=["GAME_ID", "TEAM_ID","SEASON","HOME_TEAM_ID","VISITOR_TEAM_ID", "HOME_TEAM_WINS", "NICKNAME", "CITY"])
    df_game_consolidated = df_game_consolidated[df_game_consolidated["SEASON"] >= 2010]
    # mydf = df_game_consolidated[[not elem for elem in pd.isnull(df_game_consolidated["FGA"])]]
    convert_dict = {'GAME_ID': str, 
                    'TEAM_ID': str,
                    'HOME_TEAM_ID': str,
                    'VISITOR_TEAM_ID': str
                    }
    df_game_consolidated = df_game_consolidated.astype(convert_dict)
    # using dictionary to convert specific columns
    return df_game_consolidated

def add_is_winner_column(team_id, home_team_id,home_team_wins):
    if team_id == home_team_id:
        if home_team_wins == 1:
            return 1
        else:
            return 0
    if home_team_wins == 1:
        return 0
    else:
        return 1


def plot_attempt_line_by_year(df):
    attempts_year_df = df.drop(['GAME_ID', 'TEAM_ID', 'NICKNAME', 'FGM', 'FGA', 'FG3M', 'FTM', 'FTA', 'isWinner', 'FG%_3PT', 'CITY'], axis=1)
    attempts_year_df = attempts_year_df.groupby(['SEASON'])['FG3A'].mean().to_frame()
    print(attempts_year_df)
    plt.figure()
    attempts_year_df.plot(kind='line', color='dodgerblue', linestyle='dotted')
    plt.title('Number of 3 Point shots attempted by year', color='red', fontsize=15)
    plt.xlabel('Year', color='darkblue', size=12)
    plt.ylabel('3 Point Field Goals attempted per game', color='darkblue', size=12)
    plt.yticks(np.arange(15,40,2))
    plt.xticks(np.arange(2010,2022,1))
    plt.xticks(rotation=30)
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()

main()
