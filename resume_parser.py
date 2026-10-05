import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher
from pdfminer.high_level import extract_text
from io import StringIO
import docx2txt
import json
# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def load_skills():
    with open("./sample data/skills_list.json", "r") as f:
        return json.load(f)["skills"]

def save_skills(skill_list):
    with open("./sample data/skills_list.json", "w") as f:
        json.dump({"skills": skill_list}, f)

def add_skill(new_skill):
    skills = load_skills()
    skill = new_skill.strip().lower()
    if skill and skill not in skills_list:
        skills_list.append(skill)
        save_skills(skills_list)

skills_list=load_skills()

patterns = [nlp.make_doc(skill.lower()) for skill in skills_list]

# Setup matcher
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
matcher.add("SKILL", patterns)


def extract_skills_from_resume(text, skills_list):
    # Apply matcher
    doc = nlp(text.lower())
    matches = matcher(doc)

    # Extract matched skills
    found_skills = set([doc[start:end].text.lower() for _, start, end in matches])

    return sorted(set(found_skills))



# Example usage
df=pd.read_csv('./sample data/UpdatedResumeDataSet.csv')


def extract_text_from_file(uploaded_file):
    if uploaded_file is None:
        return ""

    file_type = uploaded_file.name.split('.')[-1].lower()

    # Handle text file
    if file_type == 'txt':
        stringio = StringIO(uploaded_file.read().decode("utf-8"))
        return stringio.read()

    # Handle docx file
    elif file_type == 'docx':
        return docx2txt.process(uploaded_file)

    # Handle PDF file
    elif file_type == 'pdf':
        text = extract_text(uploaded_file)
        return text

    else:
        return ""

def user_skill(text):
    user_skills=extract_skills_from_resume(text,skills_list)
    return user_skills

def job_description_skill(skills_list):
    df=pd.read_csv('./sample data/UpdatedResumeDataSet.csv')
    df['Required Skills']=df['Resume'].apply(lambda x:extract_skills_from_resume(str(x), skills_list))
    return df