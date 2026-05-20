-- ============================================================================
-- App Pedidos - Seed de ejemplo (idempotente)
-- ============================================================================
-- Carga datos minimos para probar los casos de uso en clase.
-- Usa INSERT OR IGNORE para evitar duplicar al reiniciar la app.
-- ============================================================================

-- Planes
INSERT OR IGNORE INTO plans (id, name, kind, price, duration_days, max_members, is_public, is_active) VALUES
    (1, 'Individual',  'single',  4.99,  30, 1, 1, 1),
    (2, 'Duo',         'duo',     7.99,  30, 2, 1, 1),
    (3, 'Kids',        'kids',    3.99,  30, 2, 1, 1),
    (4, 'Familiar',    'family', 12.99,  30, 5, 1, 1);

-- Usuarios (password_hash es ficticio, solo para ejemplo)
INSERT OR IGNORE INTO users (id, name, email, password_hash, birthday, role, group_id) VALUES
    (1, 'Ada Lovelace',     'ada@example.com',   'hash_demo_1', '1985-12-10', 'admin',    NULL),
    (2, 'Linus Torvalds',   'linus@example.com', 'hash_demo_2', '1990-06-15', 'standard', NULL),
    (3, 'Mini User',        'mini@example.com',  'hash_demo_3', '2018-01-20', 'kid',      NULL);

-- Grupo familiar
INSERT OR IGNORE INTO user_groups (id, name, owner_id) VALUES
    (1, 'Familia Lovelace', 1);

-- Asociar usuarios al grupo
UPDATE users SET group_id = 1 WHERE id IN (1, 3);

-- Suscripcion activa del grupo al plan familiar
INSERT OR IGNORE INTO subscriptions (id, group_id, plan_id, expires_at, is_active) VALUES
    (1, 1, 4, '2026-12-31', 1);

-- Peliculas
INSERT OR IGNORE INTO movies (id, title, url, age_rating) VALUES
    (1, 'Hackers',          'https://example.com/hackers.mp4',  13),
    (2, 'The Social Network','https://example.com/tsn.mp4',     13),
    (3, 'Coco',             'https://example.com/coco.mp4',     0);

-- Catalogo personal de Ada (publico) con dos peliculas
INSERT OR IGNORE INTO catalogs (id, name, is_public, owner_id) VALUES
    (1, 'Favoritas de Ada', 1, 1);

INSERT OR IGNORE INTO catalog_movies (catalog_id, movie_id) VALUES
    (1, 1),
    (1, 2);
