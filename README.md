# Server-Side Execution
Investigating the use of server-side processing to manage and execute algorithms in a code-free environment. 
This is a Django-based (Python) project

## Example Use-Case
This project has been designed to promote the democratisation of digital signal processing (DSP) to non-developers. 
This system may be used by non-developers or clinicians to process biomedical data in a trial-and-error format without 
the need to write code or have a deep understanding of DSP principles.

## Usage
1. Create your `SECRET_KEY` in `ecg/ecg/settings.py`. By default, the system looks for a file. Feel free to comment this out and use the example `SECRET_KEY` for development
2. In the project directory, install dependencies using:
```commandline
pip install -r requirements.txt
```
3. Start the project using:
```commandline
python manage.py runserver
```
4. Navigate to `http://127.0.0.1:8000/` in your web browser to view the app. If you have another web app running, use:
```commandline
python manage.py runserver 8080
```
5. Create an administrator account
```commandline
python manage.py createsuperuser
```
6. Ensure the project is running via point four. Access the admin interface via `http://127.0.0.1:8000/admin/`
7. As an admin, upload `Script` files as either MATLAB or Python files that accept a single argument with the file path
   of the data file. They must output a single data file.
8. Create a user login via `http://127.0.0.1:8000/register/`
9. Upload data as a user via `http://127.0.0.1:8000/upload/`
10. View user files via `http://127.0.0.1:8000/show_files/`
11. Process a script by creating an algorithm using `http://127.0.0.1:8000/create_algorithm/`
12. View the created algorithms via `http://127.0.0.1:8000/show_files/show_algorithms/`

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
|   |       * This is the uploaded scripts (MATLAB or Python)
|   |       add_half_M3r8RWx.m
|   |       extract_12leads.m
|   |       filter_ecg.py
|   |       handler.asv
|   |       handler.m
|   |       take_half_ws3u8BZ.m
|   |       
|   +---results
|   \---user_data
|           * This is the uploaded user-data
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
The venv was created using Python 3.7. Packages required are found in requirements.txt

## Acknowledgements
This project is part of the Eastern Corridor Medical Engineering Centre (ECME). It is supported by the European Union’s INTERREG VA Programme, managed by the Special EU Programmes Body (SEUPB).