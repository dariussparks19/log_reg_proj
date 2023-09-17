from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt
# Create your views here.
def index(request):
    return render(request, 'index.html')

def create_user(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        print(request.POST)
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )
        # set session id
        request.session['uid'] = user.id
    return redirect('/success')

def login_user(request):
    print("logging in user")
    print(request.POST)
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email = request.POST['login_email'])
        request.session['uid'] = user.id
        return redirect('/success')


def dashboard(request):
    if 'uid' not in request.session:
        return redirect('/')
    user_id = request.session['uid']
    context = {
        "user" : User.objects.get(id = user_id)
    }
    return render(request, 'dashboard.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')