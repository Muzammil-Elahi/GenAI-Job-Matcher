from .process_resume import extract_resume
from .es_query_resume import retrieve_jd
from .match_and_rank import rank_result
from .es_query_jd_id import retrieve_jds
import requests
import logging
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import os
import tempfile

USE_API = True
logger = logging.getLogger(__name__)

@csrf_exempt
def upload_resume(request):
    if request.method == 'POST' and 'resume' in request.FILES:
        resume_file = request.FILES['resume']
        
        # Prepare the file for upload
        files = {'file': (resume_file.name, resume_file, resume_file.content_type)}
        
        try:
            # Upload to tmpfiles.org
            response = requests.post('https://tmpfiles.org/api/v1/upload', files=files)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'url' in data['data']:
                    tmp_link = data['data']['url']
                    
                    # Replace 'tmpfiles.org' with 'tmpfiles.org/dl' to get direct download link
                    download_link = tmp_link.replace('tmpfiles.org', 'tmpfiles.org/dl')
                    
                    # Process the resume
                    resume_summary = extract_resume(download_link)
                    
                    es_query_data = {
                        "target job titles": resume_summary.get('target job titles', []),
                        "skills": resume_summary.get('skills', []),
                        "location": resume_summary.get('city', '')
                    }
                    
                    jd_list = retrieve_jd(es_query_data)
                    print("reaches after retrive jobs")
                    rank_id_list = rank_result(resume_summary, jd_list)
                    print("reaches after rank result")
                    ranked_jds = retrieve_jds(rank_id_list)
                    print("reaches after ranked jobs")
                    return JsonResponse(ranked_jds, safe=False)
                else:
                    return JsonResponse({'error': 'Failed to get URL from tmpfiles.org response'}, status=500)
            else:
                return JsonResponse({'error': f'Failed to upload to tmpfiles.org. Status code: {response.status_code}'}, status=500)
        
        except requests.RequestException as e:
            return JsonResponse({'error': f'Error uploading file: {str(e)}'}, status=500)
        except Exception as e:
            return JsonResponse({'error': f'Error processing resume: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def resume_service(resume_url):
    if USE_API:
        resume_summary = extract_resume(resume_url)

        es_query_data = {
            "target job titles": resume_summary.get('target job titles'),
            "skills": resume_summary.get('skills'),
            "location": resume_summary.get('city'),
        }

        jd_list = retrieve_jd(es_query_data)
        rank_id_list=rank_result(resume_summary, jd_list)
    else:
        rank_example = [
            "QC85LpEBIvxPMcUyAMOd",
            "Qy85LpEBIvxPMcUyAMOd",
            "RC85LpEBIvxPMcUyAMOd",
            "Ri85LpEBIvxPMcUyAMOd",
            "SC85LpEBIvxPMcUyAMOd"
        ]
        rank_id_list=rank_example
    
    ranked_jds=retrieve_jds(rank_id_list)
    
    return ranked_jds