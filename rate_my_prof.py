from ratemyprof_api.ratemyprof_api import RateMyProfApi
import re
import pandas as pd

def main():
    rmp_sec_school_dict ={ 1100: "University of Florida", 1101: "University of Georgia", 1118: "University of Kentucky",
    1321: "University of Missouri", 1309: "University of South Carolina", 
    1385: "University of Tennessee", 4002: "Vanderbilt University", 1058: "University of Alabama", 
    1391: "University of Arkansas", 60: "Auburn University", 3071: "Louisiana State University", 
    1265: "University of Mississippi", 617: "Mississippi State University", 1003: "Texas A&M University" }

    rmp_sec_school_dict ={ 1101: "University of Georgia", 1118: "University of Kentucky",
    1321: "University of Missouri", 1309: "University of South Carolina", 
    1385: "University of Tennessee", 4002: "Vanderbilt University", 1058: "University of Alabama", 
    1391: "University of Arkansas", 60: "Auburn University", 3071: "Louisiana State University", 
    1265: "University of Mississippi", 617: "Mississippi State University", 1003: "Texas A&M University" }

    rmp_arts_school_dict ={  32: "American University", 1320: "University of Vermont", 
    696: "Northeastern University", 709: "Northwestern University", 675: "New York University",
    1072: "University of California Berkeley", 4086: "Mount Saint Mary's University",
    1381: "University of Southern California",1258: "University of Michigan",
    124: "Boston University", 1530: "University of Washington", 1261: "University of Oregon", 457: "James Madison University", 
    1277: "University of Virginia", 3965: "Davidson College", 1139: "Washington and Lee University", 140: "Bucknell University" }
    
    #scrape_school_tid_for_all_prof(rmp_sec_school_dict)
    
    # scrape_school_tid_for_all_prof(rmp_arts_school_dict)
    for sec_college_name in list(rmp_sec_school_dict.values()):
        count = 0
        review_df = pd.DataFrame(columns=["prof_id","quality","difficulty","comment"])
        df_tids = pd.read_csv(f"./SEC_DATA/{sec_college_name}_tid.csv")
        for tid in list(df_tids["prof_id"]):
            review_list = RateMyProfApi().create_reviews_list(tid)
            for review in review_list:
                print(count)
                review_df.loc[len(review_df.index)] = [tid, review["rOverall"], review["rEasy"],review["rComments"]]
            count +=1
        review_df.to_csv(f"./SEC_DATA_REVIEWS/{sec_college_name}_reviews.csv")
    




def scrape_school_tid_for_all_prof(rmp_school_dict):
    def create_first_name_column(prof_id, list_of_prof):
        return list_of_prof[prof_id].first_name
    for school_id in rmp_school_dict.keys():
        univ = RateMyProfApi(school_id)
        list_of_prof = univ.scrape_professors(False)
        df = pd.DataFrame(columns=['prof_id',"first_name", "school_id", "school_name"])
        df["prof_id"] = [*set(list(list_of_prof.keys()))]
        df["first_name"] = df.apply(lambda x: create_first_name_column(x.prof_id,list_of_prof), axis=1)
        df["school_id"] = school_id
        df["school_name"] = rmp_school_dict[school_id]

        #write to csv. this will take sometime, so will store data for part 2
        df.to_csv(f"./LIBERAL_ARTS_DATA/{rmp_school_dict[school_id]}_tid.csv")






main()
