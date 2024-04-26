from django.shortcuts import render, redirect
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}! You are logged in!')
            return redirect('login')
        else:
            for error in form.errors:
                if 'password' in error.lower():
                    messages.error(request,
                                   f'Password error: Please use a combination of uppercase,'
                                   f' lowercase letters, numbers, and symbols.\n Ensure that passwords match.')
                    break
                if 'username' in error.lower():
                    messages.error(request,
                                   f'Username already taken. Please select new username.')
                    break
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})
