# Casos de uso de la capa de aplicacion.
#
# Convencion:
#   - Una carpeta por entidad: movie/, user/, plan/, subscription/, catalog/
#   - Un archivo por caso de uso (crear_, listar_, obtener_, actualizar_, eliminar_)
#   - Cada caso de uso es una CLASE con un solo metodo `execute(...)`.
#
# Estado:
#   - movie/        -> IMPLEMENTADO (sirve como plantilla)
#   - user/         -> TODO (live coding)
#   - user_group/   -> TODO
#   - plan/         -> TODO
#   - subscription/ -> TODO (incluye regla "expira en duration_days dias")
#   - catalog/      -> TODO (incluye gestion de movie_ids)
