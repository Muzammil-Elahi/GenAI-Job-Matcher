from .utils import clean_text, date_calculator
from .es_query import query_es

def retrieve_jd(resume_summary):
    response = query_es_resume(resume_summary)
    
    jd_list = extract_es_response(response)
    return jd_list

def extract_es_response(es_jd_list):
    summarized_jd_list = {}

    for hit in es_jd_list:
        id = hit['_id']
        job_data = hit['_source']

        extracted = {
            "title": job_data.get("title"),
            "location": job_data.get("location"),
            "schedule type": job_data.get("metadata", {}).get("scheduleType"),
            "company name": job_data.get("companyName"),
        }

        if work_from_home := job_data.get("metadata", {}).get("workFromHome"):
            extracted["work from home"] = work_from_home 

        run_time = job_data.get("run_time")
        posted_at = job_data.get("metadata", {}).get("postedAt")

        if run_time and posted_at:
            calculated_date = date_calculator(run_time, posted_at)
            extracted["posted date"] = calculated_date

        if job_data.get("ai_summary"):
            extracted["description"] = clean_text(job_data.get("ai_summary"))
        else:
            extracted["description"] = clean_text(job_data.get("description"))

        jd_text = " ".join(key + ':' + str(value) for key, value in extracted.items())
        summarized_jd_list[id] = jd_text
    return summarized_jd_list

def query_es_resume(resume_summary):    
    query=build_query(resume_summary)
    add_location_filter(query, resume_summary)
    
    es_jd_list = query_es(query)
    return es_jd_list
    
def filter_locations(resume_locations):
    available_locations = ['Toronto', 'Vancouver', 'Montreal', 'Calgary']
    return ",".join(loc for loc in resume_locations.split(',') if loc.strip() in available_locations)

def add_location_filter(query, resume_summary):
    if city_locations := resume_summary.get('location'):
        valid_locations = filter_locations(city_locations)
        print("valid location in ES:",valid_locations)
        if valid_locations:
            query["query"]["bool"]["filter"].append({
                "match": {"location": valid_locations}
            })

def build_query(resume_summary, return_size=100, days_ago=7):
    job_titles = resume_summary["target job titles"]
    if type(job_titles) == str:
        job_titles = job_titles.split(',')

    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "bool": {
                            "should": [
                                {
                                    "multi_match": {
                                        "query": title.strip(),
                                        "fields": ["title^2", "searched_job_title"],
                                        "type": "phrase_prefix"
                                    }
                                } for title in job_titles
                            ],
                            "minimum_should_match": 1
                        }
                    }
                ],
                "should": [
                    {"match_phrase": {"description": skill.strip()}} for skill in resume_summary["skills"].split(',')[:6]
                ],
                "filter": [
                    {"range": {"run_time": {"gte": f"now-{days_ago}d/d"}}},
                ]
            }
        },
        "sort": [{"run_time": "desc"}],
        "size": return_size
    }

    return query
