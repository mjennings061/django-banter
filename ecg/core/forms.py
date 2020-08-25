from django import forms
from django.contrib.auth.forms import UserCreationForm  # import DJango's form to register
from django.contrib.auth.models import User     # import django's model for the user


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
