# django-banter
Investigating the use of Django to manage and execute algorithms.

## Structure
Core project is named 'ecg'. There is a single app called 'core'. The base HTML file is templates/base.html. 

```bash
ecg
|   db.sqlite3
|   manage.py
|   tree.txt
|           
+---core
|   |   admin.py
|   |   apps.py
|   |   forms.py
|   |   models.py
|   |   tests.py
|   |   urls.py
|   |   views.py
|   |   __init__.py
|   |   
|   +---migrations
|   |   |   0001_initial.py
|   |   |   __init__.py
|   |           
|   +---templates
|   |       file_upload.html
|   |       index.html
|   |       login.html
|   |       messages.html
|   |       navbar.html
|   |       register.html
|   |       run_script.html
|   |       show_files.html
|   |       
|           
+---ecg
|   |   asgi.py
|   |   settings.py
|   |   urls.py
|   |   wsgi.py
|   |   __init__.py
|           
+---media
|   +---algorithm
|   |       add_half_M3r8RWx.m
|   |       extract_12leads.m
|   |       handler.asv
|   |       handler.m
|   |       take_half_ws3u8BZ.m
|   |       
|   +---results
|   \---user_data
|           mj_0890794f-23c3-46f6-bcf9-b5bede7534fc.mat
|           mj_a5259203-4ed5-476a-9381-4aab932bf9cf.mat
|           mj_d59fca4d-c076-4fe3-bd1b-cacfdb1c7b5f.csv
|           
+---static
|   |   base.js
|   |   run_script.js
|   |   
|   +---core
|   \---css
|           materialize.css
|           
+---templates
        base.html
       
        
```

## Dependencies
The venv was created using Python 3.7. Packages required are:
- Django
- Matlab Engine for Python
