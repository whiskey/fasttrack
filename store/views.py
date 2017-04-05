from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render

from store.models import MobileApp


def index(request):
    apps = MobileApp.objects.all
    context = {
        'app_list': apps
    }
    return render(request, 'store/index.html', context)


def detail(request, app_id):
    app = get_object_or_404(MobileApp, pk=app_id)
    return HttpResponse(app)
