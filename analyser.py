import ast


def anaylse(df, user_skills):
    whole_list = []
    df["Required Skills"] = df["Required Skills"].apply(ast.literal_eval)

    for index, row in df.iterrows():
        skills = list(row["Required Skills"])
        jd_skills = set(skills)

        if not jd_skills:
            continue

        matches = user_skills & jd_skills
        missing_skills = jd_skills - user_skills
        extra_skill = user_skills - jd_skills

        # score based on required skill overlap only
        score = (len(matches) / len(jd_skills)) * 100

        # slight penalty for missing skills, but do not reward unrelated extra skills
        if missing_skills:
            score -= min(len(missing_skills) * 5, 35)
        if extra_skill:
            score -= min(len(extra_skill), 10)

        score = max(0, min(100, round(score, 2)))

        result = [score, index, row["Category"], missing_skills]
        whole_list.append(result)

    whole_list.sort(key=lambda x: x[0], reverse=True)
    return whole_list[0:50]