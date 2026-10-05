import re
import time

import pandas as pd
import streamlit as st

from add_to_df import add_job_entry
from analyser import anaylse
from resume_parser import add_skill, extract_text_from_file, user_skill


def extract_basic_contact_info(text):
    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    phone_match = re.search(r"(?:\+?\d[\d\s\-()]{7,}\d)", text)

    name = ""
    name_match = re.search(r"(?im)^\s*(?:Mr\.?|Ms\.?|Mrs\.?|Dr\.?|Prof\.?\s+)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}\s*$", text)
    if name_match:
        name = name_match.group(0).strip()

    return {
        "name": name,
        "email": email_match.group(0) if email_match else "",
        "mobile_number": re.sub(r"\D", "", phone_match.group(0)) if phone_match else ""
    }

st.title('Resume Job Matcher')

# Home
if "resume_uploaded" not in st.session_state:
    st.session_state.resume_uploaded = False
if "uploaded_resume" not in st.session_state:
    st.session_state.uploaded_resume = None
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0  # Used to force reset uploader
   
if "show_skill_form" not in st.session_state:
    st.session_state.show_skill_form = False 
if "job_search" not in st.session_state:
    st.session_state.job_search=False

uploader = st.empty()

#Only show uploader if resume has not uploaded
if not st.session_state.resume_uploaded:
    uploaded_resume = uploader.file_uploader("please upload your resume here", type=["pdf", "docx"],
    help="Accepted formats: PDF, DOCX. Max size: 20MB", key=st.session_state.uploader_key)
else:
    uploaded_resume = st.session_state.uploaded_resume  # Restore from session

if "show_form" not in st.session_state:
    st.session_state.show_form = False

submit_placeholder = st.empty()
submit = submit_placeholder.button('Search Job')

col1, col2 = st.columns(2)

with col1:
    if st.button("Refresh"):
        st.session_state.show_form = False
        st.session_state.resume_uploaded = False
        st.session_state.uploaded_resume = None
        st.session_state.processing_done = False
        st.session_state.show_skill_form = False  # Reset skill form too
        st.session_state.uploader_key = 1
        st.rerun()

with col2:
    if st.button("Add Opportunity"):
        submit_placeholder.empty()
        uploader.empty()
        st.session_state.show_form = True
        st.session_state.uploaded_resume = None
        st.session_state.resume_uploaded = True
        st.session_state.processing_done = True  


#for Add new Opportunity
if st.session_state.show_form:
    submit_placeholder.empty()
    with st.form("job_form"):
        job_title = st.text_area("Write Job Title Here")
        job_description = st.text_area("Write The Job Description")
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        if job_title and job_description:
            result = add_job_entry(job_title, job_description)
            if result:
                st.success("✅ Job added successfully!")
                time.sleep(2)
                st.session_state.show_form = False
                st.session_state.resume_uploaded = False
                st.session_state.uploaded_resume = None
                st.session_state.processing_done = False
                st.session_state.uploader_key = 0
                st.rerun()
        else:
            st.error("❌ Please fill in both fields.")
            time.sleep(2)

        st.session_state.show_form = False
        st.session_state.resume_uploaded = False
        st.session_state.uploaded_resume = None
        st.session_state.processing_done = False
        st.session_state.uploader_key = 0
        st.rerun()

msg = st.empty()
if submit:
    st.session_state.job_search=True

# Show the skill form right after the button
#to Add a Skill to Skills List
if st.session_state.show_skill_form:
    with st.form("Add_Skill"):
        new_skill = st.text_area("Write The Skill")
        col1, col2 = st.columns(2)
                    
        with col1:
            submit_skill = st.form_submit_button("Submit")
        with col2:
            cancel_skill = st.form_submit_button("Cancel")

        if submit_skill:
            if new_skill.strip():
                add_skill(new_skill)
                st.success(f"Skill '{new_skill.strip()}' added!")
                st.session_state.show_skill_form = False
                st.rerun()
            else:
                st.warning("Please enter a valid skill.")
                    
            if cancel_skill:
                st.session_state.show_skill_form = False
                st.rerun()

temp=1


#Processing the resume here!
if st.session_state.job_search and temp:
    if uploaded_resume:
        msg.success('Processing your Resume')
        text = extract_text_from_file(uploaded_resume)

        if text:
            user_data = extract_basic_contact_info(text)
            submit_placeholder.empty()
            uploader.empty()
            st.session_state.uploaded_resume = uploaded_resume
            st.session_state.resume_uploaded = True
            st.session_state.processing_done = True
            user_skills = set(user_skill(text))

            st.write(f"Your Skills:- {user_skills}")

            if st.button('A Skill not Mentioned?'):
                st.session_state.show_skill_form = True
                temp = 0

            st.write(f'Details:- {user_data["name"]}, {user_data["email"]}, {user_data["mobile_number"]}')

            df = pd.read_csv('./sample data/Job_description.csv')
            matches = anaylse(df, user_skills)
            msg.success("✅ Resume processed successfully!")
            if temp:
                st.text("Matches Found")
                for match in matches:
                    st.write(f'Your Match:- {match[0]}, Title:- {match[2]}, Missing Skill:- {match[3]}')
        else:
            msg.error('Unsupported Resume File')
    else:
        msg.error('please Upload Your Resume First')    



