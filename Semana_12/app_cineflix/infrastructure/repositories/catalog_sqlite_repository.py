# ============================================================================
# IMPLEMENTACION: CatalogSQLiteRepository  -- TODO live coding
# ============================================================================
# Plantilla: ver infrastructure/repositories/movie_sqlite_repository.py
#
# Tabla principal: catalogs.
# Tabla M:N:       catalog_movies (catalog_id, movie_id).
#
# Para obtener_por_id:
#   1. SELECT * FROM catalogs WHERE id = ?
#   2. SELECT movie_id FROM catalog_movies WHERE catalog_id = ?
#   3. Construir CatalogModel.from_row(row, movie_ids=[...]).to_entity()
# ============================================================================

# TODO
