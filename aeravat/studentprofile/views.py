from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'base.html')


from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import fitz  # PyMuPDF
import re
from .models import Choice, StudentProfile

import re
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def find_information(text):
    """Finds specific information based on patterns."""
    info = {
        'name': None,
        'skills': [],
        'projects': [],
        'linkedin_profile': None,
        'email': None
    }
    # Regular expressions for matching patterns
 
def find_information(text):
    """Finds specific information based on patterns."""
    info = {
        'name': None,
        'skills': [],
        'projects': [],
        'linkedin_profile': None,
        'email': None
    }
    
    # Regular expressions for matching patterns
    name_pattern = re.compile(r"NAME\s*:\s*(.*)", re.IGNORECASE)
    skills_pattern = re.compile(r"SKILLS[\s\S]+?([\w\s,]+)\s*(?:\n|$)", re.IGNORECASE)
    projects_pattern = re.compile(r"Developed\s+(.*?)(?:Tech\s+Stack\s*:\s*(.*?))?\s*(?:$|\n)", re.IGNORECASE | re.DOTALL)
    linkedin_pattern = re.compile(r"Linkedin\s*:\s*(https?://[^\s]+)", re.IGNORECASE)
    email_pattern = re.compile(r"Email\s*:\s*([\w\.-]+@[\w\.-]+)", re.IGNORECASE)

    # Searching for matches in the text
    name_match = name_pattern.search(text)
    skills_match = skills_pattern.search(text)
    projects_matches = projects_pattern.findall(text)
    linkedin_match = linkedin_pattern.search(text)
    email_match = email_pattern.search(text)

    # Assigning matched information to the info dictionary
    if name_match:
        info['name'] = name_match.group(1).strip()
    if skills_match:
        info['skills'] = [skill.strip() for skill in skills_match.group(1).split(',')]
    for project, tech_stack in projects_matches:
        info['projects'].append({'name': project.strip(), 'tech_stack': tech_stack.strip()})
    if linkedin_match:
        info['linkedin_profile'] = linkedin_match.group(1).strip()
    if email_match:
        info['email'] = email_match.group(1).strip()

    return info

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import fitz  # PyMuPDF
import re
from django.http import HttpResponse
from .models import StudentProfile

# from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .models import StudentProfile

# Your existing extract_text_from_pdf and find_information functions go here

def upload_pdf(request):
    if request.method == 'POST':
        if 'pdf_file' in request.FILES:
            pdf_file = request.FILES['pdf_file']
            fs = FileSystemStorage()
            filename = fs.save(pdf_file.name, pdf_file)
            pdf_path = fs.path(filename)
            text = extract_text_from_pdf(pdf_path)
            extracted_info = find_information(text)
            
            # Redirect back with extracted info to pre-fill form
            return render(request, 'student/uploadcv.html', {'info': extracted_info})
        else:
            # Simply save the form data into StudentProfile model without any additional logic
            student_profile = StudentProfile.objects.create(
                name=request.POST.get('name'),
                linkedin_profile=request.POST.get('linkedin_profile'),
                skills=request.POST.get('skills'),
                current_year = request.POST.get('current_year'),
                placement_year = request.POST.get('placement_year'),
                desired_role=request.POST.get('desired_role'),
                preferred_industry=request.POST.get('preferred_industry'),
                technology_interests=request.POST.get('technology_interests'),
                email=request.POST.get('email')  # Ensure this field is in your form
            )
            # Inside your form processing else block, after extracting other form fields



            student_profile.save()  # This line is technically redundant as `create()` saves the model instance already.
            return redirect('/quiz/2/')  # Directly using the hardcoded URL for redirection

    else:
        # If it's a GET request, just show the form
        return render(request, 'student/uploadcv.html')


from django.shortcuts import render, get_object_or_404
from collections import defaultdict
from .models import Quiz, UserAnswer, StudentProfile, Question

def calculate_score(correct_answers, total_questions):
    return (correct_answers / total_questions * 100) if total_questions else 0

from django.shortcuts import redirect


def quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz).prefetch_related('choice_set')
    student_profile = get_object_or_404(StudentProfile, email=request.user.email)

    if request.method == 'POST':
        correct_answers = 0
        topic_performance = defaultdict(lambda: {'correct': 0, 'incorrect': 0})
        
        for question in questions:
            selected_choice_id = request.POST.get(str(question.id))
            if selected_choice_id:
                selected_choice = Choice.objects.get(id=selected_choice_id)
                UserAnswer.objects.create(
                    student_profile=student_profile,
                    question=question,
                    selected_choice=selected_choice
                )
                if selected_choice.is_correct:
                    correct_answers += 1
                    topic_performance[question.topic]['correct'] += 1
                else:
                    topic_performance[question.topic]['incorrect'] += 1

        total_questions = questions.count()
        score = calculate_score(correct_answers, total_questions)

        proficiency_level = 'Beginner'
        if score >= 80:
            proficiency_level = 'Advanced'
        elif score >= 50:
            proficiency_level = 'Intermediate'

        strengths, improvements = [], []
        for topic, performance in topic_performance.items():
            if performance['correct'] >= performance['incorrect']:
                strengths.append(topic)
            else:
                improvements.append(topic)

  

        # Prepare the context for rendering results
        context = {
            'quiz': quiz,
            'questions': questions,
            'score': score,
            'proficiency_level': proficiency_level,

            'show_results': True  # Flag to indicate that results should be shown
        }
        return redirect('quiz_results', quiz_id=quiz.id)

    else:
        context = {
            'quiz': quiz,
            'questions': questions,
            'show_results': True
        }
        return render(request, 'student/skill_assessment.html', context)


def quiz_results(request, quiz_id):
    # Fetch user's quiz answers
    student_profile = get_object_or_404(StudentProfile, email=request.user.email)
    user_answers = UserAnswer.objects.filter(student_profile=student_profile, question__quiz_id=quiz_id)
    total_questions = user_answers.count()
    correct_answers = sum(user_answer.is_correct() for user_answer in user_answers)
    score = calculate_score(correct_answers, total_questions)

    # Calculate proficiency level
    proficiency_level = 'Beginner'
    if score >= 80:
        proficiency_level = 'Advanced'
    elif score >= 50:
        proficiency_level = 'Intermediate'

    # Prepare question-wise results
    question_results = {}
    for user_answer in user_answers:
        question_text = user_answer.question.text
        is_correct = user_answer.is_correct()
        question_results[question_text] = is_correct

    # Calculate strengths and areas for improvement based on question topics
    topic_performance = defaultdict(lambda: {'correct': 0, 'incorrect': 0})
    for user_answer in user_answers:
        question = user_answer.question
        topic = question.topic
        if user_answer.is_correct():
            topic_performance[topic]['correct'] += 1
        else:
            topic_performance[topic]['incorrect'] += 1

    strengths, improvements = [], []
    for topic, performance in topic_performance.items():
        if performance['correct'] >= performance['incorrect']:
            strengths.append(topic)
        else:
            improvements.append(topic)
    print(strengths, improvements)
          # Prepare chart data after analyzing all topics
    strengths_chart_data = {
        'labels': [topic for topic in strengths],
        'datasets': [{
            'data': [topic_performance[topic]['correct'] for topic in strengths],
            'backgroundColor': ['#4caf50', '#2196f3', '#ffeb3b', '#ff9800', '#f44336'],
            'hoverOffset': 4
        }]
    }

    improvements_chart_data = {
        'labels': [topic for topic in improvements],
        'datasets': [{
            'data': [topic_performance[topic]['incorrect'] for topic in improvements],
            'backgroundColor': ['#f44336', '#ff9800', '#ffeb3b', '#2196f3', '#4caf50'],
            'hoverOffset': 4
        }]
    }
    print(strengths_chart_data,improvements_chart_data)
    context = {
        'score': score,
        'proficiency_level': proficiency_level,
        'total_questions': total_questions,
        'question_results': question_results,
    'strengths': strengths,  # Just pass the labels
    'improvements': improvements,  # Just pass the labels
    }
    return render(request, 'student/quiz_results.html', context)

def mentor(request):
    return render(request, 'student/mentor.html')


from django.shortcuts import render
from django.http import HttpResponse
import requests
from serpapi import GoogleSearch

def display_courses(request):
    courses = []

    topic = 'Front End Development'
    params = {
    "engine": "youtube",
    "search_query": topic,
    "gl": "in",
    "api_key": "63717a6375c3289fae06621a3846332972c18a825a8ac3297da171a34e15c854"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    courses = results.get('video_results', [])  # Safely get job results or empty list

    print(courses)
    return render(request, 'student/student_courses.html',{'courses': courses})
    
from serpapi import GoogleSearch
from django.shortcuts import render
from serpapi import GoogleSearch

def job_listings(request):
    jobs = []  # Default empty state for jobs


    job_type = 'Front End Developer'
    location = 'Mumbai'

    params = {
        "engine": "google_jobs",
        "google_domain": "google.co.in",
        "q": job_type,
        "hl": "hi",
        "gl": "in",
        "location": location,
        "api_key": "63717a6375c3289fae06621a3846332972c18a825a8ac3297da171a34e15c854"
    }


    search = GoogleSearch(params)
    results = search.get_dict()
    jobs = results.get('jobs_results', [])  # Safely get job results or empty list
    print(jobs)
    # Pass the jobs list to the template
    return render(request, 'student/jobs.html', {'jobs': jobs})


def dashboard(request):
    return render(request, 'student/dashboard.html')

from django.shortcuts import render
import requests

import requests
from requests.exceptions import ConnectTimeout, RequestException
from django.shortcuts import render

def profile(request):
    context = {}
    if 'username' in request.GET:
        username = request.GET['username']
        url = f"https://api.github.com/users/{username}/repos"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for non-200 status codes
            repos = response.json() if response.status_code == 200 else []
            context['repos'] = repos
        except ConnectTimeout:
            error_message = "Connection to GitHub API timed out. Please try again later."
            context['error'] = error_message
        except RequestException as e:
            error_message = f"An error occurred while fetching data from GitHub API: {e}"
            context['error'] = error_message
    return render(request, 'student/profile.html', context)

def landing(request):
    return render(request, 'landing.html')