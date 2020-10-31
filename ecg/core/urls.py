from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_request, name='logout'),
    path('upload/', views.upload, name='upload'),
    path('account/', views.show_files, name='show_files'),
    path('run_script/', views.run_script, name='run_script'),
    path('run_script/get_scripts/<slug:data_input_id>/', views.get_scripts, name='get_scripts'),
    path('download_file/<slug:file_id>/', views.download_file, name='download_file'),
    path('download_file/<slug:file_id>/<int:delete>/', views.download_file, name='download_file'),
    path('delete_file/<slug:file_id>/', views.delete_file, name='delete_file'),
    path('create_algorithm/', views.create_algorithm, name='create_algorithm'),
    path('create_algorithm/<slug:input_file_id>/', views.create_algorithm, name='create_algorithm'),
    path('show_algorithms/', views.show_algorithms, name='show_algorithms'),
    path('delete_algorithm/<slug:algorithm_id>', views.delete_algorithm, name='delete_algorithm'),
    path('login/', views.login_request, name='login'),  # login must be at the end due to @login_required
]
