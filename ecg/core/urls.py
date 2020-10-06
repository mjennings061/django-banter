from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('upload/', views.upload, name='upload'),
    path('account/', views.show_files, name='show_files'),
    path('run_subprocess/', views.run_subprocess, name='run_subprocess'),
    path('download_result/<int:file_id>', views.download_result, name='download_result')
]
