from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_request, name='logout'),
    path('upload/', views.upload, name='upload'),
    path('account/', views.show_files, name='show_files'),
    path('run_script/', views.run_script, name='run_script'),
    path('download_result/<int:file_id>', views.download_result, name='download_result'),
    path('run_script/get_scripts/<slug:data_input_id>/', views.get_scripts, name='get_scripts'),
    path('create_algorithm/', views.create_algorithm, name='create_algorithm'),
    path('algorithm_buider/', views.algorithm_builder, name='algorithm_builder'),
    path('run_algorithm/', views.run_algorithm, name='run_algorithm'),
    path('login/', views.login_request, name='login'),  # login must be at the end due to @login_required
]
