import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.formula.api import ols
import re
import gzip
import sklearn
import folium
import geopy

# How often does someone leave a rating but no comment - group by professor
# 4411 professors with reviews that have no comments for liberal arts
# 3529 professors with reviews that have no comments for SEC

# Number of professors split by gender

# Linear regression of difficulty to quality - average professor level
# 22% of the variation in quality can be explain by the variation in difficulty which is not that high however
# you can argue that the ratings are based on a 0.5 incremental category starting at 1. Because of the gaps
# in ratings that will naturally distory the R-squared value and reduce our correlation. Our attempt is to
# do a comparison to see if the qualtity, difficulty, and sentiment score has any correlation with the gender
# of the professor. Already, you can see the bias resulting from the correlation between our independent variables
# (in this case, quality and difficulty).

# Get number of professors
# 30,939 professors from Northern schools – 17 schools
# 36,023 professors from SEC schools – 14 schools
# 30 schools total

# Number of records after cleaning
# Differences b/w liberal arts and sec schools


def main():
    arts_df = pd.read_csv(
        './merged_data/Liberal Arts Schools.csv', lineterminator='\n')
    sec_df = pd.read_csv('./merged_data/SEC Schools.csv', lineterminator='\n')
    # number_reviews_per_prof(arts_df)

    # num_of_prof(sec_df)
    # Not using above methods as of now

    rating_no_comment(arts_df)
    rating_no_comment(sec_df)

    num_prof_by_gender(arts_df, sec_df)

    difficulty_to_quality()


def difficulty_to_quality():
    sec_df = pd.read_csv("./merged_data/SEC Schools Sentiment.csv")
    sec_df = sec_df.groupby(
        ["prof_id", "first_name", "gender", "school_name", "school_id"]).mean().reset_index()
    arts_df = pd.read_csv("./merged_data/Liberal Arts Schools Sentiment.csv")
    arts_df = arts_df.groupby(
        ["prof_id", "first_name", "gender", "school_name", "school_id"]).mean().reset_index()

    difficulty_vs_quality(sec_df, arts_df)


def difficulty_vs_quality(sec_data, arts_data):
    df = sec_data.append(arts_data)
    ols_model = ols("quality ~ difficulty", df).fit()
    df["predicted_quality"] = ols_model.predict(df)
    plt.figure()
    plt.title("Review Difficulty vs. Quality Rating")
    plt.xlabel("Difficulty Rating")
    plt.ylabel("Quality Rating")
    plt.scatter(df["difficulty"], df["quality"], s=2)
    plt.scatter(df["difficulty"],
                df["predicted_quality"], color="red", s=2)
    plt.show()
    print(ols_model.summary())


def num_of_prof(df):
    new_df = df.groupby('prof_id').prof_id.count()
    # new_df.to_csv('./liberal_arts_professor_count.csv')
    print(new_df)


def rating_no_comment(df):
    new_df = df.groupby('prof_id')['comment'].value_counts().to_frame()
    new_df = new_df.rename({'comment': 'comment_count'}, axis=1)
    new_df = new_df.reset_index()
    new_df = new_df[new_df.comment == 'No Comments']
    print(new_df.comment_count.count(), 'reviews with no comments')


def num_prof_by_gender(arts, sec):
    arts_gender = arts.groupby(
        'gender').value_counts()
    sec_gender = sec.groupby('gender').value_counts()

    arts_gender = arts_gender.reset_index()
    sec_gender = sec_gender.reset_index()

    arts_gender = arts_gender[arts_gender.gender != 'andy']
    arts_gender = arts_gender[arts_gender.gender != 'unknown']
    arts_gender = arts_gender[arts_gender.gender != 'mostly_male']
    arts_gender = arts_gender[arts_gender.gender != 'mostly_female']

    sec_gender = sec_gender[sec_gender.gender != 'andy']
    sec_gender = sec_gender[sec_gender.gender != 'unknown']
    sec_gender = sec_gender[sec_gender.gender != 'mostly_male']
    sec_gender = sec_gender[sec_gender.gender != 'mostly_female']

    arts_gender['gender_binary'] = arts_gender['gender'].apply(
        get_gender_binary)

    sec_gender['gender_binary'] = sec_gender['gender'].apply(
        get_gender_binary)

    arts_gender = arts_gender.groupby(
        'gender_binary')['gender'].value_counts().to_frame()

    arts_gender = arts_gender.rename({'gender': 'gender_count'}, axis=1)
    arts_gender = arts_gender.reset_index()

    sec_gender = sec_gender.groupby(
        'gender_binary')['gender'].value_counts().to_frame()

    sec_gender = sec_gender.rename({'gender': 'gender_count'}, axis=1)
    sec_gender = sec_gender.reset_index()

    print(arts_gender, end='\n')
    print(sec_gender)

    plt.figure()
    plt.pie(arts_gender['gender_count'], labels=arts_gender['gender'],
            autopct=lambda pct: func(pct, arts_gender['gender_count']))
    plt.title('Female vs Male Professors in Northern Schools')
    plt.legend(title="Gender", loc="center left",
               bbox_to_anchor=(1, 0, 0.5, 1))
    plt.show()

    plt.figure()
    plt.pie(sec_gender['gender_count'], labels=sec_gender['gender'],
            autopct=lambda pct: func(pct, sec_gender['gender_count']))
    plt.title('Female vs Male Professors in SEC Schools')
    plt.legend(title="Gender", loc="center left",
               bbox_to_anchor=(1, 0, 0.5, 1))
    plt.show()


def func(pct, allvalues):
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.1f}%\n({:d})".format(pct, absolute)


def get_gender_binary(gender):
    if gender == 'female':
        return 0
    else:
        return 1


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


main()
