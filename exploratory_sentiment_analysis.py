import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import gzip
import sklearn
import folium
import geopy


def main(): 
     #We make our unit at the professor level instead of the review level
    sec_df = pd.read_csv("./merged_data/SEC Schools Sentiment.csv")
    sec_df = sec_df.groupby(["prof_id","first_name","gender", "school_name","school_id"]).mean().reset_index()
    arts_df = pd.read_csv("./merged_data/Liberal Arts Schools Sentiment.csv")
    arts_df = arts_df.groupby(["prof_id","first_name","gender", "school_name","school_id"]).mean().reset_index()
    
    print(arts_df.columns)
    print(sec_df.columns)

    sec_df = sec_df.rename(columns={'sentiment_score\r':'sentiment_score'})
    arts_df = arts_df.rename(columns={'sentiment_score\r':'sentiment_score'})

    print(arts_df[['quality', 'difficulty', 'sentiment_score']].describe(), end='\n\n')
    print(sec_df[['quality', 'difficulty', 'sentiment_score']].describe(), end='\n\n')

    # sentiment_score_school_plot(arts_df)
    # sentiment_score_school_plot(sec_df)
    quality_gender_plot(arts_df)
    quality_gender_plot(sec_df)



def sentiment_score_school_plot(df):
    df_group = df[["quality","sentiment_score", "school_name"]].groupby(['school_name']).mean().reset_index()
    # df_group = df_group.rename({0:'average'}, axis = 1)
    # df_pivot = df_group.pivot(index='school_name', columns=['sentiment_score', 'quality'], values=['sentiment_score', 'quality'])
    #print(df_pivot)
    plt.bar(df_group["school_name"],df_group["quality"])
    plt.axhline(df_group["quality"].mean(), color="red")
    plt.text(1, df_group["quality"].mean() + .2,"Mean " + str(round(df_group["quality"].mean(),2)), color="red")
    plt.title("Sentiment & Professor Quality by School")
    plt.xlabel("School")
    plt.yticks(np.arange(0,5,.5))
    plt.xticks(rotation=80)
    plt.ylabel(" Quality (1-5)")
    plt.legend('')
    #plt.tight_layout()
    plt.show()

def quality_gender_plot(df):
    df = df[(df["gender"] == "male") | (df["gender"] == "female") ]

    df_group = df[["quality","sentiment_score","gender"]].groupby(['gender']).mean().reset_index()
    # df_group = df_group.rename({0:'average'}, axis = 1)
    # df_pivot = df_group.pivot(index='school_name', columns=['sentiment_score', 'quality'], values=['sentiment_score', 'quality'])
    #print(df_pivot)
    plt.bar(df_group["gender"],df_group["quality"])
    plt.axhline(df_group["quality"].mean(), color="red")
    plt.text(1, df_group["quality"].mean() + .2,"Mean " + str(round(df_group["quality"].mean(),2)), color="red")
    plt.title("Sentiment & Professor Quality by School")
    plt.xlabel("School")
    plt.yticks(np.arange(0,5,.5))
    plt.xticks(rotation=80)
    plt.ylabel(" Quality (1-5)")
    plt.legend('')
    #plt.tight_layout()
    plt.show()

main()



