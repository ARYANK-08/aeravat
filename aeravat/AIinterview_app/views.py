from django.shortcuts import render
from django.http import JsonResponse
import os
from gtts import gTTS
import speech_recognition as sr
import pyttsx3  


# Built-in questions
QUESTIONS = [
    "What is Django?",
    "What is a Django app?"
]

# Function to convert text to speech
def speak(text, language='en'):
    """Speaks the provided text in the specified language (default English)."""

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    if not voices:
        print("No voices available. Text-to-speech is not possible.")
        return

    for voice in voices:
        if language in voice.languages:
            engine.setProperty('voice', voice.id)
            break
    else:
        print(f"Voice for language '{language}' not found. Using the default voice.")

    engine.say(text)
    engine.runAndWait()



# Function to listen for user's response
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        print("hi")  # Adjust for ambient noise
        audio = recognizer.listen(source)
        print("hi2")  # Adjust for ambient noise

    try:
        print("Recognizing...")
        user_response = recognizer.recognize_google(audio)
        return user_response
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Error: {e}")
        return ""

# Main question view
def question_view(request):
    if request.method == 'POST':
        question_index = request.POST.get('question_index', 0)
        if question_index.isdigit() and int(question_index) < len(QUESTIONS):
            question = QUESTIONS[int(question_index)]
            speak(question)  # Speak the question
            user_response = listen()  # Listen for user's response
            return JsonResponse({
                'question': question,
                'response': user_response,
                'question_index': int(question_index) + 1
            })
        else:
            # If the question index is out of range, indicate that all questions have been asked
            return JsonResponse({'all_questions_asked': True})
    return render(request, 'roadmap/ai_interview.html')