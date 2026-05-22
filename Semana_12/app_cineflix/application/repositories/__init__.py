# Interfaces ABSTRACTAS de repositorios (un archivo por entidad).
#
# Cada interfaz define QUE puede hacer el repositorio, no COMO.
# La implementacion concreta vive en `infrastructure/repositories/` y traduce
# las operaciones a SQL real. Esto permite intercambiar SQLite por Postgres
# (o por un repo en memoria para tests) sin tocar el dominio ni los use cases.
