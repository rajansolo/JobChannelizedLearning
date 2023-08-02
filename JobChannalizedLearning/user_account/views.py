from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from user_account.forms import RegistrationForm, UserAuthenticationForm
from django.contrib.auth.decorators import login_required

@login_required
def registration_successful_view(request):
    context = {}
    return render(request, 'user_account/registration_successful.html', context)


def login_first(request):
    context = {}
    return render(request, 'user_account/login_first.html', context)


def you_have_to_logout_first(request):
    context = {}
    return render(request, 'user_account/you_have_to_logout_first.html', context)


def user_registration_view(request):
    context = {}
    user_choices = [
        ('STUDENT', 'Student'),
        ('MENTOR', 'Mentor'),
    ]
    context['user_choices'] = user_choices
    if request.user.is_authenticated:
        return redirect('user_account:you_have_to_logout_first')
    if request.POST:
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()  # creates a new user in the database
            print(registration_form)
            return redirect('user_account:registration_successful')
        else:
            context['registration_form'] = registration_form
    else:
        context['registration_form'] = RegistrationForm()
    return render(request, 'user_account/registration_page.html', context)


def user_login_view(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('website_content:home')
    if request.POST:
        login_form = UserAuthenticationForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user:
                login(request, authenticated_user)
                return redirect('website_content:home')
        print(login_form.errors)
    else:
        login_form = UserAuthenticationForm()
    context['login_form'] = login_form
    return render(request, 'user_account/login_page.html', context)


def user_logout_view(request):
    logout(request)
    return redirect('user_account:login')
