from django.shortcuts import render,redirect
from django.http import JsonResponse
import google.generativeai as genai

from django.contrib import auth
from django.contrib.auth.models import User
from .models import chat



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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request,username=username,password = password)

        if user is not None:
            auth.login(request,user)
            return redirect('chatbot')
        else:
            error_message = 'username or password is wrong'
            return render(request,'login.html',{'error_message':error_message})
        
    else:
        return render(request,'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating password'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Passwords don’t match'
            return render(request, 'register.html', {'error_message': error_message})
            
    return render(request,'register.html')


def logout(request):
    auth.logout(request)
    return redirect('login')