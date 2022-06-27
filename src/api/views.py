# Create your views here.
from django.http import JsonResponse

def hello_world(request):
    return JsonResponse('Hello World', safe=False)

def hello_name(request, name='Marcel'):
    return JsonResponse({"nome": f'Hello {name}'})