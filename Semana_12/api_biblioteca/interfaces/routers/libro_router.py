# ============================================================================
# ROUTER: /api/libros
# ============================================================================
# Traduce requests HTTP en llamadas a use cases y respuestas HTTP a partir
# de las entidades/schemas. El router NO contiene logica de negocio.
# ============================================================================

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from application.schemas.libro_schema import LibroCreate, LibroRead, LibroUpdate
from application.use_cases.libro.actualizar_libro import ActualizarLibro
from application.use_cases.libro.crear_libro import CrearLibro
from application.use_cases.libro.eliminar_libro import EliminarLibro
from application.use_cases.libro.listar_libros import ListarLibros
from application.use_cases.libro.obtener_libro import ObtenerLibro
from domain.exceptions import EntidadDuplicada, EntidadNoEncontrada
from domain.repositories.libro_repository import LibroRepository
from interfaces.dependencies import get_libro_repository


router = APIRouter(prefix="/api/libros", tags=["libros"])


@router.get("", response_model=List[LibroRead])
def listar_libros(repo: LibroRepository = Depends(get_libro_repository)):
    return ListarLibros(repo).execute()


@router.get("/{libro_id}", response_model=LibroRead)
def obtener_libro(libro_id: int, repo: LibroRepository = Depends(get_libro_repository)):
    try:
        return ObtenerLibro(repo).execute(libro_id)
    except EntidadNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", response_model=LibroRead, status_code=status.HTTP_201_CREATED)
def crear_libro(data: LibroCreate, repo: LibroRepository = Depends(get_libro_repository)):
    try:
        return CrearLibro(repo).execute(data)
    except EntidadDuplicada as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{libro_id}", response_model=LibroRead)
def actualizar_libro(
    libro_id: int,
    data: LibroUpdate,
    repo: LibroRepository = Depends(get_libro_repository),
):
    try:
        return ActualizarLibro(repo).execute(libro_id, data)
    except EntidadNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except EntidadDuplicada as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{libro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_libro(libro_id: int, repo: LibroRepository = Depends(get_libro_repository)):
    try:
        EliminarLibro(repo).execute(libro_id)
    except EntidadNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
