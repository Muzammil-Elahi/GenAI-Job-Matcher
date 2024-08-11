from .utils import clean_text, extract_json_from_response
import google.generativeai as genai
import os
from langchain_community.document_loaders import PyMuPDFLoader
from dotenv import load_dotenv

load_dotenv() 
GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def extract_resume(resume_url):
    cleaned_text = load_pdf(resume_url)
    response = summarize_and_infer(cleaned_text)
    resume_summary = extract_json_from_response(response)
    return resume_summary

def summarize_and_infer(cleaned_text, is_resume=True, output_format="json", model='gemini-1.5-pro'):
    prompt_text_output = "Format the output as a concise, text-only paragraph without any formatting (e.g., bold text) or new lines."
    prompt_json_output = "Return a JSON object ONLY with the following fields. Provide concise, relevant information for each field in plain text PARAGRAPH format."
    target_job_titles="- target job titles: list of DISTINCT target roles that align with the candidate's skills and experience. Do not include job title prefix e.g. senior."
    company_culture = "- company culture: company's values, mission, industry fit, growth potential, role alignment. Junior: Look for collaborative environments, clear career paths, and roles with varied tasks for skill development. Mid-Level: Seek opportunities for increased responsibility, specialized skill development, and high-impact projects with recognition. Senior: Focus on leadership roles, strategic impact on business goals, and autonomy to drive innovation within the organization."
    career_goal = "- career goal: Based on job progression, skills & experience, projects & accomplishments, education & certifications"
    qualification_responsibility="Identify core responsibilities and duties of the role. Identify minimum educational requirements and preferred experience and level."
    qualification_experience="Include education, experience, and other relevant qualifications, highlighting achievements and quantifiable results."
    prompt = f"""
    Analyze this {'resume' if is_resume else 'job description'}. Extract and infer the following information
    Prioritize speed. {prompt_json_output if output_format=="json" else prompt_text_output} If information for a field is not available or cannot be reasonably inferred, do not return the field.
    Fields to extract/infer:
    { target_job_titles if is_resume else "- job title:" }
    - skills: {"include all relevant hard and soft skills." if is_resume else "Identify the required and preferred skills listed"}
    - qualifications: { qualification_experience if is_resume else qualification_responsibility}
    {"- city: Include city name ONLY" if is_resume else "- location: "}
    - salary range:
    { career_goal if is_resume else company_culture}
    {'resume' if is_resume else 'job description'} text:
    """

    print(prompt + cleaned_text)

    model = genai.GenerativeModel(model)
    response = model.generate_content(prompt + cleaned_text)
    return response.text

def load_pdf(url):
    loader = PyMuPDFLoader(url)
    docs = loader.load()
    full_text = " ".join(doc.page_content for doc in docs)
    return clean_text(full_text)