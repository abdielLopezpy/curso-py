# ============================================================================
# IMPLEMENTACION: UserSQLiteRepository  -- TODO live coding
# ============================================================================
# Plantilla: ver infrastructure/repositories/movie_sqlite_repository.py
# Modelo de fila: ver infrastructure/models/user_model.py
#
# Tablas SQL involucradas: users (FK opcional a user_groups).
# Cuidado:
#   - email es UNIQUE en la tabla -> atrapar IntegrityError y levantar
#     EntidadDuplicada.
#   - Convertir birthday str <-> date via UserModel.
# ============================================================================

# TODO
