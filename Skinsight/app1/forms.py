from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model 

class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter email-username", "class": "form-control"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Enter email-address", "class": "form-control"}))
    age = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={"placeholder": "Enter age", "class": "form-control"}))
    gender = forms.CharField(max_length=1, required=False, widget=forms.TextInput(attrs={"placeholder": "Enter gender (M/F)", "class": "form-control"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Enter password", "class": "form-control"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"placeholder": "Confirm password", "class": "form-control"}))
    
    class Meta:
        model = get_user_model()
        fields = ["username","email", "age", "gender","password1", "password2"]

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Select an image')