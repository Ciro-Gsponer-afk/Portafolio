# Fase 7 — Deploy paso a paso

Objetivo: publicar el portfolio con **Flask en Clever Cloud** y la **base MySQL en Clever Cloud**.
Todo lo sensible va en variables de entorno; nada de credenciales en Git.

> Documentación oficial usada: [Python en Clever Cloud](https://www.clever.cloud/developers/doc/deploy/applications/python/),
> [MySQL add-on](https://www.clever.cloud/developers/doc/deploy/databases/mysql/),
> [Variables de entorno](https://www.clever.cloud/developers/doc/develop/common-configuration/environment-variables/).

---

## 0. Preparación local (5 minutos)

```bash
# 1) Instalar lo que falta (gunicorn es el servidor de producción)
pip install -r requirements.txt

# 2) Probar que la app sigue andando en local
python run.py
# abrir http://127.0.0.1:5000 y hacer login con ciro / portafolio2026

# 3) Generar una clave secreta NUEVA para producción
python -c "import secrets; print(secrets.token_hex(32))"
```

Guardá el valor del paso 3 en un lugar seguro: va en `SECRET_KEY` del servidor.
**No lo subas a Git** (`.env` ya está en `.gitignore`).

Antes de seguir, confirmá que el working tree esté limpio:

```bash
git status
git push origin main
```

---

## 1. Crear la base MySQL (add-on)

1. Entrá a la [consola de Clever Cloud](https://console.clever-cloud.com).
2. **Create → Add-on → MySQL**.
3. Elegí:
   - **Plan**: `DEV` (gratis, alcanza para defender; no tiene backups ni SLA). Para algo real, un plan XS.
   - **Versión**: 8.4 (LTS recomendada).
   - **Región**: la misma que vas a usar para la aplicación (ej. Paris).
   - **Nombre**: `portafolio-db`.
4. Creá el add-on. Clever Cloud **ya crea la base de datos**: por eso no se ejecuta
   `CREATE DATABASE` ni `USE`.

### 1.1 Cargar las tablas y los datos de ejemplo

En el dashboard del add-on vas a ver host, puerto, usuario, contraseña y nombre de base.
Tenés dos formas:

**A) Desde el navegador (más simple)**

1. Abrí [phpMyAdmin de Clever Cloud](https://pma.services.clever-cloud.com/).
2. Ingresá con las credenciales del add-on.
3. Elegí la base → pestaña **Importar** → seleccioná `database/schema_clevercloud.sql` → **Ir**.

**B) Desde la terminal**

```bash
mysql -h "$MYSQL_ADDON_HOST" -P "$MYSQL_ADDON_PORT" \
      -u "$MYSQL_ADDON_USER" -p"$MYSQL_ADDON_PASSWORD" \
      "$MYSQL_ADDON_DB" < database/schema_clevercloud.sql
```

> Usá `database/schema_clevercloud.sql`, **no** `schema.sql`: este último tiene
> `CREATE DATABASE` y `USE`, y Clever Cloud no permite crear bases desde el usuario.

Cuando termine, verificá que existan las 8 tablas: `usuario`, `perfil`, `red_social`,
`experiencia`, `educacion`, `skill`, `idioma`, `proyecto`.

---

## 2. Crear la aplicación Flask

1. En la consola: **Create → An application → Python**.
2. Nombre: `portafolio-ciro`. Región: **la misma del add-on**.
3. Tipo de deploy: **Git**. Clever Cloud te va a mostrar una URL de repositorio remoto.

### 2.1 Linkear la base

En el panel de la app: **Service dependencies → Link add-ons → `portafolio-db`**.
Al linkear, Clever Cloud inyecta automáticamente estas variables:

| Variable inyectada | Para qué sirve |
|---|---|
| `MYSQL_ADDON_HOST` | host de MySQL |
| `MYSQL_ADDON_PORT` | puerto |
| `MYSQL_ADDON_DB` | nombre de la base |
| `MYSQL_ADDON_USER` | usuario |
| `MYSQL_ADDON_PASSWORD` | contraseña |

Nuestro `app/config.py:20` arma la `DATABASE_URL` con esos valores, así que
**no hace falta copiar la contraseña a mano**.

### 2.2 Variables de entorno de la app

En **Environment variables** agregá:

| Variable | Valor | Por qué |
|---|---|---|
| `CC_PYTHON_MODULE` | `run:app` | Le dice a Clever Cloud dónde está el objeto Flask (`app` en `run.py`). |
| `CC_PYTHON_BACKEND` | `gunicorn` | Usa Gunicorn en vez del servidor por defecto. |
| `SECRET_KEY` | el valor generado en el paso 0 | Firma las sesiones y los tokens CSRF. |
| `FLASK_DEBUG` | `0` | Desactiva modo debug en producción (además, la app exige `SECRET_KEY`). |
| `DEMO_URL` | link embebible o vacío | Opcional: el iframe de "Demo en vivo". |

Si querés fijar la versión: `CC_PYTHON_VERSION=3.13` (Clever Cloud soporta 3.9 a 3.14).

### 2.3 Subir el código

```bash
# Pegar la URL que te muestra la consola (cambiar app_xxx por la tuya)
git remote add clever git+ssh://git@push-par-clevercloud-customers.services.clever-cloud.com/app_xxx.git

# Usar el comando exacto que indica el panel. Si tu rama es main y el remoto espera master:
git push clever main:master
```

Clever Cloud instala `requirements.txt`, arranca Gunicorn y redeploya en cada push.
Para ver los logs en vivo:

```bash
clever logs -f portafolio-ciro
```

---

## 3. Verificación en producción

En la URL que te da la consola (`https://portafolio-ciro.cleverapps.io` o tu dominio):

- [ ] Carga el banner, Acerca de, Educación, Skills, Idiomas y Proyectos desde MySQL.
- [ ] Experiencia puede aparecer vacía con su mensaje (si eliminás la fila).
- [ ] El iframe aparece (o el aviso si `DEMO_URL` está vacío).
- [ ] Click en **Login** → usuario `ciro` → el botón pasa a **Logout**.
- [ ] Aparecen lápices, X y **Agregar**; podés editar y recargar para confirmar que persistió.
- [ ] **Descargar CV** baja `CV_Ciro_Gsponer.pdf`.
- [ ] Podés arrastrar dos proyectos y el orden se mantiene al recargar.

---

## 4. Alternativa: app en Render, base en Clever Cloud

Si preferís Render para el sitio:

1. **New → Web Service** desde tu repo de GitHub.
2. Runtime: **Python**. Build: `pip install -r requirements.txt`.
3. Start: `gunicorn run:app` (o dejá que use el `Procfile` que ya está en el repo).
4. Environment variables: `SECRET_KEY`, `FLASK_DEBUG=0`, `DEMO_URL` y **`DATABASE_URL`**.
5. Armá `DATABASE_URL` a mano con los datos del add-on:

```
mysql+mysqlconnector://USUARIO:CLAVE@HOST:PUERTO/NOMBRE_BASE
```

> Si la clave tiene caracteres especiales (`@`, `#`, `/`), codificalos con
> `urllib.parse.quote_plus`. En Clever Cloud eso ya lo hace `config.py` por vos.

---

## 5. Limitación conocida: archivos subidos

Las imágenes y el PDF que se suben desde el modo edición se guardan en
`app/static/uploads/`. En PaaS ese disco suele ser **efímero**: al redesplegar,
los archivos subidos pueden perderse (las imágenes iniciales de `static/img/`
sí sobreviven porque vienen del repositorio).

Es una limitación aceptable para el trabajo práctico y hay que **mencionarla en la defensa**.
Para un sistema real, esos archivos irían a un almacenamiento de objetos (por ejemplo
un bucket S3/Cellar) y en la base se guardaría la URL pública.

---

## 6. Problemas comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `Falta la conexión a MySQL` al arrancar | Add-on no linkeado o variable mal puesta | Linkear el add-on y redeployar. |
| Error 500 en todas las páginas | No se importaron las tablas | Importar `schema_clevercloud.sql` en phpMyAdmin. |
| Login tira 400 Bad Request | `SECRET_KEY` distinta entre workers o inexistente | Definir la misma `SECRET_KEY` y redeployar. |
| CSS/JS 404 | Carpetas `static/` fuera del repo | Verificar `git ls-files app/static`. |
| La página queda "sin estilo" | Cache del navegador | Recarga forzada (Ctrl+F5). |
| No conecta MySQL | App y base en regiones distintas | Crear ambas en la misma región. |
| Logo/perfil no aparecen | Faltan imágenes en el repo | Las de `static/img/` son placeholders; subir las reales. |

---

## Checklist para la defensa

- Sé explicar la diferencia entre `schema.sql` (local) y `schema_clevercloud.sql` (producción).
- Sé decir qué hace `CC_PYTHON_MODULE=run:app` y por qué se usa Gunicorn.
- Sé explicar que las credenciales viven en variables de entorno, nunca en el código.
- Menciono la limitación de los archivos subidos y cómo se resolvería con un bucket.
