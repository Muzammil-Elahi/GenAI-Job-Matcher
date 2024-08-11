
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework import generics
from .models import MatchRecord
from .serializers import MatchRecordSerializer
from api.services.main import upload_resume
from django.views import View
from django.http import JsonResponse
import logging
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class ResumeProcessView(APIView):
    def post(self, request):
        if 'resume' in request.FILES:
            try:
                return upload_resume(request)
            except Exception as e:
                logger.error(f"Error in ResumeProcessView: {str(e)}", exc_info=True)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

class HelloWorld(APIView):
    def get(self, request):
        resume_url="https://daaouztnkoascsishisv.supabase.co/storage/v1/object/public/icons/resumes/test_resume.pdf?t=2024-08-07T18%3A54%3A47.255Z"
        return Response({"ranked_jds": upload_resume(resume_url)})
    
class MatchRecordCreateView(generics.ListCreateAPIView):
    queryset = MatchRecord.objects.all()
    serializer_class = MatchRecordSerializer