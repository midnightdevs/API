# Create your views here.
import json
from django.http import JsonResponse
from .models import Pessoa, Funcionario
from .serializers import PessoaSerializer, FuncionarioSerializer

def hello_world(request):
    return JsonResponse('Hello World', safe=False)

def hello_name(request, name='Marcel'):
    return JsonResponse({"nome": f'Hello {name}'})

def pessoa_info(request):
       
    pessoa = Pessoa()
    pessoa.nome = 'Marcel'
    pessoa.sobrenome = 'Fox'

    # Como trazer todos os objetos:
    # qs_pessoa = Pessoa.objects.all().values()

    qtd_objetos = Pessoa.objects.filter(nome='Marcel').count()

    if qtd_objetos > 1:
        marcel_existe = Pessoa.objects.filter(nome='Marcel').all()
        pessoa_serializer = PessoaSerializer(marcel_existe, many=True)
    else:
        marcel_existe = Pessoa.objects.filter(nome='Marcel').first()
        pessoa_serializer = PessoaSerializer(marcel_existe, many=False)

    if marcel_existe:
        print(pessoa_serializer.data)
    else:
        pessoa.save()

    if request.method == 'POST':
        data = json.loads(request.body)

        nome = data.get('nome')
        sobrenome = data.get('sobrenome')

        return JsonResponse({'mensagem': f'O nome é {nome}, e o sobrenome é {sobrenome}'})

    if request.method == 'GET':
        return JsonResponse({"mensagem": pessoa_serializer.data})
    
    return JsonResponse({"message": 'funcionario existe'})

def funcionario_info(request):
    """View de funcionário."""

    if request.method == 'GET':
        qs_funcionario = Funcionario.objects.all().values()
        serializer = FuncionarioSerializer(qs_funcionario, many=True)
        return JsonResponse({"funcionarios": serializer.data})

    if request.method == 'POST':
        data = json.loads(request.body)

        funcionario = Funcionario()
        funcionario.ano_nascimento = data.get('ano_nascimento')
        funcionario.nome = data.get('nome')
        funcionario.sobrenome = data.get('sobrenome')
        funcionario.email = data.get('email')
        funcionario.funcao = data.get('funcao')

        existe_funcionario = Funcionario.objects.filter(email=funcionario.email).count()
        if existe_funcionario:
            return JsonResponse({"mensagem": "O usuário já existe"})
        
        cadastro = funcionario.save()
        serializer = FuncionarioSerializer(cadastro, many=False)
        return JsonResponse(serializer.data)

    return JsonResponse({"mensagem": "Método inválido"})

