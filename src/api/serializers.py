from .models import Funcionario, Perfil, Curriculo
from django.db.models.query import QuerySet
from rest_framework import serializers
from django.conf import settings


class FuncionarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Funcionario
        fields = ['id', 'nome', 'sobrenome', 'created_at', 'updated_at',
        'funcao', 'email', 'ano_nascimento']

class PerfilSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Perfil
        fields = ['id', 'nome', 'sobrenome', 'created_at', 'updated_at',
        'email', 'github', 'avatar', 'celular', 'perfil', 'avatar_path']

    avatar = serializers.SerializerMethodField()
    avatar_path = serializers.SerializerMethodField()

    def get_avatar(self, instance):
        if hasattr(instance, 'avatar'):
            if not instance.avatar:
                instance.avatar = 'default.png'
            return str(instance.avatar)

        avatar = str(instance.get('avatar'))
        return avatar if avatar != "" else 'default.png'

    def get_avatar_path(self, instance):
        if hasattr(instance, 'avatar'):
            if not instance.avatar:
                instance.avatar = 'default.png'
            return settings.MEDIA_URL + str(instance.avatar)

        if str(instance.get('avatar')) == "":
            instance['avatar'] = 'default.png'
        return settings.MEDIA_URL + str(instance.get('avatar'))
        

    

class CurriculoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Curriculo
        fields = ['id', 'empresa', 'data_inicio', 'data_saida', 'empresa_atual',
        'resumo', 'created_at', 'updated_at']