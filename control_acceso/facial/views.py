import base64
import numpy as np
import cv2
import face_recognition
from io import BytesIO

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.utils import timezone

from usuarios.models import Usuario, Zona
from usuarios.decorators import rol_requerido
from registro_accesos.models import RegistroAcceso
from .models import EncodingFacial


@login_required
@rol_requerido('admin', 'supervisor')
def registrar_rostro(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)

    if request.method == 'POST':
        imagen_data = request.POST.get('imagen')
        if not imagen_data:
            messages.error(request, 'No se recibió imagen.')
            return redirect('detalle_usuario', pk=usuario_id)

        try:
            header, data = imagen_data.split(',', 1)
            imagen_bytes = base64.b64decode(data)
            imagen_np = np.frombuffer(imagen_bytes, dtype=np.uint8)
            imagen = cv2.imdecode(imagen_np, cv2.IMREAD_COLOR)
            rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

            encodings = face_recognition.face_encodings(rgb)
            if not encodings:
                messages.error(request, 'No se detectó ningún rostro en la imagen.')
                return redirect('detalle_usuario', pk=usuario_id)

            encoding_facial = EncodingFacial(usuario=usuario)
            encoding_facial.set_encoding(encodings[0])
            encoding_facial.foto.save(
                f'{usuario.cedula}_{timezone.now():%Y%m%d%H%M%S}.jpg',
                ContentFile(imagen_bytes),
            )
            encoding_facial.save()
            messages.success(request, f'Rostro registrado para {usuario.nombre_completo}.')
        except Exception as e:
            messages.error(request, f'Error al procesar la imagen: {e}')

        return redirect('detalle_usuario', pk=usuario_id)

    return render(request, 'facial/registrar_rostro.html', {'usuario': usuario})


@login_required
@rol_requerido('admin', 'supervisor', 'vigilante')
def punto_acceso(request):
    zonas = Zona.objects.filter(activa=True)
    return render(request, 'facial/punto_acceso.html', {'zonas': zonas})


@csrf_exempt
@login_required
def verificar_rostro(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    imagen_data = request.POST.get('imagen')
    zona_id = request.POST.get('zona_id')
    tipo = request.POST.get('tipo', 'entrada')

    if not imagen_data or not zona_id:
        return JsonResponse({'error': 'Faltan datos'}, status=400)

    try:
        zona = Zona.objects.get(pk=zona_id, activa=True)
    except Zona.DoesNotExist:
        return JsonResponse({'error': 'Zona no válida'}, status=400)

    try:
        header, data = imagen_data.split(',', 1)
        imagen_bytes = base64.b64decode(data)
        imagen_np = np.frombuffer(imagen_bytes, dtype=np.uint8)
        imagen = cv2.imdecode(imagen_np, cv2.IMREAD_COLOR)
        rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

        face_encodings = face_recognition.face_encodings(rgb)
        if not face_encodings:
            registro = RegistroAcceso.objects.create(
                zona=zona, tipo=tipo, autorizado=False,
                metodo='facial', observacion='No se detectó rostro',
            )
            registro.foto_captura.save(f'captura_{timezone.now():%Y%m%d%H%M%S}.jpg', ContentFile(imagen_bytes))
            return JsonResponse({
                'autorizado': False,
                'mensaje': 'No se detectó ningún rostro.',
            })

        encoding_captura = face_encodings[0]

        todos_encodings = EncodingFacial.objects.select_related('usuario').all()
        for enc in todos_encodings:
            encoding_guardado = enc.get_encoding()
            distancia = face_recognition.face_distance([encoding_guardado], encoding_captura)[0]
            coincide = distancia < 0.5

            if coincide:
                usuario = enc.usuario
                tiene_permiso = usuario.activo and usuario.zonas_permitidas.filter(pk=zona.pk).exists()

                registro = RegistroAcceso.objects.create(
                    usuario=usuario, zona=zona, tipo=tipo,
                    autorizado=tiene_permiso, metodo='facial',
                    confianza=round(1 - distancia, 4),
                    observacion='' if tiene_permiso else 'Sin permiso para esta zona',
                )
                registro.foto_captura.save(f'captura_{timezone.now():%Y%m%d%H%M%S}.jpg', ContentFile(imagen_bytes))

                return JsonResponse({
                    'autorizado': tiene_permiso,
                    'usuario': usuario.nombre_completo,
                    'cedula': usuario.cedula,
                    'confianza': round((1 - distancia) * 100, 1),
                    'mensaje': 'Acceso permitido' if tiene_permiso else 'Sin permiso para esta zona',
                })

        registro = RegistroAcceso.objects.create(
            zona=zona, tipo=tipo, autorizado=False,
            metodo='facial', observacion='Rostro no reconocido',
        )
        registro.foto_captura.save(f'captura_{timezone.now():%Y%m%d%H%M%S}.jpg', ContentFile(imagen_bytes))
        return JsonResponse({
            'autorizado': False,
            'mensaje': 'Rostro no reconocido en el sistema.',
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
