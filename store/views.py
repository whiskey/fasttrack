from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from store.models import MobileApp


def home(request):
    apps = MobileApp.objects.all()
    filtered = []

    for app in apps:
        permission = 'store.can_access_{}'.format(app.normalized_name)
        if request.user.has_perm(permission):
            filtered.append(app)

    context = {
        'app_list': filtered
    }
    return render(request, 'store/home.html', context)


@login_required(login_url='/login/')
def detail(request, app_id):
    app = get_object_or_404(MobileApp, pk=app_id)
    context = {
        'app': app
    }
    return render(request, 'store/detail.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('store:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
