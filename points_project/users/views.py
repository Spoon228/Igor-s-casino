from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AddPointsForm, RemovePointsForm
from .models import UserPoints

# Widok rejestracji
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatyczne logowanie po rejestracji
            return redirect('/')
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

# Widok punktów użytkownika
@login_required
def user_points(request):
    user_points, created = UserPoints.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        add_form = AddPointsForm(request.POST)
        remove_form = RemovePointsForm(request.POST)
        
        if add_form.is_valid():
            user_points.points += add_form.cleaned_data['points']
            user_points.save()
            return redirect('user_points')
        
        if remove_form.is_valid():
            user_points.points -= remove_form.cleaned_data['points']
            user_points.save()
            return redirect('user_points')
    else:
        add_form = AddPointsForm()
        remove_form = RemovePointsForm()
    
    return render(request, 'users/user_points.html', {
        'user_points': user_points,
        'add_form': add_form,
        'remove_form': remove_form,
    })

def homepage(request):
    return render(request, 'users/homepage.html')

from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    return redirect('homepage')


from django.contrib.auth.models import User

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('homepage')

    return render(request, 'users/delete_account.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.decorators import method_decorator

@csrf_exempt
@login_required
def modify_points(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        points = data.get('points', 0)
        user_points, created = UserPoints.objects.get_or_create(user=request.user)

        if action == 'add':
            user_points.points += points
        elif action == 'remove' and user_points.points >= points:
            user_points.points -= points
        user_points.save()

        return JsonResponse({'status': 'success', 'points': user_points.points})
    return JsonResponse({'status': 'error'}, status=400)
