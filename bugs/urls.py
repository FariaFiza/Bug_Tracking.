from django.urls import path
from . import views

urlpatterns = [
    path('', views.bug_list, name='bug_list'),
    path('create/', views.bug_create, name='bug_create'),
    path('<int:pk>/', views.bug_detail, name='bug_detail'),
    path('<int:pk>/edit/', views.bug_edit, name='bug_edit'),
    path('<int:pk>/delete/', views.bug_delete, name='bug_delete'),
    path('feedback/', views.feedback_list, name='feedback_list'),
    path('feedback/new/', views.feedback_create, name='feedback_create'),
]