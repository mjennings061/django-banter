from django import forms
from django.contrib.auth.forms import UserCreationForm  # import Django's form to register
from django.contrib.auth.models import User     # import django's model for the user
from .models import File, Script, Execution, Algorithm    # created file form


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


class ExecutionSelectForm(forms.ModelForm):
    data_input = forms.ModelChoiceField(queryset=File.objects.all(), required=True)
    script = forms.ModelChoiceField(queryset=Script.objects.all(), required=True)

    class Meta:
        model = Execution
        fields = ('data_input', 'script')   # form fields

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # get the current user
        super(ExecutionSelectForm, self).__init__(*args, **kwargs)  # expands args into keyword arguments again
        self.fields['data_input'].queryset = File.objects.filter(user=self.user)  # filter files for one user


class AlgorithmForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    description = forms.CharField(widget=forms.Textarea)
    data_input = forms.ModelChoiceField(queryset=File.objects.all())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # get the current user
        super(AlgorithmForm, self).__init__(*args, **kwargs)
        self.fields['data_input'].queryset = File.objects.filter(user=self.user)  # filter files for one user
        for i in range(0, 4):
            self.fields[f'script[{i}]'] = forms.ModelChoiceField(queryset=Script.objects.all(),
                                                                 label=f'Script to run: No.{i+1}',
                                                                 required=False,)
