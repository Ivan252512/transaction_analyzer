from django.http import HttpResponse

def index(request):
    return HttpResponse("¡Hola, esta es mi nueva app!")