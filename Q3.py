#Nicks File 
#           -histogram of free throws per game
#           -pie chart of points divided between 1,2,3
#question: relationship between freethrows and penaltys
#           -linear regression freethrows ~ penaltys
#question: how important are free throws in winning games
#           -logistical regression isWinner ~ freethrows made
#           -logistical regression isWinner ~ freethrows made + penalties recieved

import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import math
import numpy as np

def main():
    df = get_data()
    df = organize_data(df)
    print(df.columns)
    df["isWinner"] = df.apply(lambda x: add_is_winner_column(x.TEAM_ID,x.HOME_TEAM_ID,x.HOME_TEAM_WINS), axis=1)
    df = df.drop(["HOME_TEAM_ID", "VISITOR_TEAM_ID", "HOME_TEAM_WINS"], axis=1)

    #df is cleaned and ready to go right here
    exploratory_analysis(df)




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


def exploratory_analysis(df):
    # ftm_hist_plt(df)
    the_pie_plt(df)

    




def the_pie_plt(df):
    ftm = sum(df["FTM"])
    fgm = sum(df["FGM"])
    fg3m = sum(df["FG3M"])
    total_made = ftm + fgm + fg3m   

    labels = 'Free Throws', '2-Pointers', '3-Pointers'
    sizes = [ftm/total_made, fgm/total_made,fg3m/total_made ]
    explode = [.1,0,0]


    plt.pie(sizes,explode,labels=labels,autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title("Distribution of Shots across all NBA games 2010-2020", color="black")
    plt.show()  

    ftm_point = ftm*1   
    fgm_point = fgm*2
    fg3m_point = fg3m*3
    total_made = ftm_point + fgm_point + fg3m_point 
    sizes = [ftm_point/total_made, fgm_point/total_made,fg3m_point/total_made ]
    plt.pie(sizes,explode,labels=labels,autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title("Distribution of Point per shot type across all NBA games 2010-2020", color="black")
    plt.show()  

def ftm_hist_plt(df):
    plt.hist(df["FTM"], bins=30, edgecolor="gray", color="navy")
    plt.title("Free Throws Made Per Game", color="black")
    plt.xlabel("Free Throws Made")
    plt.ylabel("Count")
    plt.xticks(np.arange(0,50,5), rotation=50)
    plt.yticks(np.arange(0,7500, 500), fontsize=12, rotation=0)
    #adding verticle lines in plot
    plt.axvline(df.FTM.median(), color="red",linestyle="dashed")
    plt.text(df["FTM"].median() - 12, 6500, "Median", color="red")
    plt.axvline(df.FTM.mean(), color="orange", linestyle="dotted" )
    plt.text(df["FTM"].mean() + 3, 6500, "Mean", color="orange")
    plt.show()








main()
