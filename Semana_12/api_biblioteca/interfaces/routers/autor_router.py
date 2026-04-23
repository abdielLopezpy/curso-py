# ============================================================================
# ROUTER: /api/autores
# ============================================================================
# Completar siguiendo el patron de interfaces/routers/libro_router.py.
# ============================================================================

from fastapi import APIRouter


router = APIRouter(prefix="/api/autores", tags=["autores"])


# TODO: definir los endpoints GET, POST, PUT, DELETE siguiendo el patron
#       de libro_router.py, usando:
#         - application.schemas.autor_schema
#         - application.use_cases.autor.*
#         - interfaces.dependencies.get_autor_repository
