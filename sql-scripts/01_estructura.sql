-- ========================================================
-- ESTRUCTURA DE BASE DE DATOS - GESTIÓN DE NOTAS
-- Este script crea las tablas: usuarios, profesores,
-- estudiantes, materias y notas.
-- Ejecutar PRIMERO, antes de 02_datos_prueba.sql
-- (Ejecutar en el Query Tool de pgAdmin 4)
-- ========================================================

-- 1. Tabla: usuarios (Cuentas de acceso al sistema)
CREATE TABLE usuarios (
    id            SERIAL PRIMARY KEY,
    username      VARCHAR(50) UNIQUE NOT NULL,
    password      VARCHAR(100) NOT NULL,
    rol           VARCHAR(20) NOT NULL CHECK (rol IN ('estudiante', 'profesor')),
    activo        BOOLEAN DEFAULT TRUE,
    creado_en     TIMESTAMP DEFAULT NOW()
);

-- 2. Tabla: profesores (Docentes de la universidad)
CREATE TABLE profesores (
    id                  SERIAL PRIMARY KEY,
    usuario_id          INTEGER UNIQUE REFERENCES usuarios(id) ON DELETE CASCADE,
    documento_docente   VARCHAR(20) UNIQUE NOT NULL,
    nombre              VARCHAR(100) NOT NULL,
    correo              VARCHAR(100) UNIQUE NOT NULL,
    telefono            VARCHAR(20),
    especialidad        VARCHAR(100)
);

-- 3. Tabla: estudiantes (Alumnos matriculados)
CREATE TABLE estudiantes (
    id                  SERIAL PRIMARY KEY,
    usuario_id          INTEGER UNIQUE REFERENCES usuarios(id) ON DELETE CASCADE,
    codigo              VARCHAR(20) UNIQUE NOT NULL,
    nombre              VARCHAR(100) NOT NULL,
    correo              VARCHAR(100) UNIQUE NOT NULL,
    telefono            VARCHAR(20),
    programa_academico  VARCHAR(100) DEFAULT 'Ingeniería de Sistemas'
);

-- 4. Tabla: materias (Asignaturas del plan de estudios)
CREATE TABLE materias (
    id             SERIAL PRIMARY KEY,
    codigo_materia VARCHAR(10) UNIQUE NOT NULL,
    nombre         VARCHAR(100) NOT NULL,
    creditos       INTEGER NOT NULL CHECK (creditos >= 1 AND creditos <= 6) DEFAULT 3,
    profesor_id    INTEGER REFERENCES profesores(id) ON DELETE SET NULL
);

-- 5. Tabla: notas (Registro de calificaciones de estudiantes)
CREATE TABLE notas (
    id              SERIAL PRIMARY KEY,
    estudiante_id   INTEGER REFERENCES estudiantes(id) ON DELETE CASCADE,
    materia_id      INTEGER REFERENCES materias(id) ON DELETE CASCADE,
    periodo         VARCHAR(10) NOT NULL,
    tipo_nota       VARCHAR(50) NOT NULL CHECK (tipo_nota IN ('Parcial 1', 'Parcial 2', 'Examen Final', 'Seguimiento')),
    porcentaje      NUMERIC(5,2) NOT NULL CHECK (porcentaje > 0 AND porcentaje <= 100) DEFAULT 30.0,
    nota            NUMERIC(5,2) NOT NULL CHECK (nota >= 0.0 AND nota <= 100.0),
    registrado_en   TIMESTAMP DEFAULT NOW()
);