# ============================================================================
# ROUTER: /api/catalogs  -- TODO live coding
# ============================================================================
# Plantilla: ver interfaces/routers/movie_router.py
#
# Endpoints sugeridos:
#   GET    /api/catalogs
#   GET    /api/catalogs/{id}
#   POST   /api/catalogs
#   PUT    /api/catalogs/{id}
#   DELETE /api/catalogs/{id}
#   POST   /api/catalogs/{id}/movies/{movie_id}    -> agregar M:N
#   DELETE /api/catalogs/{id}/movies/{movie_id}    -> quitar M:N
# ============================================================================

from fastapi import APIRouter


router = APIRouter(prefix="/api/catalogs", tags=["catalogs"])

# TODO
