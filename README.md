#django-banter
Investigating the use of Django to manage and execute algorithms.

## Structure
Core project is named 'ecg'. There is a single app called 'core'. The base HTML file is templates/base.html. 

'''bash
C:.
│   db.sqlite3
│   manage.py
│   tree.txt
│   
├───.idea
│   │   .gitignore
│   │   ecg.iml
│   │   misc.xml
│   │   modules.xml
│   │   vcs.xml
│   │   workspace.xml
│   │   
│   └───inspectionProfiles
│           profiles_settings.xml
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
│   ├───migrations
│   │   │   0001_initial.py
│   │   │   0002_file_uploaded_file.py
│   │   │   0003_auto_20200825_1851.py
│   │   │   0004_auto_20200825_1859.py
│   │   │   0005_auto_20200825_1905.py
│   │   │   0006_auto_20200825_2118.py
│   │   │   __init__.py
│   │           
│   ├───templates
│   │       file_upload.html
│   │       index.html
│   │       login.html
│   │       messages.html
│   │       navbar.html
│   │       register.html
│           
├───ecg
│   │   asgi.py
│   │   settings.py
│   │   urls.py
│   │   wsgi.py
│   │   __init__.py
│           
├───media
│       mj2_496ab599-90b0-4314-bc12-bdac808ef12d.pdf
│       mj2_b9d874c4-b670-4595-a8f6-d529995f210d.pdf
│       
├───static
│   ├───core
│   └───css
│           materialize.css
│           
├───templates
        base.html
'''
