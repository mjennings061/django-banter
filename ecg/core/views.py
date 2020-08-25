from django.shortcuts import render, redirect
from .forms import NewUserForm, UploadFileForm  # import our own custom form
from django.contrib import messages     # alert the user
from django.contrib.auth import login, logout as django_logout, authenticate     # user handling (register)
from django.contrib.auth.forms import AuthenticationForm
from core.models import File
from django.contrib.auth.models import User     # import django's model for the user


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
    form = UploadFileForm()
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = File(
                name=form.cleaned_data["name"],
                uploaded_file=form.files["uploaded_file"],
                user=user,
            )
            file.save()
            messages.info(request, f"File uploaded")
        else:
            messages.error(request, f"File not uploaded")

    context = {
        'form': form,
    }
    return render(request, 'file_upload.html', context)
