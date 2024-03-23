from django.shortcuts import render

# Create your views here.


def companies(request):
    return render (request,'roadmap/companies.html')

def aboutamazon(request):
    return render (request,'roadmap/aboutamazon.html')

def amazonaptitude(request):
    return render (request, 'roadmap/amazonaptitude.html')
from .models import Quiz

# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Quiz, Question, Option, Response

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'roadmap/quiz_list.html', {'quizzes': quizzes})
# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Quiz, Question, Option, Response

def quiz_detail(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    return render(request, 'roadmap/quiz_detail.html', {'quiz': quiz})


from django.shortcuts import render
from django.http import HttpResponse
from .models import Question, Option, Response

# def save_response(request):
#     if request.method == 'POST':
#         score = 0  # Initialize score counter
#         total_questions = 0  # Initialize total questions counter

#         for key, value in request.POST.items():
#             if key.startswith('question_'):
#                 question_id = int(key.split('_')[1])
#                 selected_option_id = int(value)
#                 question = Question.objects.get(pk=question_id)
#                 selected_option = Option.objects.get(pk=selected_option_id)
                
#                 total_questions += 1  # Increment total questions counter

#                 if selected_option.is_correct:
#                     score += 1  # Increment score if selected option is correct

#                 response = Response(question=question, option=selected_option)
#                 response.save()
        
#         # Calculate percentage score
#         percentage_score = (score / total_questions) * 100 if total_questions > 0 else 0

#         # Categorize user's performance
#         if percentage_score < 30:
#             performance = "beginner"
#         elif percentage_score < 70:
#             performance = "intermediate"
#         else:
#             performance = "proficient"

#         # Prepare context data
#         context = {
#             'score': score,
#             'total_questions': total_questions,
#             'percentage_score': percentage_score,
#             'performance': performance.capitalize(),
#         }

#         # Render the response template with context data
#         return render(request, 'pages/save_response.html', context)
#     else:
#         return HttpResponse("Invalid request method!")


def save_response(request):
    if request.method == 'POST':
        score = 0  # Initialize score counter
        total_questions = 0  # Initialize total questions counter

        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])
                selected_option_id = int(value)
                question = Question.objects.get(pk=question_id)
                selected_option = Option.objects.get(pk=selected_option_id)
                
                total_questions += 1  # Increment total questions counter

                if selected_option.is_correct:
                    score += 1  # Increment score if selected option is correct

                response = Response(question=question, option=selected_option)
                response.save()
        
        # Calculate percentage score
        percentage_score = (score / total_questions) * 100 if total_questions > 0 else 0
        
        # Calculate incorrect answers
        incorrect_answers = total_questions - score

        return render(request, 'roadmap/save_response.html', {
            'score': score,
            'total_questions': total_questions,
            'percentage_score': percentage_score,
            'incorrect_answers': incorrect_answers
        })
    else:
        return HttpResponse("Invalid request method!")
