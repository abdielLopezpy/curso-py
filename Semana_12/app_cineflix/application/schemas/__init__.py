# Schemas Pydantic para entrada/salida HTTP.
# Un archivo por entidad. Cada archivo expone:
#   - <Entidad>Create  -> body del POST
#   - <Entidad>Read    -> respuesta del GET (incluye id)
#   - <Entidad>Update  -> body del PUT (campos opcionales para PATCH-like)
