-- Crear tabla de usuarios
CREATE TABLE
    IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP
    );

-- Crear índice para búsquedas por email
CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);

-- Crear índice para filtrar usuarios activos
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users (is_active);