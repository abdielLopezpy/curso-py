# ============================================================================
# SCHEMAS Pydantic: User  -- TODO live coding
# ============================================================================
# Plantilla: ver application/schemas/movie_schema.py
#
# Campos esperados (ver application/entities/user.py):
#   name, email (EmailStr), password (plano en Create -> hash en use case),
#   birthday (date), role (UserRole), group_id (Optional[int])
#
# Tips:
#   - Usa Pydantic EmailStr para validar email automaticamente.
#   - En UserRead nunca devuelvas password_hash.
# ============================================================================

# TODO: definir UserCreate, UserRead, UserUpdate
