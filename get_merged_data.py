import pandas as pd


def main():
    rmp_sec_school_dict = {1100: "University of Florida", 1101: "University of Georgia", 1118: "University of Kentucky",
                           1321: "University of Missouri", 1309: "University of South Carolina",
                           1385: "University of Tennessee", 4002: "Vanderbilt University", 1058: "University of Alabama",
                           1391: "University of Arkansas", 60: "Auburn University", 3071: "Louisiana State University",
                           1265: "University of Mississippi", 617: "Mississippi State University", 1003: "Texas A&M University"}

    rmp_arts_school_dict = {32: "American University", 1320: "University of Vermont",
                            696: "Northeastern University", 709: "Northwestern University", 675: "New York University",
                            1072: "University of California Berkeley", 4086: "Mount Saint Mary's University",
                            1381: "University of Southern California", 1258: "University of Michigan",
                            124: "Boston University", 1530: "University of Washington", 1261: "University of Oregon", 457: "James Madison University",
                            1277: "University of Virginia", 3965: "Davidson College", 1139: "Washington and Lee University", 140: "Bucknell University"}

    sec_schools = []
    arts_schools = []

    for value in rmp_sec_school_dict.values():
        sec_schools.append(value)

    for value in rmp_arts_school_dict.values():
        arts_schools.append(value)
    # Set the values in a list

    sec_prof_df = pd.DataFrame()
    sec_reviews_df = pd.DataFrame()

    for school in sec_schools:
        school = pd.read_csv(
            f'./SEC_DATA_PROF/{school}_tid.csv')
        sec_prof_df = sec_prof_df.append(school)

    for school in sec_schools:
        school = pd.read_csv(
            f'./SEC_DATA_REVIEWS/{school}_reviews.csv', lineterminator='\n')
        sec_reviews_df = sec_reviews_df.append(school)

    arts_prof_df = pd.DataFrame()
    arts_reviews_df = pd.DataFrame()

    for school in arts_schools:
        school = pd.read_csv(
            f'./LIBERAL_ARTS_DATA_PROF/{school}_tid.csv')
        arts_prof_df = arts_prof_df.append(school)

    for school in arts_schools:
        school = pd.read_csv(
            f'./LIBERAL_ARTS_DATA_REVIEWS/{school}_reviews.csv', lineterminator='\n')
        arts_reviews_df = arts_reviews_df.append(school)

    sec_df = join_schools(sec_prof_df, sec_reviews_df)
    sec_df.to_csv('./merged_data/SEC Schools.csv')

    arts_df = join_schools(arts_prof_df, arts_reviews_df)
    arts_df.to_csv('./merged_data/Liberal Arts Schools.csv')


def join_schools(df1, df2):
    df_combined = pd.merge(df1, df2, on='prof_id', how='outer')
    df_combined = df_combined.set_index('prof_id')
    df_combined = df_combined.sort_index()
    df_combined = df_combined.drop(columns='Unnamed: 0_x', axis=1)
    df_combined = df_combined.drop(columns='Unnamed: 0_y', axis=1)
    return df_combined


main()
