from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib import messages  # alert the user
from django.contrib.auth import login, logout as django_logout, authenticate  # user handling (register)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User  # import django's model for the user
from django.shortcuts import render, redirect

from core.models import File, Script, Execution
from .forms import NewUserForm, UploadFileForm, ScriptForm  # import our own custom form


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


def upload(request):
    # UploadFileForm.base_fields['format'] = forms.ModelChoiceField(queryset=FileFormat.objects.values('name'))
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
def show_files(request):
    if request.user.is_authenticated:
        current_user = request.user
        files = File.objects.filter(user=current_user)
    else:
        current_user = None

    context = {
        'current_user': current_user,
        'files': files,
    }
    return render(request, 'show_files.html', context)


# TODO complete download and delete to return the resultant file
def download_result(file_id):
    # TODO: Check the file ID exists and return a 404 if not
    # TODO: Only let the user download their own results
    response = HttpResponse(content_type='text/csv')    # TODO change to MIME type from File
    response['Content-Disposition'] = f"attachment; filename='{file_id}.csv'"
    return response


def run_script(request):
    # TODO: Render the available files and algorithms
    # TODO: Add a form and POST to select the file and algorithm to run
    # TODO: Download the resultant file
    # TODO: Add a dynamic form to select multiple compatible algorithms
    form = None     # the form does not matter if there is no user logged in
    if request.user.is_authenticated:
        current_user = request.user     # get the logged in user
        form = ScriptForm(user=current_user)  # populate the new form with user data
        data_files = File.objects.filter(user=current_user)     # get all files associated with the user
        scripts = Script.objects.all()     # get all scripts

        if request.method == "POST":
            execution = Execution()     # each execution of a script will have its own instance
            execution.data_input = data_files.get(name='007b Trimmed Data')  # assign input and script to run
            execution.script = Script.objects.get(identifier='mat.mj.addHalf')
            file_id = execution.run_file()  # run the script
            if file_id is not 0:    # if the script executed
                execution.save()    # save the instance to the database
    else:
        current_user = None
        scripts = None
        data_files = None

    context = {
        'form': form,
        'current_user': current_user,
        'script': scripts,
        'data_files': data_files,
    }
    return render(request, 'run_script.html', context)

# TODO: Design form to pick a file and algorithm to run
# TODO: Write algorithm calling function
