from django.http import HttpResponse, Http404
from django.contrib import messages  # alert the user
from django.contrib.auth import login, logout as django_logout, authenticate  # user handling (register)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User  # import django's model for the user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import json as simplejson   # for handling AJAX queries from forms

from .models import File, Script, Execution
from .forms import NewUserForm, UploadFileForm, ExecutionSelectForm


# Create your views here.
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)   # the form will be populated with POST data
        if form.is_valid():
            user = form.save()  # equivalent to model.save() to save the user
            username = form.cleaned_data.get('username')    # grab the username from the POST data
            messages.success(request, f"New Account Created: {username}")   # alert the user of success
            login(request, user)    # login the user
            messages.info(request, f"You are now logged in as {username}")
            return redirect("index")
        else:
            if form.errors is not None:     # check if the username already exists
                for msg in form.errors:
                    messages.error(request, f"{form.errors[msg][0]}")
            else:
                for msg in form.error_messages:  # display other error messages e.g. password miss-match
                    messages.error(request, f"{msg}: {form.error_messages[msg]}")

    form = NewUserForm  # show a blank form based on forms.NewUserForm
    return render(request,
                  "register.html",     # template to load
                  context={"form": form})   # pass the form details to the page


def logout_request(request):
    django_logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("index")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)   # get the form data
        if form.is_valid():
            username = form.cleaned_data.get('username')    # get data from the form
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("index")
            else:
                messages.error(request, "Invalid username/password")
        else:
            messages.error(request, "Invalid username/password")

    form = AuthenticationForm()
    return render(request,
                  "login.html",
                  {"form": form})


@login_required
def upload(request):
    form = UploadFileForm()
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = File(
                name=form.cleaned_data["name"],
                uploaded_file=form.files["uploaded_file"],
                user=user,
                format=form.cleaned_data["format"],
            )
            file.save()
            messages.info(request, f"File uploaded")
        else:
            messages.error(request, f"File not uploaded")

    context = {
        'form': form,
    }
    return render(request, 'file_upload.html', context)


# TODO Show only the file name, not the whole path (security)
@login_required
def show_files(request):
    current_user = request.user
    files = File.objects.filter(user=current_user)

    context = {
        'current_user': current_user,
        'files': files,
    }
    return render(request, 'show_files.html', context)


# TODO complete download and delete to return the resultant file
@login_required
def download_result(file_id):
    # TODO: Check the file ID exists and return a 404 if not
    # TODO: Only let the user download their own results
    response = HttpResponse(content_type='text/csv')    # TODO change to MIME type from File
    response['Content-Disposition'] = f"attachment; filename='{file_id}.csv'"
    return response


@login_required
def run_script(request):
    # TODO: Download the resultant file
    current_user = request.user     # get the logged in user
    if request.method == "POST":    # if data is posted
        execution_form = ExecutionSelectForm(request.POST, user=current_user)   # submit POST data to ModelForm
        if execution_form.is_valid():   # if the form is valid
            execution = Execution(      # submit ModelForm fields to Model
                data_input=execution_form.cleaned_data['data_input'],
                script=execution_form.cleaned_data['script'],
            )
            file_id = execution.run_file()    # Execute the File using the Script selected to produce data_output
            if file_id is not None or 0:  # if the script processed ok
                execution.save()        # save the execution instance as a database entry
                messages.success(request, f"File processed successfully")
            else:
                messages.error(request, f"File could not be processed")
    elif request.method == "GET":
        execution_form = ExecutionSelectForm(user=current_user)     # create an empty form with user files listed
    else:
        raise Http404("Unknown request")

    context = {
        'current_user': current_user,
        'execution_form': execution_form,
    }
    return render(request, 'run_script.html', context)


# Get all scripts compatible with the input file UUID
@login_required
def get_scripts(request, data_input_id):
    data_input = File.objects.get(pk=data_input_id).format  # get the file format of the input file
    scripts = Script.objects.filter(data_input=data_input)  # get the scripts with compatible inputs matching data_input
    script_dict = {}
    for script in scripts:  # form a dictionary with script IDs to fill the select form
        script_dict[script.id] = script.identifier
    return HttpResponse(simplejson.dumps(script_dict))  # return a JSON file with compatible scripts
