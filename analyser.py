from resume_parser import job_description_skill
import ast

whole_list=[]

def anaylse(df,user_skills):
    df["Required Skills"] = df["Required Skills"].apply(ast.literal_eval)
    for index, row in df.iterrows():
        Skills= list(row['Required Skills'])
        l1=[]
        jd_skills=set(Skills)
        score=0
        matches=user_skills & jd_skills
        extra_skill=user_skills - jd_skills
        if not len(jd_skills) == 0:
            score=len(matches)/len(jd_skills)
            score=score*100
            score+=(len(extra_skill)*2)
            if score > 100:
                score=100
        l1.append(score)
        l1.append(index)
        l1.append(row['Category'])
        missing_skills=jd_skills - user_skills
        l1.append(missing_skills)
        whole_list.append(l1)

        whole_list.sort(key=lambda x: x[0], reverse=True)
        
    return whole_list[0:50]