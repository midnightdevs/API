# Create your views here.
from django.http import JsonResponse
from .models import Pessoa
from .serializers import PessoaSerializer

def hello_world(request):
    return JsonResponse('Hello World', safe=False)

def hello_name(request, name='Marcel'):
    return JsonResponse({"nome": f'Hello {name}'})

def pessoa_info(request):
    
    pessoa = Pessoa()
    pessoa.nome = 'Marcel'
    pessoa.sobrenome = 'Fox'
    pessoa.save()

    qs_pessoa = Pessoa.objects.all().values()
    pessoa_lista = PessoaSerializer(qs_pessoa, many=True)

    if request.method == 'GET':
        return JsonResponse({"Pessoas": pessoa_lista.data})
    
    return JsonResponse({"message": 'Hello'})
