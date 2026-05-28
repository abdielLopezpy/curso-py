from django.db import models
from django.conf import settings


class RegistroAcceso(models.Model):
    class TipoAcceso(models.TextChoices):
        ENTRADA = 'entrada', 'Entrada'
        SALIDA = 'salida', 'Salida'

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accesos',
    )
    zona = models.ForeignKey(
        'usuarios.Zona',
        on_delete=models.SET_NULL,
        null=True,
        related_name='accesos',
    )
    tipo = models.CharField(max_length=10, choices=TipoAcceso.choices, default=TipoAcceso.ENTRADA)
    autorizado = models.BooleanField(default=False)
    metodo = models.CharField(max_length=30, default='facial')
    confianza = models.FloatField(null=True, blank=True)
    foto_captura = models.ImageField(upload_to='capturas/%Y/%m/%d/', blank=True, null=True)
    observacion = models.TextField(blank=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_hora']
        verbose_name = 'Registro de Acceso'
        verbose_name_plural = 'Registros de Acceso'

    def __str__(self):
        estado = "Permitido" if self.autorizado else "Denegado"
        nombre = self.usuario.nombre_completo if self.usuario else "Desconocido"
        return f"{nombre} - {self.zona} - {estado} ({self.fecha_hora:%d/%m/%Y %H:%M})"
