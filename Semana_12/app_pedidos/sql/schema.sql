-- ============================================================================
-- App Pedidos - Schema (SQLite)
-- ============================================================================
-- Version mejorada del esquema del whiteboard. Cambios respecto al original:
--
--   1. USER_TYPE eliminado como tabla aparte.
--        Antes: USUARIO.user_type -> USER_TYPE.user_id (circular y redundante).
--        Ahora: users.role (texto: 'admin' | 'standard' | 'kid').
--        is_adult se deriva en la entidad desde birthday + fecha actual.
--
--   2. Circularidad user_group <-> subscription eliminada.
--        Antes: user_groups.subscription_id y subscriptions.group_id.
--        Ahora: solo subscriptions.group_id (un grupo puede tener varias
--               suscripciones a lo largo del tiempo).
--
--   3. PLAN_TYPE absorbido por plans.
--        Antes: PLAN_TYPE con valores fijos (dep=2, kid=3, all=4).
--        Ahora: plans.kind (texto) + plans.max_members (entero).
--               GROUP_LIMIT de subscription tambien sale de plans.max_members.
--
--   4. USER_CATALOG.catalog_id (auto-referencia circular) eliminado.
--        Ahora: catalogs (catalogo del usuario) + catalog_movies (M:N).
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ----------------------------------------------------------------------------
-- USERS
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    name           TEXT    NOT NULL,
    email          TEXT    NOT NULL UNIQUE,
    password_hash  TEXT    NOT NULL,
    birthday       TEXT    NOT NULL,                         -- ISO-8601 (YYYY-MM-DD)
    role           TEXT    NOT NULL DEFAULT 'standard',      -- 'admin' | 'standard' | 'kid'
    group_id       INTEGER,                                  -- NULL = sin grupo
    created_at     TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES user_groups(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_users_group ON users(group_id);

-- ----------------------------------------------------------------------------
-- USER_GROUPS (familia / hogar que comparte suscripcion)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS user_groups (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    owner_id    INTEGER NOT NULL,
    created_at  TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE RESTRICT
);

-- ----------------------------------------------------------------------------
-- PLANS (catalogo de planes contratables)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS plans (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    name           TEXT    NOT NULL,
    kind           TEXT    NOT NULL,                         -- 'single' | 'duo' | 'kids' | 'family'
    price          REAL    NOT NULL,
    duration_days  INTEGER NOT NULL,                         -- vigencia del plan al contratar
    max_members    INTEGER NOT NULL DEFAULT 1,               -- limite de usuarios en el grupo
    is_public      INTEGER NOT NULL DEFAULT 1,
    is_active      INTEGER NOT NULL DEFAULT 1,
    created_at     TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- SUBSCRIPTIONS (un grupo contrata un plan por un periodo)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS subscriptions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id    INTEGER NOT NULL,
    plan_id     INTEGER NOT NULL,
    started_at  TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at  TEXT    NOT NULL,                            -- ISO-8601
    is_active   INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (group_id) REFERENCES user_groups(id) ON DELETE CASCADE,
    FOREIGN KEY (plan_id)  REFERENCES plans(id)        ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_subscriptions_group ON subscriptions(group_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_plan  ON subscriptions(plan_id);

-- ----------------------------------------------------------------------------
-- MOVIES (catalogo global de peliculas)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS movies (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    url         TEXT    NOT NULL,
    age_rating  INTEGER NOT NULL DEFAULT 0,                  -- 0 = todos; 18 = adultos
    created_at  TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- CATALOGS (lista personal de peliculas de un usuario)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS catalogs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    is_public   INTEGER NOT NULL DEFAULT 0,
    owner_id    INTEGER NOT NULL,
    created_at  TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_catalogs_owner ON catalogs(owner_id);

-- ----------------------------------------------------------------------------
-- CATALOG_MOVIES (relacion M:N entre catalogos y peliculas)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS catalog_movies (
    catalog_id  INTEGER NOT NULL,
    movie_id    INTEGER NOT NULL,
    added_at    TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (catalog_id, movie_id),
    FOREIGN KEY (catalog_id) REFERENCES catalogs(id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id)   REFERENCES movies(id)   ON DELETE CASCADE
);
