-- ============================================================================
-- Schema de la base de datos: biblioteca.db (SQLite)
-- ============================================================================
-- Tres entidades con relaciones FK:
--   autores   (1) ---< (N) libros
--   libros    (1) ---< (N) prestamos
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ----------------------------------------------------------------------------
-- AUTORES
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS autores (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre       TEXT    NOT NULL,
    nacionalidad TEXT    NOT NULL,
    biografia    TEXT
);

-- ----------------------------------------------------------------------------
-- LIBROS
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS libros (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo           TEXT    NOT NULL,
    isbn             TEXT    NOT NULL UNIQUE,
    anio_publicacion INTEGER NOT NULL,
    disponible       INTEGER NOT NULL DEFAULT 1,   -- 0 = prestado, 1 = disponible
    autor_id         INTEGER NOT NULL,
    FOREIGN KEY (autor_id) REFERENCES autores(id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_libros_autor ON libros(autor_id);

-- ----------------------------------------------------------------------------
-- PRESTAMOS
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS prestamos (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    libro_id         INTEGER NOT NULL,
    nombre_usuario   TEXT    NOT NULL,
    fecha_prestamo   TEXT    NOT NULL,    -- ISO-8601
    fecha_devolucion TEXT,                -- NULL mientras no se devuelva
    FOREIGN KEY (libro_id) REFERENCES libros(id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_prestamos_libro ON prestamos(libro_id);
