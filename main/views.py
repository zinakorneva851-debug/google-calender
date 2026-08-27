from xmlrpc import client

from django.http import JsonResponse
from django.shortcuts import redirect, render
from main.models import User, Task
from main.forms import RegistrationForm, LoginForm
from django.contrib.auth import login, logout
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


# Create your views here.
def main(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("app")
    return render(request, "main/main.html", {"form": form})


def app_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        Task.objects.create(title=title, description=description, user=request.user)
        return redirect("app")
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
        print(tasks)
    return render(request, "main/app.html", {"tasks": tasks})


def me(request):
    return render(request, "main/me.html")


def update_task_status(request):
    if request.method == "POST":
        print(request.POST)
        task_id = request.POST.get("task_id")
        is_completed = request.POST.get("is_completed")
        print(f"Task ID: {task_id}, Is Completed: {is_completed}")
        task = Task.objects.get(id=task_id)
        if is_completed == "true":
            completed = True
        else:
            completed = False
        task.completed = completed
        task.save()
        return JsonResponse({"status": "success"})


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("app")
    else:
        form = RegistrationForm()
    return render(request, "main/registration.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("main")


def request_chatgpt(request):
    if request.method == "POST":
        chatgpt_request = request.POST.get("chatgpt")
        client = OpenAI()
        response = client.responses.create(
            model="gpt-5.4-mini",
            instructions="Do not use Markdown formatting in your response. Use Html formatting instead. Use Html tags like <p>, <b>, <i>, <ul>, <li> etc. to format your response.",
            input=chatgpt_request,
        )
        print(response.output_text)
        return JsonResponse({"response": response.output_text})
