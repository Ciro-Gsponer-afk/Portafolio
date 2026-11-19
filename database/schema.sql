-- ============================================================
-- PORTAFOLIO — DISEÑO FÍSICO (MySQL 8)
-- Fase 1: crea las tablas y carga datos de ejemplo.
--
-- Cómo usarlo en local:
--   mysql -u root -p < schema.sql
--
-- En Clever Cloud la base YA existe, entonces:
--   1) NO ejecutar CREATE DATABASE ni USE.
--   2) Ejecutar solo los CREATE TABLE e INSERT.
-- El hosting entrega usuario, contraseña, host y nombre de la base;
-- esos datos van en el archivo .env (nunca en Git).
-- ============================================================

CREATE DATABASE IF NOT EXISTS portafolio_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE portafolio_db;

-- Se borran en orden inverso a las dependencias (primero las hijas).
-- Esto permite volver a correr el script desde cero sin errores.
DROP TABLE IF EXISTS proyecto;
DROP TABLE IF EXISTS idioma;
DROP TABLE IF EXISTS skill;
DROP TABLE IF EXISTS educacion;
DROP TABLE IF EXISTS experiencia;
DROP TABLE IF EXISTS red_social;
DROP TABLE IF EXISTS perfil;
DROP TABLE IF EXISTS usuario;

-- ------------------------------------------------------------
-- USUARIO: credenciales del dueño del portfolio.
-- Solo se guarda el HASH de la contraseña, nunca el texto plano.
-- ------------------------------------------------------------
CREATE TABLE usuario (
  id            INT UNSIGNED NOT NULL AUTO_INCREMENT,
  username      VARCHAR(50)  NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  creado_en     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_usuario_username (username)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- PERFIL: datos de la sección "Acerca de" y del banner.
-- usuario_id es UNIQUE para que la relación sea 1 a 1.
-- ------------------------------------------------------------
CREATE TABLE perfil (
  id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
  usuario_id  INT UNSIGNED NOT NULL,
  nombre      VARCHAR(100) NOT NULL,
  titulo      VARCHAR(120) NOT NULL,
  descripcion TEXT         NOT NULL,
  foto_url    VARCHAR(255) NOT NULL DEFAULT 'img/perfil.jpg',
  banner_url  VARCHAR(255) NOT NULL DEFAULT 'img/banner.jpg',
  cv_url      VARCHAR(255) NOT NULL DEFAULT 'cv/Ciro_Gsponer_CV.pdf',
  PRIMARY KEY (id),
  UNIQUE KEY uq_perfil_usuario (usuario_id),
  CONSTRAINT fk_perfil_usuario
    FOREIGN KEY (usuario_id) REFERENCES usuario (id)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- RED SOCIAL: íconos del header (GitHub, LinkedIn, etc.).
-- 'icono' guarda la clase de FontAwesome, por ejemplo:
--   fa-brands fa-github
-- ------------------------------------------------------------
CREATE TABLE red_social (
  id        INT UNSIGNED NOT NULL AUTO_INCREMENT,
  perfil_id INT UNSIGNED NOT NULL,
  nombre    VARCHAR(60)  NOT NULL,
  icono     VARCHAR(80)  NOT NULL,
  url       VARCHAR(255) NOT NULL,
  orden     INT          NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY idx_red_social_orden (perfil_id, orden),
  CONSTRAINT fk_red_social_perfil
    FOREIGN KEY (perfil_id) REFERENCES perfil (id)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- EXPERIENCIA: fecha_fin NULL = "Actualidad".
-- La sección puede quedar vacía; la vista mostrará un mensaje.
-- ------------------------------------------------------------
CREATE TABLE experiencia (
  id           INT UNSIGNED NOT NULL AUTO_INCREMENT,
  perfil_id    INT UNSIGNED NOT NULL,
  puesto       VARCHAR(120) NOT NULL,
  empresa      VARCHAR(120) NOT NULL,
  descripcion  TEXT         NOT NULL,
  fecha_inicio DATE         NOT NULL,
  fecha_fin    DATE         NULL,
  orden        INT          NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY idx_experiencia_orden (perfil_id, orden),
  CONSTRAINT fk_experiencia_perfil
    FOREIGN KEY (perfil_id) REFERENCES perfil (id)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- EDUCACION: fecha_fin NULL = carrera en curso.
-- ------------------------------------------------------------
CREATE TABLE educacion (
  id           INT UNSIGNED NOT NULL AUTO_INCREMENT,
  perfil_id    INT UNSIGNED NOT NULL,
  institucion  VARCHAR(120) NOT NULL,
  titulo       VARCHAR(120) NOT NULL,
  logo_url     VARCHAR(255) NOT NULL DEFAULT 'img/instituciones/default.png',
  fecha_inicio DATE         NOT NULL,
  fecha_fin    DATE         NULL,
  orden        INT          NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY idx_educacion_orden (perfil_id, orden),
  CONSTRAINT fk_educacion_perfil
    FOREIGN KEY (perfil_id) REFERENCES perfil (id)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- SKILL: hard y soft skills en una sola tabla, separadas por 'tipo'.
-- El CHECK evita guardar porcentajes fuera de 0-100.
-- ------------------------------------------------------------
CREATE TABLE skill (
  id         INT UNSIGNED NOT NULL AUTO_INCREMENT,
  perfil_id  INT UNSIGNED NOT NULL,
  nombre     VARCHAR(80)  NOT NULL,
  porcentaje TINYINT UNSIGNED NOT NULL,
  tipo       ENUM('hard','soft') NOT NULL DEFAULT 'hard',
  orden      INT          NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY idx_skill_orden (perfil_id, tipo, orden),
  CONSTRAINT chk_skill_porcentaje CHECK (porcentaje BETWEEN 0 AND 100),
  CONSTRAINT fk_skill_perfil
    FOREIGN KEY (perfil_id) REFERENCES perfil (id)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- IDIOMA: sección extra con barra de porcentaje.
-- ------------------------------------------------------------
CREATE TABLE idioma (
  id         INT UNSIGNED NOT NULL AUTO_INCREMENT,
  perfil_id  INT UNSIGNED NOT NULL,
  nombre     VARCHAR(80)  NOT NULL,
  nivel      VARCHAR(50)  NOT NULL,
  porcentaje TINYINT UNSIGNED NOT NULL,
  orden      INT          NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY idx_idioma_orden (perfil_id, orden),
  CONSTRAINT chk_idioma_porcentaje CHECK (porcentaje BETWEEN 0 AND 100),
  CONSTRAINT fk_idioma_perfil
    FOREIGN KEY (perfil_id) REFERENCES perfil (id)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- PROYECTO: incluye este mismo portfolio como evidencia.
-- 'link' apunta al repositorio o demo online.
-- ------------------------------------------------------------
CREATE TABLE proyecto (
  id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
  perfil_id   INT UNSIGNED NOT NULL,
  nombre      VARCHAR(120) NOT NULL,
  descripcion TEXT         NOT NULL,
  fecha       DATE         NOT NULL,
  link        VARCHAR(255) NOT NULL,
  imagen_url  VARCHAR(255) NOT NULL DEFAULT 'img/proyectos/default.jpg',
  orden       INT          NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY idx_proyecto_orden (perfil_id, orden),
  CONSTRAINT fk_proyecto_perfil
    FOREIGN KEY (perfil_id) REFERENCES perfil (id)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================
-- DATOS DE EJEMPLO
-- ============================================================

-- Usuario: ciro / contraseña: portafolio2026
-- El hash se generó con werkzeug.security.generate_password_hash.
-- En Fase 4 se explica cómo cambiarlo por uno propio.
INSERT INTO usuario (id, username, password_hash) VALUES
(1, 'ciro', 'scrypt:32768:8:1$796KvYSoIuuvIm3M$6f95b2fb8b0641b333f1661825e7bb6cafb5794b8b68ce0002b44f30a2223078f4b955ecfc969e2f68aeb3b7d2b461c19776fc3e0dc108004386bd69bcf4fb77');

INSERT INTO perfil
  (id, usuario_id, nombre, titulo, descripcion, foto_url, banner_url, cv_url)
VALUES
(1, 1,
 'Ciro Gsponer',
 'Full Stack Developer Jr',
 'Soy estudiante de 6° año del Instituto Técnico Renault y me formo como desarrollador Full Stack. Me interesa construir aplicaciones web completas: desde la base de datos y la lógica en Python hasta una interfaz clara y responsive. Disfruto aprender con proyectos reales, trabajar en equipo y documentar lo que hago para poder explicarlo.',
 'img/perfil.jpg',
 'img/banner.jpg',
 'cv/Ciro_Gsponer_CV.pdf');

-- Redes del header (los links son de ejemplo: reemplazarlos por los reales).
INSERT INTO red_social (perfil_id, nombre, icono, url, orden) VALUES
(1, 'GitHub',   'fa-brands fa-github',   'https://github.com/Ciro-Gsponer-afk', 1),
(1, 'LinkedIn', 'fa-brands fa-linkedin', 'https://www.linkedin.com/in/ciro-gsponer-4a9b76394/', 2),
(1, 'Correo',   'fa-solid fa-envelope',  'mailto:cirogsp235@gmail.com', 3);

-- Experiencia: si no corresponde, se puede eliminar desde el modo edición.
-- fecha_fin NULL se muestra como "Actualidad".
INSERT INTO experiencia
  (perfil_id, puesto, empresa, descripcion, fecha_inicio, fecha_fin, orden)
VALUES
(1, 'Práctica Profesionalizante',
    'Instituto Técnico Renault',
    'Participé en el desarrollo de una aplicación web con Flask y MySQL como parte de la práctica profesionalizante de 5° año. Trabajé en el modelo de datos, las rutas y la interfaz.',
    '2025-04-01', '2025-11-30', 1);

-- Educación: fecha_fin NULL = "en curso".
INSERT INTO educacion
  (perfil_id, institucion, titulo, logo_url, fecha_inicio, fecha_fin, orden)
VALUES
(1, 'Instituto Técnico Renault',
    'Técnico en Programación — 5° año',
    'img/instituciones/renault.png',
    '2021-03-01', NULL, 1);

-- Hard skills (tipo 'hard').
INSERT INTO skill (perfil_id, nombre, porcentaje, tipo, orden) VALUES
(1, 'Python',        75, 'hard', 1),
(1, 'Flask',         70, 'hard', 2),
(1, 'MySQL',         65, 'hard', 3),
(1, 'HTML y CSS',    80, 'hard', 4),
(1, 'JavaScript',    60, 'hard', 5),
(1, 'Git y GitHub',  70, 'hard', 6);

-- Soft skills (tipo 'soft').
INSERT INTO skill (perfil_id, nombre, porcentaje, tipo, orden) VALUES
(1, 'Trabajo en equipo',      85, 'soft', 1),
(1, 'Comunicación',           80, 'soft', 2),
(1, 'Resolución de problemas', 75, 'soft', 3),
(1, 'Organización',           80, 'soft', 4);

-- Idiomas.
INSERT INTO idioma (perfil_id, nombre, nivel, porcentaje, orden) VALUES
(1, 'Español', 'Nativo',      100, 1),
(1, 'Inglés',  'Intermedio',   65, 2);

-- Proyectos: Weather Report y este mismo portfolio.
INSERT INTO proyecto
  (perfil_id, nombre, descripcion, fecha, link, imagen_url, orden)
VALUES
(1, 'Weather Report',
    'Aplicación web que consulta una API del clima y muestra el pronóstico de distintas ciudades. Incluye búsqueda, íconos según el estado del tiempo y diseño responsive.',
    '2025-10-15',
    'https://github.com/cirogsponer/weather-report',
    'img/proyectos/weather-report.jpg',
    1),
(1, 'Portafolio Personal',
    'Este mismo sitio: Flask, MySQL y Jinja2, con autenticación, modo edición y despliegue en la nube. Es la evidencia principal del trabajo integrador.',
    '2026-11-01',
    'https://github.com/cirogsponer/portafolio',
    'img/proyectos/portafolio.jpg',
    2);
