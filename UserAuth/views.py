from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import SignUpForm


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                form.add_error('confirm_password', 'Passwords do not match.')
                return render(request, 'Auth/sign_up.html', {'form': form})

            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)


            return redirect('UserAuth:sign_in')
    else:
        form = SignUpForm()
    return render(request, 'Auth/sign_up.html', {'form': form})


def sign_in(request):
    return render(request,'Auth/sign_in.html')