# API Biblioteca - Semana 12

API REST con **FastAPI** + **SQLite** (SQL puro) siguiendo **Clean Architecture**.

## Ejecutar

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8012
```

- Swagger UI: http://localhost:8012/docs
- ReDoc:      http://localhost:8012/redoc

## Capas

- `domain/`         → entidades + interfaces de repositorio (puro)
- `application/`    → use cases + schemas Pydantic
- `infrastructure/` → conexion SQLite + implementacion SQL
- `interfaces/`     → routers FastAPI + inyeccion de dependencias

## Entidades

- `Libro`    → IMPLEMENTADO (plantilla de referencia)
- `Autor`    → TODO (live coding)
- `Prestamo` → TODO (live coding)

Ver `../README_SEMANA_12.md` para la guia completa.
