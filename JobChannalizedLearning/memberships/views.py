from django.shortcuts import render,redirect
from .forms import Membership_form
from django.urls import reverse
# Create your views here.


def membership_view(request):
    context = {}
    if request.POST:
        membership_form = Membership_form(request.POST)
        if membership_form.is_valid():
            membership_form.user = request.user.username
            membership_form.save()
            return redirect(reverse('http://127.0.0.1:8000/membership/'))
    context['membership_form'] = Membership_form()
    return render(request,'membership/membership_registration.html',context)
