from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib import messages  # alert the user
from django.contrib.auth import login, logout as django_logout, authenticate  # user handling (register)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User  # import django's model for the user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import json as simplejson   # for handling AJAX queries from forms
from django.urls import reverse
import os
from django.core.exceptions import ObjectDoesNotExist

from .models import File, Script, Execution, Algorithm
from .forms import NewUserForm, UploadFileForm, ExecutionSelectForm, AlgorithmForm


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


@login_required
def show_files(request):
    current_user = request.user
    files = File.objects.filter(
        user=current_user
    )

    context = {
        'current_user': current_user,
        'files': files,
    }
    return render(request, 'show_files.html', context)


@login_required
def download_file(request, file_id, delete=0):
    """ Download a user file and delete if requested (1) """
    file = File.objects.get(identifier=file_id)
    if file.uploaded_file.path:
        if request.user.id is file.user.id:     # if the file belongs to the user requesting it
            file_path = file.uploaded_file.path
            with open(file_path, 'rb') as fh:   # ensure the file is closed
                contents = fh.read()

            response = HttpResponse(contents, content_type=file.format.mime_type)
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            if delete:
                file.delete()
            return response
    raise Http404


@login_required
def delete_file(request, file_id):
    """ Delete a user file """
    try:
        file = File.objects.get(identifier=file_id)     # get the file instance
        if request.user.id is file.user.id:  # if the file belongs to the user requesting it
            file_path = file.uploaded_file.path
            file.delete()  # delete the file instance - this also triggers file deletion using a model signal
            messages.info(f'{file} deleted')
            return HttpResponseRedirect(reverse('show_files'))  # redirect to the file loading screen
    except ObjectDoesNotExist:  # if it does not exist, raise 404
        raise Http404


@login_required
def run_script(request):
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


@login_required
def get_scripts(request, data_input_id):
    """ Get all scripts compatible with the input file UUID """
    data_input = File.objects.get(pk=data_input_id).format  # get the file format of the input file
    scripts = Script.objects.filter(data_input=data_input)  # get the scripts with compatible inputs matching data_input
    script_dict = {}
    for script in scripts:  # form a dictionary with script IDs to fill the select form
        script_dict[script.id] = script.identifier
    return HttpResponse(simplejson.dumps(script_dict))  # return a JSON file with compatible scripts


@login_required
def create_algorithm(request, input_file_id=None):
    """ Create an algorithm instance before linking Executions to it """
    current_user = request.user
    if request.method == "POST":  # if data is posted
        algorithm_form = AlgorithmForm(request.POST, user=current_user)  # submit POST data to ModelForm
        if algorithm_form.is_valid():   # if all required data is fulfilled
            algorithm = Algorithm(
                name=algorithm_form.cleaned_data['name'],
                description=algorithm_form.cleaned_data['description'],
                user=current_user,
            )
            algorithm.save()    # save the instance of Algorithm
            algorithm.save_executions(algorithm_form.cleaned_data)  # create an Execution for each script selected
            output_file_id = algorithm.run_algorithm()   # run each Execution in the order they were selected
            if output_file_id is not None:
                messages.info(request, f"Created algorithm")    # success toasts
                messages.success(request, f"Algorithm processed successfully")
                return HttpResponseRedirect(reverse(f'download_file', kwargs={  # download and delete output file
                    'file_id': output_file_id,
                    'delete': 1
                }))
            else:
                algorithm_form = AlgorithmForm(user=current_user)
                messages.error(request, f"Could not create algorithm")
        else:
            messages.error(request, f"Could not create algorithm")
    elif input_file_id is not None:   # empty form during a GET request
        algorithm_form = AlgorithmForm(user=current_user, data_input_id=input_file_id)
    else:
        algorithm_form = AlgorithmForm(user=current_user)

    context = {
        'algorithm_form': algorithm_form,
    }
    return render(request, 'create_algorithm.html', context)


# TODO: create a page to see all user algorithms
@login_required()
def show_algorithms(request):
    current_user = request.user
    algorithms = Algorithm.objects.filter(user=current_user)
    context = {
        'current_user': current_user,
        'algorithms': algorithms,
    }
    return render(request, 'show_algorithms.html', context)


@login_required
def delete_algorithm(request, algorithm_id):
    """ Delete an algorithm """
    try:
        algorithm = Algorithm.objects.get(identifier=algorithm_id)     # get the algo instance
        if request.user.id is algorithm.user.id:  # if the algo belongs to the user requesting it
            algorithm.delete()
            messages.info(request, f'{algorithm} deleted')
            return HttpResponseRedirect(reverse('show_algorithms'))  # redirect
    except ObjectDoesNotExist:  # if it does not exist, raise 404
        messages.error(request, f'Algorithm not found')
        raise Http404
