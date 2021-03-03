from django.http import HttpResponse

def homePageView(request):
    return HttpResponse('Funciona la API del D1!')
