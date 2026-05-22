# ============================================================================
# ROUTER: /api/subscriptions  -- TODO live coding
# ============================================================================
# Plantilla: ver interfaces/routers/movie_router.py
#
# Endpoints sugeridos:
#   POST   /api/subscriptions               -> contratar
#   GET    /api/subscriptions               -> listar
#   GET    /api/subscriptions/{id}
#   PUT    /api/subscriptions/{id}/renovar
#   PUT    /api/subscriptions/{id}/cancelar
# ============================================================================

from fastapi import APIRouter


router = APIRouter(prefix="/api/subscriptions", tags=["subscriptions"])

# TODO
