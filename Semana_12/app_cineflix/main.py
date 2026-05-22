# ============================================================================
# Cineflix - Punto de entrada (FastAPI + Clean Architecture)
# ============================================================================
# Responsabilidad:
#   - Crear la instancia FastAPI.
#   - Inicializar la BD (crear tablas + cargar seed) al arrancar.
#   - Registrar todos los routers.
#
# COMO EJECUTAR:
#   cd Semana_12/app_cineflix
#   pip install -r requirements.txt
#   uvicorn main:app --reload --port 8012
#
# DOCS:
#   Swagger UI: http://localhost:8012/docs
#   ReDoc:      http://localhost:8012/redoc
# ============================================================================

from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.database.connection import DATABASE_PATH
from infrastructure.database.init_db import init_db
from interfaces.routers import movie_router
# TODO live coding: descomentar a medida que se implementen.
# from interfaces.routers import user_router, user_group_router, plan_router
# from interfaces.routers import subscription_router, catalog_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: crear tablas y cargar seed.
    init_db()
    print(f"[Cineflix] Base de datos lista en: {DATABASE_PATH}")
    yield
    # Shutdown: nada por ahora.


app = FastAPI(
    title="Cineflix API",
    description=(
        "Semana 12 - Curso de Python. API REST tipo Netflix con FastAPI + "
        "SQLite siguiendo Clean Architecture "
        "(application / infrastructure / interfaces)."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/", tags=["health"])
def health():
    return {"status": "ok", "api": "cineflix", "docs": "/docs"}


# --- Routers ---------------------------------------------------------------
app.include_router(movie_router.router)
# TODO live coding: incluir los demas routers cuando esten listos:
# app.include_router(user_router.router)
# app.include_router(user_group_router.router)
# app.include_router(plan_router.router)
# app.include_router(subscription_router.router)
# app.include_router(catalog_router.router)
