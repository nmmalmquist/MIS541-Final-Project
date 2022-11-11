import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import gzip
import sklearn
import folium
import geopy

# How often does someone leave a rating but no comment - group by school (value counts)
# If it seems standard we will remove them from the data


def main():
    arts_df = pd.read_csv(
        './MERGED_DATA/Liberal Arts Schools.csv', lineterminator='\n')
    sec_df = pd.read_csv('./MERGED_DATA/SEC Schools.csv', lineterminator='\n')
    # number_reviews_per_prof(arts_df)
    num_reviews_no_comment(arts_df)


def number_reviews_per_prof(df):
    num_reviews = {}

    curr_id = df.iloc[0]['prof_id']
    x = 0
    for i, row in df.iterrows():
        if row.prof_id == curr_id:
            x += 1
            curr_id = row.prof_id
        else:
            num_reviews.update({curr_id: x})
            x = 0
            curr_id = row.prof_id

    num_reviews = num_reviews.drop()

    # print(num_reviews)


def num_reviews_no_comment(arts_df):
    pass


main()
