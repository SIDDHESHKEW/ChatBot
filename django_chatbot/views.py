from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai

from django.contrib import auth

# Configure Gemini API
genai.configure(api_key="AIzaSyAb6zaHhIyM-uHAtgGoGQD2xgUy_GbpTWk")

def ask_gemini(message):
    try:
        # Create a model instance
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Send message to Gemini
        response = model.generate_content(message)

        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

def files(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_gemini(message)
        return JsonResponse({"message": message, "response": response})
    return render(request, 'chatbot.html')


def login(request):
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')

def logout(request):
    auth.logout(request)