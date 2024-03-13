from django.db import models
from django.contrib.auth.models import User


class HistorialAdmin(models.Model):
    h_id_user = models.AutoField(primary_key=True)
    id_user = models.PositiveBigIntegerField()
    username = models.CharField(max_length=255, null=True)
    email = models.EmailField()  
    h_user_proc = models.ForeignKey(User, on_delete=models.RESTRICT)
    h_fch_creacion = models.DateTimeField(auto_now_add=True)
    h_tipo_proc = models.CharField(max_length=1, null=True)

    class Meta:
        verbose_name = 'H_Usuario'
        verbose_name_plural = 'H_Usuarios'

    def __str__(self) -> str:
        return f"ID: {self.id_user} - USERNAME: {self.username} - EMAIL: {self.email} - FECH. CREACION: {self.h_fch_creacion} - USER_PROC: {self.h_user_proc}"


