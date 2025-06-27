import pandas as pd
import os
from resume_parser import job_description_skill, skills_list

df=job_description_skill(skills_list)

df.to_csv('./sample data/Job_description.csv',index=False)