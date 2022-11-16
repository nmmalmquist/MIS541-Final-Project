import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.formula.api import logit
from statsmodels.formula.api import mnlogit
import matplotlib.pyplot as plt


def main():

    sec_data = pd.read_csv("./merged_data/SEC Schools Sentiment.csv")
    arts_data = pd.read_csv("./merged_data/Liberal Arts Schools Sentiment.csv")

    #OLS Linear Regression on Sentiment Score and Rating
    sentiment_vs_quality(sec_data,arts_data)




def sentiment_vs_quality(sec_data,arts_data):
    df = sec_data.append(arts_data)
    ols_model = ols("quality ~ sentiment_score", df).fit()
    df["predicted_quality"] = ols_model.predict(df)
    plt.figure()
    plt.title("Review Sentiment Score vs. Quality Rating")
    plt.xlabel("Sentiment Score")
    plt.ylabel("Quality Rating")
    plt.scatter(df["sentiment_score"], df["quality"], s=2)
    plt.scatter(df["sentiment_score"], df["predicted_quality"], color="red", s=2)
    plt.show()
    print(ols_model.summary())
    #Since the quality is not a continuous various var, we should do a multinomial logit
    mn_logit = mnlogit("quality ~ sentiment_score", df).fit()
    print(mn_logit.summary())










main()