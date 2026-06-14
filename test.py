import streamlit as st
import PyPDF2
# PAGE CONFIG
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)
st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and compare it with a Job Description.")
# SKILLS DATABASE
skills_db = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "excel",
    "power bi",
    "tableau",
    "machine learning",
    "deep learning",
    "nlp",
    "data analytics",
    "data science",
    "streamlit",
    "tensorflow",
    "pytorch",
    "git",
    "github",
    "html",
    "css",
    "javascript"
]
# PDF TEXT EXTRACTION
def extract_text(pdf_file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text
# SKILL DETECTION
def detect_skills(text):
    text = text.lower()
    found_skills = []
    for skill in skills_db:
        if skill in text:
            found_skills.append(skill)
    return found_skills
# UI
resume_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)
job_description = st.text_area(
    "Paste Job Description Here",
    height=200
)
# ANALYZE BUTTON
if st.button("Analyze Resume"):
    if resume_file is None:
        st.warning("Please upload a resume.")
        st.stop()
    resume_text = extract_text(resume_file)
    resume_skills = detect_skills(resume_text)
    jd_skills = detect_skills(job_description)
    matched_skills = []
    for skill in jd_skills:
        if skill in resume_skills:
            matched_skills.append(skill)
    missing_skills = []
    for skill in jd_skills:
        if skill not in resume_skills:
            missing_skills.append(skill)
    if len(jd_skills) > 0:
        score = (
            len(matched_skills)
            / len(jd_skills)
        ) * 100
    else:
        score = 0
    # RESULTS
    st.header("📊 Analysis Report")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Skills Found in Resume")
        if resume_skills:
            for skill in resume_skills:
                st.success(skill.title())
        else:
            st.warning("No skills detected.")
    with col2:
        st.subheader("🎯 Skills Required")
        if jd_skills:
            for skill in jd_skills:
                st.info(skill.title())
        else:
            st.warning("No job skills detected.")
    # MATCH SCORE
    st.subheader("📈 Match Score")
    st.progress(int(score))
    if score >= 80:
        
        st.success(f"Excellent Match: {score:.2f}%")
    elif score >= 60:
        
        st.warning(f"Good Match: {score:.2f}%")
    else:
        
        st.error(f"Low Match: {score:.2f}%")

    # MATCHED SKILLS

    st.subheader("✅ Matched Skills")

    if matched_skills:

        for skill in matched_skills:
            st.success(skill.title())

    else:
        st.warning("No matched skills found.")

    # MISSING SKILLS
    st.subheader("❌ Missing Skills")

    if missing_skills:

        for skill in missing_skills:
            st.error(skill.title())

    else:
        st.success("No missing skills.")
    # RESUME STRENGTH
    st.subheader("💪 Resume Strength")

    if len(resume_skills) >= 8:
        st.success("Strong Technical Resume")

    elif len(resume_skills) >= 5:
        st.info("Moderate Technical Resume")

    else:
        st.warning("Add more technical skills")

    # SUGGESTIONS
    st.subheader("💡 Suggestions")

    if score >= 80:

        st.success(
            "Excellent fit for this role. Your resume aligns well with the job description."
        )

    elif score >= 60:

        st.info(
            "Good match. Consider adding the missing skills to improve your chances."
        )

    else:

        st.warning(
            "Resume needs improvement. Focus on learning and adding the missing skills."
        )
    # DOWNLOAD REPORT
    report = f"""
AI RESUME ANALYZER REPORT
Match Score: {score:.2f}%
Skills Found:
{', '.join(resume_skills)}
Matched Skills:
{', '.join(matched_skills)}
Missing Skills:
{', '.join(missing_skills)}
"""
    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="resume_analysis_report.txt",
        mime="text/plain"
    )
