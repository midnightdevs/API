# Create your views here.
import json, os
from os.path import exists
from django.http import JsonResponse
from django.conf import settings
from .models import Funcionario, Perfil, Curriculo
from rest_framework.decorators import api_view

from .serializers import FuncionarioSerializer, PerfilSerializer, CurriculoSerializer

def health(request):
    return JsonResponse({"mensagem": "ok"}, safe=False)

def funcionario_info(request):
    """View de funcionário."""
    query_params = request.GET

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
        
        funcionario.save()
        serializer = FuncionarioSerializer(funcionario, many=False)
        return JsonResponse({"objeto": serializer.data})

    if request.method == 'DELETE':
        existe_email = query_params.get('email')

        if existe_email:
            existe_funcionario = Funcionario.objects.filter(email=existe_email).first()

            if existe_funcionario:
                serializer = FuncionarioSerializer(existe_funcionario, many=False)
                existe_funcionario.delete()
                return JsonResponse({"objeto": serializer.data})

        return JsonResponse({"mensagem": 'Usuário não encontrado'})

    if request.method == 'PUT':
        data = json.loads(request.body)
        email = query_params.get('email')

        email_existe = Funcionario.objects.filter(email=data.get('email')).count()
        if email_existe:
            return JsonResponse({'mensagem': 'Usuario já existe'})

        funcionario = Funcionario.objects.filter(email=email).first()
        if funcionario:
            funcionario.ano_nascimento = data.get('ano_nascimento')
            funcionario.nome = data.get('nome')
            funcionario.sobrenome = data.get('sobrenome')
            funcionario.email = data.get('email')
            funcionario.funcao = data.get('funcao')
            funcionario.save()
            serializer = FuncionarioSerializer(funcionario, many=False)
            return JsonResponse(serializer.data) 

        return JsonResponse({'mensagem': 'Usuario não encontrado'})

    return JsonResponse({"mensagem": "Método inválido"})


def perfil_info(request):
    """View da model Perfil."""

    query_params = request.GET

    if request.method == 'GET':
        if query_params.get('email'):
            perfil = Perfil.objects.filter(email=query_params.get('email')).first()
            serializer = PerfilSerializer(perfil, many=False)
            return JsonResponse(serializer.data, safe=False)
        else:
            lista_perfis = Perfil.objects.all().values()
            serializer = PerfilSerializer(lista_perfis, many=True)
            return JsonResponse(serializer.data, safe=False)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        
        perfil = Perfil()
        perfil.nome = data.get('nome')
        perfil.sobrenome = data.get('sobrenome')
        perfil.avatar = data.get('avatar')
        perfil.email = data.get('email')
        perfil.perfil = data.get('perfil')
        perfil.github = data.get('github')
        perfil.celular = data.get('celular')

        existe_perfil = Perfil.objects.filter(email=perfil.email).count()
        if existe_perfil:
            return JsonResponse({'mensagem': 'O usuário já existe'})

        perfil.save()
        serializer = PerfilSerializer(perfil, many=False)
        return JsonResponse({'objeto': serializer.data})
        
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        existe_perfil = Perfil.objects.filter(email=query_params.get('email')).count()

        if existe_perfil:
            perfil = Perfil.objects.filter(email=query_params.get('email')).first()
            perfil.nome = data.get('nome')
            perfil.sobrenome = data.get('sobrenome')
            perfil.email = data.get('email')
            perfil.perfil = data.get('perfil')
            perfil.github = data.get('github')
            perfil.celular = data.get('celular')

            perfil.save()
            serializer = PerfilSerializer(perfil, many=False)
            return JsonResponse({'objeto': serializer.data})

        return JsonResponse({'mensagem': 'Email não existe'})


    if request.method == 'DELETE':
        existe_email = query_params.get('email')

        perfil = Perfil.objects.filter(email=existe_email).first()

        if perfil:
            perfil.delete()
            return JsonResponse({'mensagem': 'objeto deletado'})

        return JsonResponse({'mensagem': 'objeto não encontrado'})

@api_view(['POST', 'DELETE'])
def perfil_avatar(request):
    query_params = request.GET

    if request.method == 'POST':
        perfil = Perfil.objects.filter(email=query_params.get('email')).first()
        
        if not perfil:
            return JsonResponse({'mensagem': 'Perfil não encontrado'})

        serializer = PerfilSerializer(perfil, many=False)
        avatar_path = serializer.data.get('avatar')

        if avatar_path and avatar_path != 'default.png':
            os.remove(settings.MEDIA_ROOT + '/' + str(avatar_path))

        perfil.avatar = request.data['file']
        perfil.save()

        serializer = PerfilSerializer(perfil, many=False)
        return JsonResponse({'mensagem': serializer.data})

    if request.method == 'DELETE':
        perfil = Perfil.objects.filter(email=query_params.get('email')).first()
        
        if not perfil:
            return JsonResponse({'mensagem': 'Perfil não encontrado'})
        
        serializer = PerfilSerializer(perfil, many=False)
        avatar_path = serializer.data.get('avatar')

        if avatar_path and avatar_path != 'default.png':
            os.remove(settings.MEDIA_ROOT + '/' + str(avatar_path))

        perfil.avatar = 'default.png'
        perfil.save()

        return JsonResponse({'mensagem': 'Imagem deletada'})
    
    return JsonResponse({'mensagem': 'método não suportado'})


def curriculo_info(request):
    """View da model Perfil."""

    query_params = request.GET

    if request.method == 'GET':
        lista_curriculo = Curriculo.objects.all().values()
        serializer = CurriculoSerializer(lista_curriculo, many=True)
        return JsonResponse({'curriculo': serializer.data})

    if request.method == 'POST':
        data = json.loads(request.body)
        existe_empresa = Curriculo.objects.filter(empresa=data.get('empresa')).count()

        if existe_empresa:
            return JsonResponse({'mensagem': 'Empresa já existe'})

        curriculo = Curriculo()
        curriculo.empresa = data.get('empresa')
        curriculo.data_inicio = data.get('data_inicio')
        curriculo.data_saida = data.get('data_saida')
        curriculo.empresa_atual = data.get('empresa_atual')
        curriculo.resumo = data.get('resumo')
        curriculo.save()

        serializer = CurriculoSerializer(curriculo, many=False)
        return JsonResponse({"objeto": serializer.data})

    if request.method == 'PUT':
        data = json.loads(request.body)
        existe_empresa = Curriculo.objects.filter(empresa=data.get('empresa')).count()
        empresa_diferente = data.get('empresa') != query_params.get('empresa')

        if existe_empresa and empresa_diferente:
            return JsonResponse({'mensagem': 'Empresa já existe'})

        curriculo = Curriculo.objects.filter(empresa=query_params.get('empresa')).first()
        curriculo.empresa = data.get('empresa')
        curriculo.data_inicio = data.get('data_inicio')
        curriculo.data_fim = data.get('data_fim')
        curriculo.empresa_atual = data.get('empresa_atual')
        curriculo.resumo = data.get('resumo')
        curriculo.save()

        serializer = CurriculoSerializer(curriculo, many=False)
        return JsonResponse({"objeto": serializer.data})
    
    if request.method == 'DELETE':
        curriculo = Curriculo.objects.filter(empresa=query_params.get('empresa')).first()

        if curriculo:
            curriculo.delete()
            return JsonResponse({'mensagem': 'objeto deletado'})

        return JsonResponse({'mensagem': 'objeto não encontrado'})