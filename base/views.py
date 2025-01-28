from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

def auth_view(request):
    action = request.GET.get('action', 'login')  # Default to login
    is_login = action == 'login'

    if request.method == 'POST':
        if is_login:
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('home')
        else:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm() if is_login else UserCreationForm()

    context = {
        'form': form,
        'is_login': is_login,
        'title': 'Login Here' if is_login else 'Sign Up',
    }
    return render(request, 'base/auth.html', context)

def logout_view(request):
    logout(request)
    return redirect('auth')

def home_view(request):
    return render(request, 'base/home.html')