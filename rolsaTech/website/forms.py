from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

class loginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class createUserForm(UserCreationForm):
    full_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Password Check")

    class Meta:
        model = User
        fields = ['full_name', 'email', 'username', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data['full_name']
        if commit:
            user.save()
        return user

class bookingForm(forms.Form):
    type = forms.ChoiceField(choices=[('ev-charger', 'EV Charger Installation'), ('solar', 'Solar Panel Installation'), ('smart-home', 'Smart Home Energy')], widget=forms.Select(attrs={'class': 'form-control'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    notes = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)

class userSettingsForm(forms.ModelForm):
    full_name = forms.CharField(max_length=150, label="Full Name")
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="New Password (leave blank to keep current)")
    
    class Meta:
        model = User
        fields = ['full_name', 'email', 'username']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set full_name to the user's current first_name and last_name combined
        if self.instance.pk:
            self.fields['full_name'].initial = f"{self.instance.first_name} {self.instance.last_name}".strip()
        self.fields['full_name'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Split full_name into first_name and last_name
        full_name = self.cleaned_data.get('full_name', '')
        name_parts = full_name.split(' ', 1)
        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Update password if provided
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
        return user

