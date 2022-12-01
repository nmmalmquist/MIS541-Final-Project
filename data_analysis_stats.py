import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.formula.api import logit
from statsmodels.formula.api import mnlogit
import matplotlib.pyplot as plt
import seaborn as sn
from sklearn.cluster import KMeans


def main():

    #We make our unit at the professor level instead of the review level
    sec_data = pd.read_csv("./merged_data/SEC Schools Sentiment.csv")
    sec_data = sec_data.groupby(["prof_id","first_name","gender", "school_name","school_id"]).mean().reset_index()
    arts_data = pd.read_csv("./merged_data/Liberal Arts Schools Sentiment.csv")
    arts_data = arts_data.groupby(["prof_id","first_name","gender", "school_name","school_id"]).mean().reset_index()
    


    # #OLS Linear Regression on Sentiment Score and Rating
    sentiment_vs_quality(sec_data,arts_data)

    cluster_analysis(sec_data.append(arts_data))
    # # #doing logistical regression on gender ~ sentiment_score + difficulty + quality
    logit_plot(sec_data)
    logit_plot(arts_data)
    corr_map(sec_data)
    corr_map(arts_data)


def corr_map(df):
   
    
    # Numeric columns of the dataset
    numeric_col = ['sentiment_score','quality','difficulty']
    
    # Correlation Matrix formation
    corr_matrix = df.loc[:,numeric_col].corr()
    
    #Using heatmap to visualize the correlation matrix
    sn.heatmap(corr_matrix, annot=True)
    plt.show()

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
    # mn_logit = mnlogit("quality ~ sentiment_score", df).fit_regularized()
    # print(mn_logit.summary())

def logit_plot(df):
    df = df[(df["gender"] == "male") | (df["gender"] == "female") ]
    df["gender_binary"] = df["gender"].apply(make_gender_binary_column)
    logit_model_all = logit("gender_binary ~ quality + difficulty + sentiment_score", df).fit()
    print(logit_model_all.summary())
    logit_model = logit("gender_binary ~ quality", df).fit()
    print(logit_model.summary())
    logit_model = logit("gender_binary ~ difficulty", df).fit()
    print(logit_model.summary())
    logit_model = logit("gender_binary ~ sentiment_score", df).fit()
    print(logit_model.summary())

def make_gender_binary_column(value ):
    if (value == "male"):
        return 1
    return 0


def cluster_analysis(df):
    variable_list = ["quality", "difficulty"]
    df['quality_norm'] = (df['quality'] - df['quality'].mean())/df['quality'].std()
    df['difficulty_norm'] = (df['difficulty'] - df['difficulty'].mean())/df['difficulty'].std()

    find_cluster_count(df, variable_list)
    cluster_count = 3

    df = create_clusters(df, variable_list, cluster_count)
  
    plot_clusters(df, cluster_count)
    print(df[variable_list].describe().round(3))

def find_cluster_count(df, variable_list):
    wcss = [] # Within Cluster Sum of Squares (trying to minimize)
    
    for i in range(1, 16):
        k_means_model = KMeans(n_clusters=i)
        k_means_model.fit(df[variable_list])
        wcss.append(k_means_model.inertia_)
        
    plt.figure()
    plt.plot(range(1,16), wcss, marker='*')
    plt.title('Elbow Curve')
    plt.xlabel('Number of Clusters')
    plt.ylabel('WCSS')
    plt.show()

def create_clusters(df, variable_list, cluster_count):
    k_means_model = KMeans(n_clusters=cluster_count)
    df['cluster'] = k_means_model.fit_predict(df[variable_list])
    
    print(df['cluster'].value_counts().sort_index())
    
    return df

def plot_clusters(df, cluster_count):
    color_list = ['red', 'blue', 'green', "brown", "purple","orange","cyan", "gray"]
    
    plt.figure()
    
    for i in range(cluster_count):
        df_cluster = df[df['cluster'] == i]
        plt.scatter(df_cluster['quality'], df_cluster['difficulty'], 
                    s=20, color=color_list[i], marker="*")
        
    plt.title('Clusters')
    plt.xlabel('Difficulty')
    plt.ylabel('Quality')
    plt.show()

main()