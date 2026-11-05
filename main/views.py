
from django.http import JsonResponse, request
from django.forms.models import model_to_dict
from django.shortcuts import redirect, render
from main.models import Subtask, User, Task
from main.forms import RegistrationForm, LoginForm, SubtaskForm
from django.contrib.auth import login, logout
from openai import OpenAI
from dotenv import load_dotenv
from datetime import timedelta


load_dotenv()


# Create your views here.
def main(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("screen3")
    return render(request, "main/main.html", {"form": form})


def screen3_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        date_str = request.POST.get("date")
        duration = request.POST.get("duration")
        Task.objects.create(
            title=title,
            description=description,
            user=request.user,
            start_datetime=date_str,
            duration=duration,
        )
        return redirect("screen3")
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
        print(tasks)

    return render(request, "main/screen3.html", {"tasks": tasks})


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


def getcalender_events(request):
    tasks = Task.objects.filter(user=request.user)
    print(tasks)
    all_tasks = []
    for task in tasks:
        if task.start_datetime and task.duration:
            time_end = task.start_datetime + timedelta(minutes=task.duration)
            all_tasks.append(
                {
                    "id": task.id,
                    "title": task.title,
                    "start": str(task.start_datetime.isoformat()),
                    "end": str(time_end.isoformat()),
                }
            )
    print(all_tasks)
    return JsonResponse(all_tasks, safe=False)

def screen4_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        date_str = request.POST.get("date")
        duration = request.POST.get("duration")
        Task.objects.create(
            title=title,
            description=description,
            user=request.user,
            start_datetime=date_str,
            duration=duration,

        )
        return redirect("screen4")
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
        print(tasks)
    return render(request, "main/screen4.html", {"tasks": tasks})


def toggle_subtask(request):
    if request.method == "POST":
        subtask_id = request.POST.get("subtask_id")
        is_completed = request.POST.get("is_completed")
        subtask = Subtask.objects.get(id=subtask_id, task__user=request.user)
        if is_completed == "true":
            subtask.completed = True
        else:
            subtask.completed = False
        subtask.save()
        return JsonResponse({"status": "success"})
    return redirect("screen4")



def subtask_update(request): 
   if request.method == "POST":
        subtask_id = request.POST.get("subtask_id")

        if subtask_id:
            subtask = Subtask.objects.get(id=subtask_id, task__user=request.user)
            subtask.title = request.POST.get("title")
            subtask.description = request.POST.get("description")
            subtask.priority_level = request.POST.get("priority_level") or None
            subtask.dresscode = request.POST.get("dresscode")
            subtask.checklist = request.POST.get("checklist")
            subtask.save()
        else:
            task_id = request.POST.get("task_id")
            task = Task.objects.get(id=task_id, user=request.user)
            title = request.POST.get("title")
            Subtask.objects.create(
                task=task,
                title=title,
            )
        print(request.POST)
        return redirect("screen4")

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()
    return redirect(request.META.get('HTTP_REFERER'))  # Redirect back to the previous page

def get_event(request, task_id):
    if request.user.is_authenticated:
        task = Task.objects.get(id=task_id, user= request.user)
        return JsonResponse(model_to_dict(task))
    return JsonResponse({'error':'Not found'}, status=404)

