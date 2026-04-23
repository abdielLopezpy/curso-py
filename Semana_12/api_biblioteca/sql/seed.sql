-- ============================================================================
-- Datos de ejemplo (seed) para biblioteca.db
-- ============================================================================
-- Ejecutar despues de schema.sql.
-- Los INSERT usan OR IGNORE para que correr el seed dos veces no duplique
-- registros (gracias al UNIQUE en isbn y al PK autoincrement).
-- ============================================================================

INSERT OR IGNORE INTO autores (id, nombre, nacionalidad, biografia) VALUES
    (1, 'Gabriel Garcia Marquez', 'Colombiana', 'Premio Nobel de Literatura 1982.'),
    (2, 'Isabel Allende',         'Chilena',    'Novelista reconocida por La casa de los espiritus.'),
    (3, 'Jorge Luis Borges',      'Argentina',  'Ensayista y poeta, maestro del cuento breve.');

INSERT OR IGNORE INTO libros (id, titulo, isbn, anio_publicacion, disponible, autor_id) VALUES
    (1, 'Cien anos de soledad',   '9780307474728', 1967, 1, 1),
    (2, 'El amor en los tiempos del colera', '9780307387264', 1985, 1, 1),
    (3, 'La casa de los espiritus', '9788401242052', 1982, 1, 2),
    (4, 'Ficciones',              '9788420633121', 1944, 1, 3);

-- Sin prestamos iniciales: se crean desde el API.
