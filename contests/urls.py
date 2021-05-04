from django.urls import path
from . import views

app_name = 'contests'

urlpatterns = [
    path('contest/', views.view_contest, name='view_contest'),
    path('contest/<int:contest_id>/', views.detail, name='detail'),
    path('exercise/<int:exercise_id>/', views.submit_exercise, name='submit_exercise'),
    # path('job-single/<int:exercise_id>/', views.job_single, name='job-single'),
    path('create_contest/', views.create_contest.as_view(), name='create_contest'),
]