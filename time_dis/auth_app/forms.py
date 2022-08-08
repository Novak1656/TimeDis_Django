from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Users


def set_attrs(placeholder=None, tag_type=None):
    attrs = {'class': 'form-control'}
    if placeholder:
        attrs['placeholder'] = placeholder
    elif tag_type:
        attrs['type'] = tag_type
    return attrs


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs=set_attrs('Введите логин...')))
    email = forms.EmailField(label='E-mail',
                             widget=forms.EmailInput(attrs=set_attrs('Введите адрес электронной почты...')))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs=set_attrs('Введите ваше имя...')))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs=set_attrs('Введите вашу фамилию...')))
    date_of_birth = forms.DateField(label='Дата рождения',
                                    widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs=set_attrs('Придумайте пароль...')))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs=set_attrs('Введите пароль ещё раз...')))

    class Meta:
        model = Users
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'password1', 'password2',)


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs=set_attrs('Введите логин...')))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs=set_attrs('Введите пароль...')))


class LoginChangeForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('username',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'})
        }


class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }


class UserInfoChangeForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'date_of_birth',)
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }
