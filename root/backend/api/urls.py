from django.urls import path, include
from .views import ResumeProcessView, HelloWorld, MatchRecordCreateView

urlpatterns = [
    path('match/', ResumeProcessView.as_view(), name='match-resume'),
    path('hello/', HelloWorld.as_view(), name='hello_world'),
    path('match_records/', MatchRecordCreateView.as_view(), name='match-record-list-create'),
]