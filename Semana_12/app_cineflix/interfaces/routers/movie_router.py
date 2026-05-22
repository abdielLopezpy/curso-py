# ============================================================================
# ROUTER: /api/movies
# ============================================================================
# Traduce HTTP <-> use cases. No contiene logica de negocio:
#   - Recibe el repositorio via Depends().
#   - Instancia el use case correspondiente.
#   - Atrapa excepciones de dominio y las convierte en HTTPException.
#
# Patron para los demas routers (user, plan, etc.): copiar este archivo y
# cambiar la entidad. La estructura es identica.
# ============================================================================

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from application.exceptions import EntidadDuplicada, EntidadNoEncontrada
from application.repositories.movie_repository import MovieRepository
from application.schemas.movie_schema import MovieCreate, MovieRead, MovieUpdate
from application.use_cases.movie.actualizar_movie import ActualizarMovie
from application.use_cases.movie.crear_movie import CrearMovie
from application.use_cases.movie.eliminar_movie import EliminarMovie
from application.use_cases.movie.listar_movies import ListarMovies
from application.use_cases.movie.obtener_movie import ObtenerMovie
from interfaces.dependencies import get_movie_repository


router = APIRouter(prefix="/api/movies", tags=["movies"])


@router.get("", response_model=List[MovieRead])
def listar_movies(repo: MovieRepository = Depends(get_movie_repository)):
    """Lista todas las peliculas."""
    return ListarMovies(repo).execute()


@router.get("/{movie_id}", response_model=MovieRead)
def obtener_movie(
    movie_id: int,
    repo: MovieRepository = Depends(get_movie_repository),
):
    """Obtiene una pelicula por id. 404 si no existe."""
    try:
        return ObtenerMovie(repo).execute(movie_id)
    except EntidadNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", response_model=MovieRead, status_code=status.HTTP_201_CREATED)
def crear_movie(
    data: MovieCreate,
    repo: MovieRepository = Depends(get_movie_repository),
):
    """Crea una pelicula. 409 si viola una restriccion UNIQUE."""
    try:
        return CrearMovie(repo).execute(data)
    except EntidadDuplicada as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{movie_id}", response_model=MovieRead)
def actualizar_movie(
    movie_id: int,
    data: MovieUpdate,
    repo: MovieRepository = Depends(get_movie_repository),
):
    """Actualiza campos parcialmente (solo los enviados)."""
    try:
        return ActualizarMovie(repo).execute(movie_id, data)
    except EntidadNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_movie(
    movie_id: int,
    repo: MovieRepository = Depends(get_movie_repository),
):
    """Elimina una pelicula. 404 si no existe."""
    try:
        EliminarMovie(repo).execute(movie_id)
    except EntidadNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
