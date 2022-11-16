from textblob import TextBlob
import pandas as pd
import re
import numpy as np

def main(): 
    arts_df = pd.read_csv('./merged_data/Liberal Arts Schools.csv', lineterminator='\n')
    sec_df = pd.read_csv('./merged_data/SEC Schools.csv', lineterminator='\n')

    sec_df = sec_df.drop(columns=['comment\r\r']) #dropping extra comment row
    arts_df = arts_df.drop(columns=['comment\r\r']) #dropping extra comment row

    #print(arts_df.columns)
    #print(sec_df.columns)


    arts_df['comment'] = arts_df.apply(lambda x: clean_comment(x.comment), axis=1  ) #regex cleaning comments
    sec_df['comment'] = sec_df.apply(lambda x: clean_comment(x.comment), axis=1  ) #regex cleaning comments

    arts_df['sentiment_score'] = arts_df.apply(lambda x: get_sentiment(x.comment), axis=1)
    sec_df['sentiment_score'] = sec_df.apply(lambda x: get_sentiment(x.comment), axis=1)

    arts_df.to_csv('./merged_data/Liberal Arts Schools Sentiment.csv')
    sec_df.to_csv('./merged_data/SEC Schools Sentiment.csv')


def get_sentiment(comment):
    return TextBlob(comment).polarity

def clean_comment(comment):
    comment = re.sub("[^A-Za-z'\s]", '', str(comment))
    comment = re.sub('\s+', ' ', str(comment))
    comment = comment.strip()
    return comment



main()