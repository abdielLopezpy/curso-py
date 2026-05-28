import pickle
from django.db import models
from django.conf import settings


class EncodingFacial(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='encodings_faciales',
    )
    foto = models.ImageField(upload_to='fotos_faciales/')
    encoding = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Encoding Facial'
        verbose_name_plural = 'Encodings Faciales'

    def __str__(self):
        return f"Encoding de {self.usuario.nombre_completo} ({self.created_at:%d/%m/%Y})"

    def set_encoding(self, encoding_array):
        self.encoding = pickle.dumps(encoding_array)

    def get_encoding(self):
        return pickle.loads(self.encoding)
