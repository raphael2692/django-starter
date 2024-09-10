# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import password_validators_help_texts


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        
class UserEditFormWithPassword(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        help_text='<ul>' + ''.join(f'<li>{text}</li>' for text in password_validators_help_texts()) + '</ul>')
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        label='Conferma password',  
        help_text='Inserisci la stessa password inserita sopra, come verifica.'
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password != password_confirm:
            self.add_error('password_confirm', 'Passwords do not match.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user