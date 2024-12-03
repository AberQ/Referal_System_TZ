from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import PhoneAuthForm

def phone_login_view(request):
    if request.method == "POST":
        form = PhoneAuthForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            return redirect("home")  # Редирект на главную страницу
    else:
        form = PhoneAuthForm()
    return render(request, "login.html", {"form": form})
