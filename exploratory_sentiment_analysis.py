import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import gzip
import sklearn
import folium
import geopy


def main(): 
    arts_df = pd.read_csv('./merged_data/Liberal Arts Schools Sentiment.csv', lineterminator='\n')
    sec_df = pd.read_csv('./merged_data/SEC Schools Sentiment.csv', lineterminator='\n')

    print(arts_df.columns)
    print(sec_df.columns)

    sec_df = sec_df.rename(columns={'sentiment_score\r':'sentiment_score'})
    arts_df = arts_df.rename(columns={'sentiment_score\r':'sentiment_score'})

    print(arts_df[['quality', 'difficulty', 'sentiment_score']].describe(), end='\n\n')
    print(sec_df[['quality', 'difficulty', 'sentiment_score']].describe(), end='\n\n')

    sentiment_score_school_plot(arts_df)
    sentiment_score_school_plot(sec_df)




def sentiment_score_school_plot(df):
    df_group = df[["quality","sentiment_score", "school_name"]].groupby(['school_name']).mean().reset_index()
    df_group = df_group.rename({0:'average'}, axis = 1)
    df_pivot = df_group.pivot(index='school_name', columns=['sentiment_score', 'quality'], values=['sentiment_score', 'quality'])
    #print(df_pivot)
    df_pivot.plot(kind="bar")
    plt.title("Sentiment & Professor Quality by School")
    plt.xlabel("School")
    plt.yticks(np.arange(0,5,.5))
    plt.xticks(rotation=90)
    plt.ylabel("Sentiment Score (-1 - 1 ) & Quality (1-5)")
    plt.legend('')
    #plt.tight_layout()
    plt.show()


main()



