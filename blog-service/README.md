Perfecto, Alex 💪
Basado en tu estructura real (la de la imagen), te dejo el **README completo y mejorado en formato Markdown**, con una arquitectura actualizada y bien documentada — ideal para tu repositorio `microservices-lab`.

---

```markdown
# 📰 Blog Service — Microservicio Django + DRF + PostgreSQL + Redis

## 📘 Descripción General
**Blog Service** es un microservicio independiente desarrollado con **Django REST Framework (DRF)** y desplegado con **Docker**, que forma parte del entorno `microservices-lab`.  

Su objetivo es exponer una API REST para gestionar publicaciones (**posts**), categorías (**categories**) y autores (**authors**) con:
- Paginación y búsqueda.
- Caché en Redis (TTL 60s).
- Endpoint `/healthz` para verificación de estado.
- Logging estructurado en formato JSON.
- Script `seed_blog` para generar datos de ejemplo.

> 💡 Este servicio está preparado para integrarse con el `Auth Service` mediante JWT (en futuras etapas).

---

## ⚙️ Stack Tecnológico
- **Python 3.11**
- **Django 5**
- **Django REST Framework 3.15**
- **PostgreSQL 15**
- **Redis 7**
- **Gunicorn**
- **Docker + Docker Compose**

---

## 📂 Arquitectura del Proyecto

```

microservices-lab/
│
├── auth-service/
│
├── blog-service/
│   ├── Dockerfile
│   ├── openapi.yaml
│   ├── requirements.txt
│   ├── README.md
│   └── app/
│       ├── manage.py
│       │
│       ├── blog_service/          # Configuración principal del proyecto Django
│       │   ├── **init**.py
│       │   ├── settings.py
│       │   ├── urls.py
│       │   └── wsgi.py
│       │
│       ├── core/                  # Utilidades globales
│       │   ├── **init**.py
│       │   ├── pagination.py      # Configura paginación DRF
│       │   ├── middleware.py      # Logging JSON y lectura del header Authorization
│       │   └── health.py          # Endpoint /healthz
│       │
│       ├── authors/               # Gestión de autores
│       │   ├── **init**.py
│       │   ├── apps.py
│       │   ├── models.py
│       │   ├── serializers.py
│       │   ├── views.py
│       │   └── urls.py
│       │
│       ├── categories/            # Gestión de categorías
│       │   ├── **init**.py
│       │   ├── apps.py
│       │   ├── models.py
│       │   ├── serializers.py
│       │   ├── views.py
│       │   └── urls.py
│       │
│       └── posts/                 # Gestión de publicaciones
│           ├── **init**.py
│           ├── apps.py
│           ├── models.py
│           ├── serializers.py
│           ├── views.py
│           ├── urls.py
│           ├── tests.py
│           ├── migrations/
│           └── management/         # Comandos personalizados
│               └── commands/
│                   └── seed_blog.py      #Script para poblar la DB con datos de ejemplo
│
├── docker-compose.yml
│
├── reverse-proxy/
├── email-service/
├── frontend/
│
└── .env.example

````

---

## 🔧 Configuración del Servicio

### Variables de Entorno
Definidas en el `docker-compose.yml`:
```yaml
services:
  blog:
    build: ./blog-service
    container_name: blog_service
    environment:
      - DB_HOST=postgres
      - DB_NAME=main_db
      - DB_USER=devuser
      - DB_PASS=devpass
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - DEBUG=1
    depends_on:
      - postgres
      - redis
    ports:
      - "8001:8001"
````

---

## 🐳 Dockerfile

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

ENV DJANGO_SETTINGS_MODULE=blog_service.settings
EXPOSE 8001

CMD ["gunicorn", "blog_service.wsgi:application", "--bind", "0.0.0.0:8001"]
```

---

## 🧱 Modelos Principales

### 🏷 Category

| Campo     | Tipo         | Descripción                                  |
| --------- | ------------ | -------------------------------------------- |
| name      | CharField    | Nombre de la categoría                       |
| slug      | SlugField    | Identificador único generado automáticamente |
| is_active | BooleanField | Control de visibilidad                       |

### ✍️ Author

| Campo        | Tipo       | Descripción              |
| ------------ | ---------- | ------------------------ |
| display_name | CharField  | Nombre visible del autor |
| email        | EmailField | Correo electrónico único |

### 📰 Post

| Campo        | Tipo                  | Descripción              |
| ------------ | --------------------- | ------------------------ |
| title        | CharField             | Título del post          |
| slug         | SlugField             | Generado automáticamente |
| body         | TextField             | Contenido principal      |
| author       | ForeignKey → Author   | Autor                    |
| category     | ForeignKey → Category | Categoría                |
| status       | CharField             | `draft` o `published`    |
| published_at | DateTimeField         | Fecha de publicación     |
| views        | PositiveIntegerField  | Conteo de vistas         |

---

## 🌱 Seed de Datos

Script: `posts/management/commands/seed_blog.py`
Crea datos iniciales de prueba:

* 5 categorías
* 3 autores
* 30 posts

### 🔧 Ejecución dentro del contenedor

```bash
docker exec -it blog_service bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_blog
```

O de una sola línea:

```bash
docker exec -it blog_service bash -lc "python manage.py makemigrations && python manage.py migrate && python manage.py seed_blog"
```

---

## 🌐 Endpoints API

| Método | Endpoint          | Descripción                                        |                                |
| ------ | ----------------- | -------------------------------------------------- | ------------------------------ |
| `GET`  | `/api/categories` | Lista categorías activas (cacheadas 60s)           |                                |
| `GET`  | `/api/posts`      | Lista posts con paginación y búsqueda (`?search=`) |                                |
| `GET`  | `/api/posts/{id   | slug}`                                             | Detalle de post (cacheado 60s) |
| `GET`  | `/healthz`        | Verifica conexión a DB y Redis                     |                                |

### Ejemplos

```bash
curl -s http://localhost:8001/api/categories | jq
curl -s "http://localhost:8001/api/posts?page=1&search=Django" | jq
curl -s http://localhost:8001/api/posts/1/ | jq
curl -s http://localhost:8001/healthz | jq
```

---

## 🧠 Paginación, Búsqueda y Caché

**Paginación:**
Configurada en `core/pagination.py` con `PAGE_SIZE=10`.

**Búsqueda:**
Habilitada sobre los campos `title` y `body` usando `SearchFilter`.

**Caché:**
Usa `django-redis` con TTL de **60s** en:

* `/api/categories`
* `/api/posts/{id|slug}`

---

## 🩺 Healthcheck

Ruta:

```
GET /healthz
```

Respuesta:

```json
{
  "db": "ok",
  "redis": "ok",
  "elapsed_ms": 12
}
```

---

## 🧾 Logging JSON

Middleware: `core/middleware.py`
Ejemplo de log por request:

```json
{
  "method": "GET",
  "path": "/api/posts?page=1",
  "status": 200,
  "elapsed_ms": 47,
  "auth_header_present": false
}
```

---

## 📄 Contrato OpenAPI

Archivo: `openapi.yaml`

Incluye documentación mínima para los endpoints:

* `/api/categories`
* `/api/posts`
* `/api/posts/{id|slug}`

Listo para que el **Frontend** consuma el contrato.

---

## ✅ Verificación Final

```bash
docker ps
curl http://localhost:8001/healthz
```

Salida esperada:

```json
{"db":"ok","redis":"ok","elapsed_ms":15}
```

---

## 🏁 Resultado Final

✅ Microservicio funcional en `http://localhost:8001/`
✅ Endpoints con búsqueda, paginación y caché
✅ Conexión estable a PostgreSQL y Redis
✅ Datos de ejemplo cargados
✅ Logging JSON y healthcheck operativo

---

## 📦 Comando rápido para regenerar todo

```bash
docker exec -it blog_service bash -lc "python manage.py makemigrations && python manage.py migrate && python manage.py seed_blog"
```

---

💡 **Autor:** *Alexander Cárdenas Alhuay*
🎓 *SENATI – Proyecto Microservicios Día 3: Blog Service*

```

---

¿Quieres que te genere también la **versión README.md con formato visual mejorado para GitHub** (con emojis, badges y secciones destacadas)? Puedo hacerlo con estilos de presentación profesional.
```

