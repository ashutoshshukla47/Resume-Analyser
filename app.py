import streamlit as st
from analyser import anaylse
from resume_parser import skills_list,extract_text_from_file,user_skill
from add_to_df import add_job_entry
import pandas as pd
import tempfile,os
from pyresparser import ResumeParser
import time

st.title('Resume Job Matcher')

# Initialize session state if not set
if "resume_uploaded" not in st.session_state:
    st.session_state.resume_uploaded = False
if "uploaded_resume" not in st.session_state:
    st.session_state.uploaded_resume = None
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0  # Used to force reset uploader

add_skill=st.empty()
uploader=st.empty()

# Only show uploader if resume has not been uploaded
if not st.session_state.resume_uploaded:
    uploaded_resume = uploader.file_uploader("please upload your resume here",type=["pdf", "docx"],
    help="Accepted formats: PDF, DOCX. Max size: 20MB",key=st.session_state.uploader_key)
else:
    uploaded_resume = st.session_state.uploaded_resume  # Restore from session


if "show_form" not in st.session_state:
    st.session_state.show_form = False


submit_placeholder=st.empty()
submit=submit_placeholder.button('Search Job')    

col1, col2 = st.columns(2)

with col1:
    if st.button("Refresh"):
        st.session_state.show_form = False
        st.session_state.resume_uploaded = False
        st.session_state.uploaded_resume = None
        st.session_state.processing_done = False
        st.session_state.uploader_key = 1  # 🔁 Changes uploader's key to clear it
        st.rerun()  # 🔁 Optional: instantly clears UI

with col2:
    if st.button("Add Opportunity"):
        submit_placeholder.empty()
        uploader.empty()
        st.session_state.show_form = True
        st.session_state.uploaded_resume = None
        st.session_state.resume_uploaded = True
        st.session_state.processing_done = True  

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
                st.session_state.show_form = False  # 👈 hide form after submit
                st.session_state.show_form = False
                st.session_state.resume_uploaded = False
                st.session_state.uploaded_resume = None
                st.session_state.processing_done = False
                st.session_state.uploader_key = 0  # 🔁 Changes uploader's key to clear it
                st.rerun()  # 🔁 Optional: instantly clears UI
        else:
            st.error("❌ Please fill in both fields.")
            time.sleep(2)

        st.session_state.show_form = False  # 👈 hide form after submit
        st.session_state.show_form = False
        st.session_state.resume_uploaded = False
        st.session_state.uploaded_resume = None
        st.session_state.processing_done = False
        st.session_state.uploader_key = 0  # 🔁 Changes uploader's key to clear it
        st.rerun()  # 🔁 Optional: instantly clears UI    
        


msg=st.empty()

if submit:
    if uploaded_resume:  # Safe check
        msg.success('Processing your Resume')
        # Create a temporary file with the same extension as uploaded file
        file_extension = uploaded_resume.name.split('.')[-1].lower()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as tmp_file:
            # Write the uploaded file content to temporary file
            tmp_file.write(uploaded_resume.getbuffer())
            tmp_file_path = tmp_file.name
        
        # Use pyresparser to extract data
        user_data = ResumeParser(tmp_file_path).get_extracted_data()
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        text=extract_text_from_file(uploaded_resume)
        if text:
            submit_placeholder.empty()
            uploader.empty()
            st.session_state.uploaded_resume = uploaded_resume
            st.session_state.resume_uploaded = True
            st.session_state.processing_done = True
            user_skills=set(user_skill(text))
            st.write(f"Your Skills:- {user_skills}")

            # skill=add_skill.text_input("Can't see Your Skill", placeholder="e.g., Data Analytics(one at a time)")
            # if skill not in skills_list:
            #     skills_list.append(skill)
                
            # else:
            #     st.error("Skill Exist") 

            st.write(f'Details:- {user_data["name"]}, {user_data["email"]}, {user_data["mobile_number"]}')   

            df=pd.read_csv('./sample data/Job_description.csv')
            matches=anaylse(df,user_skills)
            msg.success("✅ Resume processed successfully!")
            st.text("Matches Found")
            for match in matches:
                st.write(f'Your Match:- {match[0]}, Title:- {match[2]}, Missing Skill:- {match[3]}')

        else:
            msg.error('Unsupported Resume File')   

    else:
        msg.error('please Upload Your Resume First')    



