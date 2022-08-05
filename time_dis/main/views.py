from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def main(request):
    return render(request, 'main/main_menu.html')
