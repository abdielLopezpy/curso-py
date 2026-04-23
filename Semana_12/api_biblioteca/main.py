# ============================================================================
# SEMANA 12 - API Biblioteca (FastAPI + SQLModel + Clean Architecture)
# ============================================================================
# Punto de entrada de la aplicacion.
#
# Responsabilidad:
#   - Crear la instancia FastAPI.
#   - Inicializar la BD (crear tablas + seed de ejemplo).
#   - Registrar los routers de cada entidad.
#
# COMO EJECUTAR:
#   pip install -r requirements.txt
#   uvicorn main:app --reload --port 8012
#
# DOCS:
#   Swagger UI: http://localhost:8012/docs
#   ReDoc:      http://localhost:8012/redoc
# ============================================================================

from contextlib import asynccontextmanager

from fastapi import FastAPI

# Importar las entidades SQLModel asegura que sus tablas queden registradas
# en SQLModel.metadata (aunque aqui creamos la BD con schema.sql).
from domain.entities.libro import Libro          # noqa: F401
from domain.entities.autor import Autor          # noqa: F401
from domain.entities.prestamo import Prestamo    # noqa: F401

from infrastructure.database.init_db import init_db
from interfaces.routers import libro_router, autor_router, prestamo_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: crear tablas y cargar seed si hace falta.
    init_db()
    yield
    # Shutdown: nada que hacer por ahora.


app = FastAPI(
    title="API Biblioteca",
    description=(
        "Semana 12 - Curso de Python. API REST con FastAPI + SQLModel "
        "siguiendo Clean Architecture (domain / application / infrastructure / interfaces)."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", tags=["health"])
def health():
    return {
        "status": "ok",
        "api": "biblioteca",
        "docs": "/docs",
    }


# Registro de routers (uno por entidad).
app.include_router(libro_router.router)
app.include_router(autor_router.router)
app.include_router(prestamo_router.router)
