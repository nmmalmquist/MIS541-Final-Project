import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.formula.api import logit
from statsmodels.formula.api import mnlogit
import matplotlib.pyplot as plt
import seaborn as sn
from sklearn.cluster import KMeans
  #We make our unit at the professor level instead of the review level
sec_data = pd.read_csv("./merged_data/SEC Schools Sentiment.csv")
sec_data = sec_data.groupby(["prof_id","first_name","gender", "school_name","school_id"]).mean().reset_index()
arts_data = pd.read_csv("./merged_data/Liberal Arts Schools Sentiment.csv")
arts_data = arts_data.groupby(["prof_id","first_name","gender", "school_name","school_id"]).mean().reset_index()

arts_data_gender = arts_data.groupby("gender")["gender"].value_counts()
print(arts_data_gender)
    

sec_data_gender = sec_data.groupby("gender")["gender"].value_counts()
print(sec_data_gender)
    
