quick start
```
source venv/bin/activate
export DATABASE_URL=
doppler run -- python manage.py runserver
```  
https://dashboard.doppler.com/workplace/87fa3aecaa170026448c/projects/django-api/configs/dev  
```
python manage.py makemigrations
python manage.py migrate
```
```
doppler run --config dev -- python manage.py runserver
```
running with Gunicorn for render.
```
doppler run -- python -m gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker
```
http://127.0.0.1:8000/api/hello/  
get started
```
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
export DATABASE_URL=
echo $DATABASE_URL
echo $OPENSEARCH_USERNAME_HOST 
echo $OPENSEARCH_USERNAME 
echo $OPENSEARCH_PASSWORD 
echo $GOOGLE_API_KEY
python manage.py migrate
python manage.py runserver
```
```
pip freeze > requirements. txt
```
use `export DOPPLER_TOKEN=` to access env var, or
```
doppler login
doppler setup
```  
doppler get started:  
https://github.com/wusixuan0/seed-supabase/blob/main/README.md  

match script overview:  
A job matching system that takes a user's resume PDF as input and returns the top 5 best-matching job descriptions from a dataset of 51,863 job listings stored in OpenSearch, scraped from Google Jobs.   
steps:  
1. extract_resume function: One API call to Gemini API
2. OpenSearch (ES) query: Retrieve 60 job descriptions based on extracted resume data.
3. Rank by Gemini API, returns list of id
4. Retrieve OpenSearch full records with list of id

api structure   
```
my-project/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── services
│   ├── utils.py     # Add this file for helper functions
│   ├── serializers.py  
│   └── urls.py      
├── manage.py
├── venv/
└── requirements.txt
```  
1. Extract the resume and save the API response to resume_summary in the model.
2. Perform the OpenSearch query and Gemini API call, saving the returned response to job_id_list in the model.
3. Retrieve OpenSearch full records with the list of IDs and send back the response.

### api structure summary before adding match script  
model.py:    
MatchRecord model with fields resume_summary, job_id_list, created_at, updated_at

views.py:  
Import generics and define MatchRecordCreateView

serializers.py:
Define MatchRecordSerializer

urls.py (app level):  
Define urlpatterns for MatchRecordCreateView

urls.py (project level):  
Include the app's URLs

### tutorial steps:  
```
touch django-api
cd django-api
# Create a virtual environment to isolate our package dependencies locally
python3 -m venv venv
source venv/bin/activate
pip install django djangorestframework && pip freeze > requirements.txt
// Create the Django project in the current directory
django-admin startproject config .
python manage.py startapp api
```

Your project structure should now look like this:
```
my-project/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
├── venv/
└── requirements.txt
```


```
touch api/urls.py

```
add app route to config/urls.py  
add Hello World to api/urls.py  
http://127.0.0.1:8000/api/hello/

