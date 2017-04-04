from django.http.response import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the fasttrack store.")