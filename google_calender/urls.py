from django.contrib import admin
from django.contrib.admin import views
from django.urls import path

from main.views import (
    main,
    me,
    toggle_subtask,
    update_task_status,
    screen3_view,
    registration_view,
    logout_view,
    request_chatgpt,
    getcalender_events,
    screen4_view,
    subtask_update,
    delete_task,
    get_event
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", main, name="main"),
    path("me/", me, name="me"),
    path("update_task_status/", update_task_status, name="update_task_status"),
    path("screen3/", screen3_view, name="screen3"),
    path("registration/", registration_view, name="registration"),
    path("logout/", logout_view, name="logout"),
    path("request_chatgpt/", request_chatgpt, name="request_chatgpt"),
    path("getcalender_events/", getcalender_events, name="getcalender_events"),
    path("screen4/", screen4_view, name="screen4"),
    path("toggle_subtask/", toggle_subtask, name="toggle_subtask"),
    path("subtask_update/", subtask_update, name="update_subtask"),
    # delete_task/task_id
    path("delete_task/<int:task_id>/", delete_task, name="delete_task"), #dynamic URL
    path("get_event/<int:task_id>/", get_event, name="get_event"),
]
