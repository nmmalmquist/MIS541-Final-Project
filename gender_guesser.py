#pip install gender-guesser

import gender_guesser.detector as gender
import pandas as pd

rmp_sec_school_dict = {1100: "University of Florida", 1101: "University of Georgia", 1118: "University of Kentucky",
                        1321: "University of Missouri", 1309: "University of South Carolina",
                        1385: "University of Tennessee", 4002: "Vanderbilt University", 1058: "University of Alabama",
                        1391: "University of Arkansas", 60: "Auburn University", 3071: "Louisiana State University",
                        1265: "University of Mississippi", 617: "Mississippi State University", 1003: "Texas A&M University"}

rmp_arts_school_dict = { 1320: "University of Vermont",
                        696: "Northeastern University", 709: "Northwestern University", 675: "New York University",
                        1072: "University of California Berkeley", 4086: "Mount Saint Mary's University",
                        1381: "University of Southern California", 1258: "University of Michigan",
                        124: "Boston University", 1530: "University of Washington", 1261: "University of Oregon", 457: "James Madison University",
                        1277: "University of Virginia", 3965: "Davidson College", 1139: "Washington and Lee University", 140: "Bucknell University"}



def assign_gender(name):
    d = gender.Detector()
    this_gender =  d.get_gender(str(name).capitalize())
    print(name, this_gender)
    return this_gender

for school_name in list(rmp_sec_school_dict.values()):
    df = pd.read_csv(f"/home/nmmalmquist/Source/repos/MIS541-Final-Project/SEC_DATA_PROF/{school_name}_tid.csv")
    df["gender"] = df["first_name"].apply(assign_gender)
    df.to_csv(f"/home/nmmalmquist/Source/repos/MIS541-Final-Project/SEC_DATA_PROF/{school_name}_tid.csv")

