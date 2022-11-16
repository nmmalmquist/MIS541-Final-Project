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




main()



# def sentiment_score_rating_plot(df):
#     df_group = df[["overall","sentiment_type"]].groupby(['overall','sentiment_type']).value_counts().to_frame().reset_index()
#     df_group = df_group.rename({0:'count'}, axis = 1)
#     df_pivot = df_group.pivot(index='overall', columns='sentiment_type', values='count')
#     print(df_pivot)
#     df_pivot.plot(kind="bar")
#     plt.title("Sentiment Type Distribution Across Ratings")
#     plt.xlabel("Rating")
#     plt.yticks(np.arange(0,30000,2000))
#     plt.xticks(rotation=0)
#     plt.ylabel("Number of Reviews")
#     plt.show()