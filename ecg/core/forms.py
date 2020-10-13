from django import forms
from django.contrib.auth.forms import UserCreationForm  # import Django's form to register
from django.contrib.auth.models import User     # import django's model for the user
from core.models import File, FileFormat, Script, Execution    # created file form


# Form to register as a new user
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")   # form fields

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)  # instantiate user from form but do not save
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('name', 'uploaded_file', 'format')


class FileSelectForm(forms.Form):
    file_select = forms.ModelChoiceField(label="File", queryset=File.objects.all())     # all user files

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)    # get the current user
        super(FileSelectForm, self).__init__(*args, **kwargs)   # expands args into keyword arguments again
        self.fields['file_select'].queryset = File.objects.filter(user=self.user)   # filter files for one user


class ScriptSelectForm(forms.Form):
    script_select = forms.ModelChoiceField(label="Script", queryset=Script.objects.all())  # all scripts to process

    def compatible_scripts(self, input_file_type, *args, **kwargs):
        super(ScriptSelectForm, self).__init__()   # expands args into keyword arguments again
        supported_scripts = Script.objects.filter(supported_input=input_file_type)  # get all matching scripts
        self.fields['script_select'].queryset = supported_scripts   # populate the form with only supported scripts
