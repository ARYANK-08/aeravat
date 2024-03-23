from django.shortcuts import render
import re
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from datetime import datetime, timedelta
from .models import WeekTask
from django.core.serializers.json import DjangoJSONEncoder



def get_start_of_week(date_obj):
    # Calculate the Monday of the week for the given date
    return date_obj - timedelta(days=date_obj.weekday())

load_dotenv()
genai.configure(api_key=(os.getenv("GOOGLE_API_KEY")))
# Create your views here.
pairs=''
button_values = [
    "frontend", "backend", "devOps", "fullstack", "android", "postgresql", 
    "ai-and-data-scientist", "blockchain", "qa", "software-architect", 
    "aspnet-core", "flutter", "cyber-security", "ux-design", "react-native", 
    "game-developer", "technical-writer", "datastructures-and-algorithms", 
    "mlops", "computer-science", "react", "angular", "vue", "javascript", 
    "nodejs", "typescript", "python", "sql", "system-design", "java", 
    "spring-boot", "golang", "rust", "graphql"
]

def match_button_values(phases, details):
    matched_values = []

    # Convert phases and details to lowercase for case-insensitive matching
    combined_text = " ".join(phases + details).lower()

    # Specific cases for matching
    if "django" in combined_text:
        matched_values.append("backend")
    
    # General matching for other values
    for value in button_values:
        if value in combined_text:
            matched_values.append(value)
    
    return matched_values
def overall(request):
    global pairs
    # skills = UserProfile.objects.filter(email = 'kyathamaryan@gmail.com').values_list('skills')
    # lang = UserProfile.objects.filter(email = 'kyathamaryan@gmail.com').values_list('language')
    role = 'Front End Developer'
    dreamcompany = 'Amazon'
    preferred_stack = 'HTML, CSS, JavaScript'
    genai.configure(api_key=(os.getenv("GOOGLE_API_KEY")))  # Set up your API key

    # Set up the model
    generation_config = {
        "temperature": 0.1,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    convo = model.start_chat(history=[])
    context = 'Act as an advisor for engineering students by providing them a roadmap of things they should do to get their desired role in their dream company. Give a generalised roadmap on the basis of their preferred stack with the main topics along the lines of languages, algorithms, frameworks ,opensource courses, tools like hackerank or leetcode, and other main topics they should learn. Give 7 phases .Basically give me a proper roadmap of main topics that one needs to master in order to get a the desired role. Note: Under each Phase give a Details: '
    convo.send_message(f"{context} Role:{role}, Dream Company: {dreamcompany}, Preferred stack to work with : {preferred_stack}")
    result = convo.last.text
    print(result)
    main_heading = re.search(r'\*\*([^*]+)\*\*', result).group(1)

    phases = re.findall(r'\*\*Phase \d+: ([^\n]+)', result)
    details = re.findall(r'\*\*Details:\*\*\n(.+?)(?=\n\n\*\*Phase|\Z)', result, re.DOTALL)

    formatted_details = [detail.replace('*', '<br>') for detail in details]

    # Printing extracted information
    # print("Main Heading:", main_heading)
    # print("Phase Topics:", phases)
    # print("Details:", details)
    phase_detail_pairs = zip(phases, formatted_details)
    # print(phase_detail_pairs)
    pairs = details

    matched_buttons = match_button_values(phases, details)
    print(matched_buttons)
    context = {
        'phase_detail_pairs': phase_detail_pairs,
        'matched_buttons' : matched_buttons

    }
    

    return render(request, 'roadmap/overall.html',context)

def category(request):
    
    button_id = request.GET.get('roadmap', 'python')
    # Use button_id as needed
    url = f'https://roadmap.sh/pdfs/roadmaps/{button_id}.pdf'
    user_input = request.POST.get('user_question')

    
    genai.configure(api_key=(os.getenv("GOOGLE_API_KEY")))  # Set up your API key

# Set up the model
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    convo = model.start_chat(history=[])
    context = 'You are an AI educator which scrapes the pdf from the link given and provides the response to the users question in 500 words with additional links and resources for the users question. If the user asks for a flowchart give a flowchart with explanation'
    convo.send_message(f"{context} Link:{url}, User Question : {user_input}")
    result = convo.last.text
    return render(request, 'roadmap/roadmap.html', {'result': result, 'url' : url})
from json import dumps
def personal(request):
    global pairs
    # skills = UserProfile.objects.filter(email = 'kyathamaryan@gmail.com').values_list('skills')
    # lang = UserProfile.objects.filter(email = 'kyathamaryan@gmail.com').values_list('language')
    placement = 'August 2024'
    proficiency = 'HTML : Intermediate, Javascript: Beginner, CSS: Intermediate'
    genai.configure(api_key=(os.getenv("GOOGLE_API_KEY")))  # Set up your API key

    # Set up the model
    generation_config = {
        "temperature": 0.1,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    convo = model.start_chat(history=[])
    context = '''Todays date is 23rd March 2024.
    You need to give a personalised roadmap for engineering students so that they can get their dream job.
    You will be givien with the placement time, Skills he needs to acquire, his current skills and proficiency in it.
    Calculate the weeks remaining from 23rd March 20 24 to the placement time and divide the skills he needs to acquire into weekly basis. example Week 1 : What he needs to learn. etc.
    Make sure that each week has a detailed explanation of what needs to be done in 50 words, along with projects which will improve his current skill.
    After weeks of skill acquisition is completed, Give him suggestions of projects coding competetions hackathons , leetcode solving during skill acquisition side by side.
    Also the last week is reserverd for interview preparation and practice. On the basis of this give me a detailed personalised roadmap 
    '''
    convo.send_message(f"{context} Placement Time: {placement}, Required Skills :{pairs}, Current Skillset and proficiency: {proficiency}")
    result = convo.last.text
    print(result)
    week_pattern = r'\*\*Week \d+:(.*?)\*\*Week \d+:|\Z'

    # Scrape weeks and tasks
    weeks_tasks_matches = re.findall(week_pattern, result, re.DOTALL)
    weeks_tasks = [week.strip() for week in weeks_tasks_matches if week.strip()]

# Create dictionaries for weeks 1 to 10 and weeks 11 to 20
    weeks_dict = {}
    weeks_tasks_dict_11_to_20 = {}

    for idx, task in enumerate(weeks_tasks):
        if idx < 10:
            weeks_dict[f"Week {idx + 1}"] = task.strip()
        elif idx < 20:
            weeks_tasks_dict_11_to_20[f"Week {idx + 1}"] = task.strip()

    # print(weeks_dict)
    # print(weeks_tasks_dict_11_to_20)
    start_date = datetime.now().date()  # Use the current date as the starting point
    for idx, (week, task) in enumerate(weeks_dict.items()):
        week_start_date = get_start_of_week(start_date + timedelta(weeks=idx))
        WeekTask.objects.create(date=week_start_date, task=task)
    # print(additional_tasks)

    
    return render(request,'roadmap/personal.html',{'weeks_dict' : weeks_dict})

def fullcalendar(request):
    # Query the database to retrieve WeekTask objects
    week_tasks = WeekTask.objects.all()

    # Convert WeekTask objects to FullCalendar event format
    events = {}
    for task in week_tasks:
        end_time = task.date + timedelta(hours=4)

        # Use task ID as the key for each event to ensure uniqueness
        events[task.id] = {
            'title': task.task,
            'start': task.date.isoformat(),  # Assuming start_time is already in ISO 8601 format
            'end': end_time.isoformat(),  # Assuming end_time is available in the model
        }

    # Convert events dictionary to JSON format
    data_json = dumps(events, cls=DjangoJSONEncoder)
    print(data_json)

    # Pass the JSON data to the template
    context = {'events_json': data_json}
    return render(request, 'roadmap/fullcalendar.html', context)

from bs4 import BeautifulSoup
import requests
def hackathons(request):
    # URL of the website to scrape
    url = "https://devfolio.co/hackathons"

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the relevant HTML elements containing the data you want to scrape
    hackathon_links = soup.find_all("a", class_="lkflLS")
    hackathon_categories = soup.find_all("p", class_="kCrHaC")
    hackathon_dates = soup.find_all("p", class_="ddThIB")
    participating_element = soup.find_all("p", class_="sc-cHPgQl ioimQF")

    hackathons_data = []
    for link, category, date, participating_element in zip(hackathon_links, hackathon_categories, hackathon_dates, participating_element):
        title = link.find("h3", class_="guEEhq").text.strip()
        href = link["href"]
        category_text = category.text.strip()
        date_text = date.text.strip()
        participating_text = participating_element.text.strip()
        hackathons_data.append({"title": title, "link": href, "category": category_text, "date": date_text, "participating": participating_text})

    # Pass data to the template
    return render(request, 'pages/hackathons.html', {'hackathons': hackathons_data})