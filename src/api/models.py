from django.db import models

# Create your models here.
class ModeloBase(models.Model):
    """Classe base da modelo, que as demais classes herdarão."""
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Pessoa(ModeloBase):
    """Classe pessoa."""
    nome = models.CharField(max_length=30)
    sobrenome = models.CharField(max_length=30)