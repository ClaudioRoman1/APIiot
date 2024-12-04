from django.db import models
class RestBase(models.Model):
    iUsuarioCreacionID =  models.IntegerField(null=True)
    dtmCreacion=models.DateTimeField(null=True)
    iUsuarioUltimaModificacionID= models.IntegerField(null=True)
    dtmUltimaModificacion=models.DateTimeField(null=True)
    bActivo= models.BooleanField(null=False, default=True)
    iUsuarioAnulacionID= models.IntegerField(null=True)
    dtmAnulacion=models.DateTimeField(null=True)
    class Meta:
        abstract = True
        