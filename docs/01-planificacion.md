# Fase 1 — Planificación del Portfolio

Dueño: **Ciro Gsponer** — Full Stack Developer Jr
Instituto Técnico Renault — 5° año, turno/info: Español e Inglés

---

## 1. Objetivo

Construir un portfolio web full stack donde **todo el contenido se lee desde MySQL**:
perfil, redes, experiencia, educación, skills, idiomas y proyectos.
El sitio es público para visitantes y tiene un **modo edición** que se activa al iniciar sesión.
La estética es nocturna (negro azulado, azul, morado y dorado) y debe verse bien en
celular, tablet y escritorio.

---

## 2. Decisiones técnicas (y por qué)

| Tema | Decisión | Por qué (una línea) |
|---|---|---|
| Backend | Flask + Jinja2 | Es el stack pedido y permite separar rutas, modelos y plantillas. |
| Base de datos | MySQL en Clever Cloud | Es el motor pedido; Clever Cloud da una URL de conexión sin instalar nada. |
| Acceso a datos | Flask-SQLAlchemy (sobre MySQL) | Cada tabla se vuelve una **clase** → la POO del checklist aparece de forma natural. |
| Conexión MySQL | Driver `mysql-connector-python` | Ya está instalado en la máquina y SQLAlchemy lo soporta. |
| Formularios | Flask-WTF | Trae validación y **protección CSRF** sin escribirla a mano. |
| Contraseñas | `werkzeug.security` | Viene con Flask; guarda hash, nunca la contraseña real. |
| CSS | CSS propio (sin Bootstrap) | Más simple de defender y deja ver las **media queries** exigidas. |
| Modales | `<dialog>` nativo + JS básico | Evita librerías; abrir/cerrar un modal es una línea de JS. |
| Estructura | Paquete `app/` con `models`, `routes`, `forms`, `templates`, `static` | Ordena el proyecto y cumple el requisito de carpetas. |

> Se instalarán en Fase 2: `flask-sqlalchemy`, `flask-wtf`, `python-dotenv`.
> (Flask, SQLAlchemy, Werkzeug y mysql-connector ya están disponibles.)

---

## 3. Estructura de carpetas

```
Portafolio/
├── app/
│   ├── __init__.py            # crea la app Flask y conecta la base (Fase 2)
│   ├── config.py              # lee SECRET_KEY y DATABASE_URL desde .env (Fase 2)
│   ├── models/                # clases POO + tablas
│   │   ├── __init__.py
│   │   ├── item_portfolio.py  # clase BASE abstracta (Fase 2)
│   │   ├── usuario.py
│   │   ├── perfil.py
│   │   ├── red_social.py
│   │   ├── experiencia.py
│   │   ├── educacion.py
│   │   ├── skill.py
│   │   ├── idioma.py
│   │   └── proyecto.py
│   ├── routes/                # vistas (endpoints)
│   │   ├── __init__.py
│   │   ├── publicas.py        # index, descarga de CV (Fase 2/6)
│   │   ├── auth.py            # login / logout (Fase 4)
│   │   └── edicion.py         # alta, edición y baja (Fase 5)
│   ├── forms/                 # formularios Flask-WTF
│   │   ├── __init__.py
│   │   ├── login.py           # Fase 4
│   │   └── items.py           # Fase 5
│   ├── templates/
│   │   ├── base.html          # esqueleto + header + footer (Fase 3)
│   │   ├── index.html         # hereda de base.html (Fase 3)
│   │   ├── secciones/         # un partial por sección (Fase 3)
│   │   │   ├── _banner.html
│   │   │   ├── _acerca.html
│   │   │   ├── _experiencia.html
│   │   │   ├── _educacion.html
│   │   │   ├── _skills.html
│   │   │   ├── _idiomas.html
│   │   │   └── _proyectos.html
│   │   ├── modales/           # formularios dentro de <dialog> (Fase 5)
│   │   │   ├── _modal_experiencia.html
│   │   │   ├── _modal_educacion.html
│   │   │   ├── _modal_skill.html
│   │   │   ├── _modal_idioma.html
│   │   │   ├── _modal_proyecto.html
│   │   │   └── _modal_perfil.html
│   │   └── errores/
│   │       ├── 404.html
│   │       └── 500.html
│   └── static/
│       ├── css/estilos.css    # Fase 3
│       ├── js/main.js         # modales, confirmación, drag & drop (Fase 3/5/6)
│       ├── img/               # logo.svg, favicon.ico, perfil.jpg, banner.jpg, proyectos/
│       └── cv/Ciro_Gsponer_CV.pdf
├── database/
│   └── schema.sql             # diseño físico (esta fase)
├── docs/
│   ├── 01-planificacion.md    # este archivo
│   ├── wireframe.html         # maqueta visual navegable
│   └── PREGUNTAS_DEFENSA.md   # Fase 8
├── .env                       # secretos reales (NO se sube)
├── .env.example               # plantilla para subir a Git
├── .gitignore
├── requirements.txt           # Fase 2
├── run.py                     # arranca el servidor (Fase 2)
└── README.md                  # Fase 7/8
```

---

## 4. Modelo relacional (diseño lógico)

### Relaciones

```
usuario (1) ───── (1) perfil          un usuario edita un solo portfolio
perfil  (1) ───── (N) red_social      un perfil tiene varias redes
perfil  (1) ───── (N) experiencia     ... y varias experiencias
perfil  (1) ───── (N) educacion
perfil  (1) ───── (N) skill
perfil  (1) ───── (N) idioma
perfil  (1) ───── (N) proyecto
```

**Por qué todas las secciones apuntan a `perfil`:** el portfolio es de una sola persona.
La clave foránea `perfil_id` deja claro a quién pertenece cada ítem y permite, si algún día
se agrega otro portfolio, separar el contenido sin rediseñar las tablas.
En el código siempre se usa el perfil del usuario logueado (o el `id = 1` en la vista pública).

### Tablas y campos

**usuario**
- `id` INT UNSIGNED · PK, autoincremental
- `username` VARCHAR(50) · NOT NULL, UNIQUE (nombre de usuario del login)
- `password_hash` VARCHAR(255) · NOT NULL (hash generado con Werkzeug, nunca texto plano)
- `creado_en` TIMESTAMP · DEFAULT CURRENT_TIMESTAMP

**perfil**
- `id` INT UNSIGNED · PK
- `usuario_id` INT UNSIGNED · NOT NULL, UNIQUE, FK → `usuario.id` (relación 1:1)
- `nombre` VARCHAR(100) · NOT NULL
- `titulo` VARCHAR(120) · NOT NULL (ej. "Full Stack Developer Jr")
- `descripcion` TEXT · NOT NULL (texto de "Acerca de")
- `foto_url` VARCHAR(255) · ruta dentro de `static/`
- `banner_url` VARCHAR(255) · ruta dentro de `static/`
- `cv_url` VARCHAR(255) · ruta del PDF dentro de `static/`

**red_social**
- `id` PK · `perfil_id` FK · `nombre` · `icono` (clase FontAwesome) · `url` · `orden`

**experiencia**
- `id` PK · `perfil_id` FK
- `puesto` VARCHAR(120) · `empresa` VARCHAR(120) · `descripcion` TEXT
- `fecha_inicio` DATE · `fecha_fin` DATE NULL (`NULL` = "Actualidad")
- `orden` INT

**educacion**
- `id` PK · `perfil_id` FK
- `institucion` VARCHAR(120) · `titulo` VARCHAR(120) · `logo_url` VARCHAR(255)
- `fecha_inicio` DATE · `fecha_fin` DATE NULL (`NULL` = "en curso")
- `orden` INT

**skill**
- `id` PK · `perfil_id` FK
- `nombre` VARCHAR(80) · `porcentaje` TINYINT (0 a 100)
- `tipo` ENUM('hard','soft') · `orden` INT

**idioma**
- `id` PK · `perfil_id` FK
- `nombre` VARCHAR(80) · `nivel` VARCHAR(50) (ej. "Nativo", "Intermedio")
- `porcentaje` TINYINT (0 a 100) · `orden` INT

**proyecto**
- `id` PK · `perfil_id` FK
- `nombre` VARCHAR(120) · `descripcion` TEXT · `fecha` DATE
- `link` VARCHAR(255) · `imagen_url` VARCHAR(255) · `orden` INT

### Decisiones sobre los datos

1. **`fecha_fin` en NULL significa "hoy"**: así no hace falta un booleano `actualidad`.
2. **Columna `orden`**: permite ordenar sin tocar fechas y habilita el drag & drop opcional.
3. **`skill.tipo` como ENUM**: una sola tabla para hard y soft, filtradas por tipo en la vista.
4. **Porcentajes con CHECK**: MySQL rechaza valores fuera de 0–100.
5. **Imágenes**: en la base se guarda la **ruta relativa** (`img/perfil.jpg`), no el archivo.
   El archivo vive en `static/`. En Fase 5 se agrega la subida.

---

## 5. Wireframe (desktop)

```
┌──────────────────────────────────────────────────────────────────┐
│ [logo] CIRO GSPONER          [GitHub][LinkedIn][Mail]  [ Login ] │ header fijo
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│      BANNER nocturno (degradado + imagen)                        │
│      "Full Stack Developer Jr"                                   │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│  Acerca de                                                       │
│  ┌────────┐  Ciro Gsponer                                        │
│  │  foto  │  Full Stack Developer Jr · Estudiante 5° año         │
│  └────────┘  Descripción profesional...           [ ⬇ Descargar CV ] │
├──────────────────────────────────────────────────────────────────┤
│  Experiencia                                    [ + Agregar ]    │
│  ┌─────────────────────────────────────────────┐                 │
│  │ Puesto · Empresa · 2025 — Actualidad   [✎][✕]│                │
│  │ Descripción breve                            │                │
│  └─────────────────────────────────────────────┘                 │
│  (si no hay filas: "Todavía no cargué experiencias")            │
├──────────────────────────────────────────────────────────────────┤
│  Educación                                      [ + Agregar ]    │
│  [logo] Instituto Técnico Renault · 2021 — 2026        [✎][✕]   │
├──────────────────────────────────────────────────────────────────┤
│  Skills                                                         │
│  Hard skills:  (○ 75%) Python   (○ 70%) Flask  ...              │
│  Soft skills:  (○ 85%) Trabajo en equipo ...                    │
│  Idiomas:      Español ██████████ 100% · Inglés ██████ 65%      │
├──────────────────────────────────────────────────────────────────┤
│  Proyectos                                      [ + Agregar ]    │
│  ┌───────────┐ Weather Report · 2025                  [✎][✕]   │
│  │  captura  │ App del clima con API...  [Ver proyecto →]       │
│  └───────────┘                                                  │
├──────────────────────────────────────────────────────────────────┤
│  VIDEO / DEMO (iframe)                                           │
├──────────────────────────────────────────────────────────────────┤
│  © 2026 Ciro Gsponer · Hecho con Flask + MySQL                   │
└──────────────────────────────────────────────────────────────────┘
```

Los botones `[✎]`, `[✕]` y `[ + Agregar ]` **solo aparecen con sesión iniciada**.

### Mobile (menos de 576 px)

```
┌────────────────────┐
│ [logo] Ciro    [☰] │   menú hamburguesa
├────────────────────┤
│      BANNER        │
├────────────────────┤
│ [foto]             │
│ Ciro Gsponer       │
│ descripción...     │
│ [ Descargar CV ]   │
├────────────────────┤
│ Experiencia        │
│ ┌────────────────┐ │
│ │ Puesto         │ │
│ │ Empresa        │ │
│ └────────────────┘ │
├────────────────────┤
│ Skills (1 columna) │
└────────────────────┘
```

**Tablet (576–991 px):** dos columnas para skills y proyectos, header sin menú hamburguesa.
**Escritorio (992 px o más):** el layout completo de arriba.

---

## 6. Diseño visual

- **Paleta**
  - Fondo: `#05060f` y `#0b1020`
  - Superficie de tarjetas: `#121a33`
  - Azul: `#2b4c9b` / acento `#4f7cff`
  - Morado: `#6d28d9` / `#8b5cf6`
  - Dorado: `#d4af37` / `#f0c75e`
  - Texto: `#e8eaf6` (principal), `#9aa4c7` (secundario)
- **Tipografías (Google Fonts)**: `Orbitron` para títulos, `Inter` para texto.
- **Animación prevista**: las tarjetas aparecen con `opacity` y `translateY` mediante
  una transición CSS y la clase `.visible` que agrega un `IntersectionObserver` en `main.js`.
  Se comentará con `/* ANIMACIÓN: ... */`.
- **Íconos**: FontAwesome por CDN (`fa-brands` para redes, `fa-solid` para lápiz, cruz, descarga).
- **Favicon y logo**: SVG propio con iniciales "CG" en dorado sobre fondo azul noche.

---

## 7. Los 4 pilares de POO (cómo se van a cumplir)

| Pilar | Dónde | Idea |
|---|---|---|
| **Abstracción** | `ItemPortfolio` | Define qué comparte todo ítem del portfolio: `id`, `orden`, `resumen()` y `para_formulario()`. No se instancia sola. |
| **Encapsulamiento** | Métodos de cada clase | Los datos se leen y modifican con métodos (`resumen()`, `porcentaje_seguro()`); los atributos internos usan `_` y se validan antes de guardar. |
| **Herencia** | `Experiencia`, `Educacion`, `Proyecto`, `Skill`, `Idioma`, `RedSocial` | Heredan de `ItemPortfolio` y reutilizan lo común. |
| **Polimorfismo** | `resumen()` | Cada clase hija lo sobrescribe: la experiencia devuelve "Puesto · Empresa · fechas"; el proyecto devuelve "Nombre · fecha". La plantilla llama `item.resumen()` sin preguntar de qué clase es. |

En el código irán comentarios visibles del tipo:
`# PILAR: HERENCIA - Experiencia hereda de ItemPortfolio para reutilizar resumen y orden.`

> Nota técnica: las clases heredan de `ItemPortfolio` **y** de `db.Model`
> (`class Experiencia(ItemPortfolio, db.Model)`). `ItemPortfolio` es un *mixin*:
> solo aporta métodos, no columnas, así que no complica el mapeo de SQLAlchemy.

---

## 8. Lo que NO se hace en esta fase

- No se instala nada nuevo ni se escribe código de la app.
- No se conecta todavía la base: el `schema.sql` se ejecutará en Fase 2.
- La maqueta `wireframe.html` es solo referencia visual, no la plantilla final.

**Próxima fase (2):** crear la app Flask, la conexión, las clases POO y las rutas de lectura.
