import google.generativeai as genai
import os
from .utils import clean_text, extract_json_from_response
from dotenv import load_dotenv

load_dotenv() 
GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def rank_result(resume_summary, jd_list):
    rank_result_llm = match_and_rank(resume_summary, jd_list, top_n=5)
    rank_result = extract_json_from_response(rank_result_llm)
    return rank_result

def match_and_rank(resume_summary, job_summaries, top_n=5):
    prompt = f"""
    Given a resume summary and {len(job_summaries)} job summaries (where keys are unique job IDs and values are summaries).
    Rank the top {top_n} matches of job summaries based on qualification and suitability to the resume.
    Output an array ONLY of job IDs (as provided in the input) in descending order of the qualitative match, in the following format: [job_id_1, job_id_2, job_id_3, ...]
    Output example: [List of job IDs (as provided in the input) in a JSON array format]
    Prioritize matching accuracy, context awareness, preference handling.
    resume summary:{resume_summary}
    job summaries:{job_summaries}
    """

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text