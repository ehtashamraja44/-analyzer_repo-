import spacy
import pdfplumber

nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_txt(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_skills(text):
    skill_list = ['python', 'sql', 'pandas', 'numpy', 'excel', 'tableau', 'machine learning', 'data analyst', 'power bi', 'r', 'django', 'flask', 'statistics', 'communication']
    found_skills = [skill for skill in skill_list if skill in text.lower()]
    return list(set(found_skills))

def calculate_match(resume_skills, job_skills):
    matching = set(resume_skills) & set(job_skills)
    match_percent = (len(matching) / len(job_skills)) * 100 if job_skills else 0
    missing = set(job_skills) - set(resume_skills)
    return match_percent, list(matching), list(missing)

def generate_suggestions(missing_skills):
    suggestions = []
    for skill in missing_skills:
        if skill == 'python':
            suggestions.append("→ Add 'Python' to Skills section + mention 1 Python project with Pandas/Numpy")
        elif skill == 'sql':
            suggestions.append("→ Add 'SQL' + write 'Wrote complex queries for data analysis & reporting'")
        elif skill == 'power bi':
            suggestions.append("→ Add 'Power BI' + create 1 dashboard project and link GitHub/portfolio")
        elif skill == 'machine learning':
            suggestions.append("→ Add 'Machine Learning' + mention ML model you built: regression, classification, etc.")
        elif skill == 'statistics':
            suggestions.append("→ Add 'Statistics' + mention A/B testing, hypothesis testing, or p-values")
        elif skill == 'tableau':
            suggestions.append("→ Add 'Tableau' + create 1 visualization project on Tableau Public")
        elif skill == 'pandas':
            suggestions.append("→ Add 'Pandas' + mention data cleaning/analysis projects")
        elif skill == 'excel':
            suggestions.append("→ Add 'Excel' + mention Pivot Tables, VLOOKUP, or macros")
        elif skill == 'communication':
            suggestions.append("→ Add 'Communication' + mention presentations or team collaboration")
        else:
            suggestions.append(f"→ Add '{skill.title()}' to your Skills section")
    return suggestions

if __name__ == "__main__":
    # 1. Read resume
    resume_text = extract_text_from_pdf("data/sample_resume.pdf")
    resume_skills = extract_skills(resume_text)
    
    # 2. Read job description
    job_text = extract_text_from_txt("data/job_description.txt")
    job_skills = extract_skills(job_text)
    
    # 3. Calculate match
    match_percent, matching, missing = calculate_match(resume_skills, job_skills)
    
    # 4. Print results
    print("=== RESUME SKILLS ===")
    print(resume_skills)
    print("\n=== JOB REQUIRED SKILLS ===")
    print(job_skills)
    print(f"\n=== MATCH SCORE: {match_percent:.1f}% ===")
    print(f"✅ Matching Skills: {matching}")
    print(f"❌ Missing Skills: {missing}")
    
    # 5. AI Suggestions
    if missing:
        print("\n=== AI SUGGESTIONS TO IMPROVE ===")
        for s in generate_suggestions(missing):
            print(s)
        print(f"\n💡 Tip: Adding these {len(missing)} skills could boost your match to 90%+")
    else:
        print("\n🎯 Perfect match! Your resume is ATS-optimized for this job.")