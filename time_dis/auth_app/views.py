from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import Users
from .forms import RegisterForm, LoginForm, LoginChangeForm, EmailChangeForm, UserInfoChangeForm


def register(request):
    if request.user.is_authenticated:
        return redirect('main')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'Ошибка регистрации!')
    else:
        form = RegisterForm()
    return render(request, 'auth_app/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('main')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'Неверный логин/пароль')
    else:
        form = LoginForm()
    return render(request, 'auth_app/login.html', {'form': form})


def pass_recovery(request):
    if request.user.is_authenticated:
        return redirect('main')
    if request.GET.get('user_hash'):
        user = Users.objects.get(password=request.GET.get('user_hash').replace(' ', '+'))
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = SetPasswordForm(user)
        return render(request, 'auth_app/pass_recovery.html', {'form': form})
    if request.method == 'POST':
        if 'email' in request.POST:
            user_mail = request.POST.get('email')
            user_hash = Users.objects.filter(email=user_mail).values_list('password', flat=True).first()
            if user_hash:
                url = request.build_absolute_uri(f'{request.path}?user_hash={user_hash}')
                mes = f'Для восстановления пароля перейдите по ссылке:\n{url}'
                mail = send_mail('Восстановление пароля', mes,
                                 f'TimeDis <{settings.EMAIL_HOST_USER}>', [user_mail], fail_silently=False)
                if mail:
                    messages.success(
                        request,
                        'Дальнейшие инструкции для восстановления пароля отправлены на вашу почту'
                    )
                else:
                    messages.error(request, 'Повторите попытку позже')
                return redirect('pass_recovery')
            else:
                messages.error(request, 'Введён неверный адрес эллектронной почты.')
                return redirect('pass_recovery')
    return render(request, 'auth_app/pass_recovery.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def user_settings(request):
    if request.method == 'POST':
        if 'login_success' in request.POST:
            form = LoginChangeForm(request.POST, instance=request.user)
        elif 'email_success' in request.POST:
            form = EmailChangeForm(request.POST, instance=request.user)
        elif 'info_success' in request.POST:
            form = UserInfoChangeForm(request.POST, instance=request.user)
        else:
            form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_settings')
    forms = {'password_form': PasswordChangeForm(user=request.user),
             'login_from': LoginChangeForm(),
             'email_form': EmailChangeForm(),
             'user_info_form': UserInfoChangeForm(instance=request.user)}
    return render(request, 'auth_app/user_settings.html', forms)
