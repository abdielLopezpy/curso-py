# ============================================================================
# SCHEMAS Pydantic: Catalog  -- TODO live coding
# ============================================================================
# Plantilla: ver application/schemas/movie_schema.py
#
# Campos: name, owner_id, is_public, movie_ids (List[int]).
# Sugerencia: separar endpoints para gestionar movie_ids (M:N) en lugar
# de mandar la lista completa en cada PUT:
#   POST   /api/catalogs/{id}/movies/{movie_id}   -> agregar
#   DELETE /api/catalogs/{id}/movies/{movie_id}   -> quitar
# ============================================================================

# TODO: definir CatalogCreate, CatalogRead, CatalogUpdate
