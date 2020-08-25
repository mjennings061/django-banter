#django-banter
Investigating the use of Django to manage and execute algorithms.

## Structure
Core project is named 'ecg'. There is a single app called 'core'. The base HTML file is templates/base.html. 

     ecg
    │   db.sqlite3
    │   manage.py
    │           
    ├───core
    │   │   admin.py
    │   │   apps.py
    │   │   forms.py
    │   │   models.py
    │   │   tests.py
    │   │   urls.py
    │   │   views.py
    │   │   __init__.py
    │   │   
    │   │           
    │   ├───templates
    │           index.html
    │           login.html
    │           messages.html
    │           navbar.html
    │           register.html
    │         
    │           
    ├───ecg
    │   │   asgi.py
    │   │   settings.py
    │   │   urls.py
    │   │   wsgi.py
    │   │   __init__.py
    │   │   
    │   └───__pycache__
    │           settings.cpython-38.pyc
    │           urls.cpython-38.pyc
    │           wsgi.cpython-38.pyc
    │           __init__.cpython-38.pyc
    │           
    ├───static
    │   ├───core
    │   └───css
    │           materialize.css
    │           
    ├───templates
            base.html
