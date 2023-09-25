from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import NewUserForm


def reg_user(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Your account has been created you can now log in')
            return redirect('login')
        messages.error(request, 'Unsuccessful registration. Invalid information.')
    form = NewUserForm()   


    return render(request,'users/register.html',context={'form':form})

@login_required
def profile(request):
    return render(request,'users/profile.html')