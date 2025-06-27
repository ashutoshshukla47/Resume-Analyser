import pandas as pd
import os
from resume_parser import skills_list, extract_skills_from_resume

DATA_FILE = "./sample data/Job_description.csv"

# 1. Load data (or create empty DataFrame)
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return


# 2. Save data
def save_data(df):
    df.to_csv(DATA_FILE, index=False)


# 3. Add entry
def add_job_entry(job_title, job_description):
    df = load_data()
    required_skill=extract_skills_from_resume(job_description,skills_list)
    new_row = {"Category": job_title, "Resume":job_description, "Required Skills": required_skill}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df)
    return 1


