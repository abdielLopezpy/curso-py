# ============================================================================
# ROUTER: /api/prestamos
# ============================================================================
# Completar siguiendo el patron de interfaces/routers/libro_router.py.
#
# Endpoints sugeridos:
#   GET    /api/prestamos                -> listar
#   GET    /api/prestamos/{id}           -> obtener
#   POST   /api/prestamos                -> crear (valida disponibilidad)
#   PUT    /api/prestamos/{id}/devolver  -> registrar devolucion
#   DELETE /api/prestamos/{id}           -> eliminar
# ============================================================================

from fastapi import APIRouter


router = APIRouter(prefix="/api/prestamos", tags=["prestamos"])


# TODO: definir los endpoints.
