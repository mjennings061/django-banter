# django-banter
Investigating the use of Django to manage and execute algorithms.

## Structure
Core project is named 'ecg'. There is a single app called 'core'. The base HTML file is templates/base.html. 

```bash
ecg
|   db.sqlite3
|   manage.py
|           
+---core
|   |   admin.py
|   |   apps.py
|   |   forms.py
|   |   mlab.py
|   |   models.py
|   |   tests.py
|   |   urls.py
|   |   views.py
|   |   __init__.py
|   |   
|   |           
|   +---templates
|   |       file_upload.html
|   |       index.html
|   |       login.html
|   |       messages.html
|   |       navbar.html
|   |       register.html
|   |       run.html
|   |       show_files.html
|   |       
|           
+---ecg
|   |   asgi.py
|   |   settings.py
|   |   urls.py
|   |   wsgi.py
|   |   __init__.py
|   |   
|           
+---media
|   |   mj_6c493203-13fa-482f-a815-5821a9ed29c3.csv
|   |   SillyBilly_65a545a2-93d1-4811-b765-32b08bc27c4e.csv
|   |   SillyBilly_6ea0357d-0289-4f6a-8f73-0daae04980eb.csv
|   |   SillyBilly_761a838c-b711-48f0-984e-a50ae4a80e57.csv
|   |   SillyBilly_8989c5a7-ad88-4b35-8712-f0df8a0e1a2b.csv
|   |   SillyBilly_f823d1ff-7f8b-4443-b22c-10211a63dac6.csv
|   |   
|   +---algorithm
|   |       LPF_single_row.asv
|   |       LPF_single_row.m
|   |       
|   \---results
|           LPF_single_row_result.csv
|           
+---static
|   +---core
|   \---css
|           materialize.css
|           
+---templates
        base.html
        
```
