from django import forms
from django.contrib.auth.forms import UserCreationForm  # import DJango's form to register
from django.contrib.auth.models import User     # import django's model for the user
from core.models import File, FileFormat    # created file form
from django.forms import ModelForm, Select


# create a new form
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


class FileFormatChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('name', 'uploaded_file', 'format')
