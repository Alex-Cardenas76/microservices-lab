# 📧 Email Service

Microservicio independiente encargado de **recibir mensajes y enviar notificaciones por correo**, funcionando de manera separada pero comunicándose con los otros microservicios (Auth y Blog).

## 💡 ¿Qué problema resuelve?

Este servicio centraliza el manejo de todas las comunicaciones por email del ecosistema:
- Formularios de contacto desde el frontend
- Notificaciones entre microservicios
- Alertas automáticas del sistema
- Historial y trazabilidad de mensajes enviados

## 🎯 Funcionalidades

✅ **Implementadas:**
- Recibir solicitudes de envío de mensajes desde frontend u otros microservicios
- Guardar cada mensaje en la base de datos para trazabilidad
- Mostrar notificaciones por consola (modo desarrollo)
- Comunicación entre microservicios via API REST

🔄 **Futuras:**
- Envío real de correos via SMTP
- Integración con Celery + Redis para tareas en segundo plano
- Templates de email personalizables

## 🛠 Tecnologías

- **Backend:** Django + Django REST Framework
- **Base de datos:** PostgreSQL (compartida con otros servicios)
- **Cache:** Redis (compartido con otros servicios)
- **Contenedor:** Docker

## 🏗 Arquitectura

```
Frontend/Otros Servicios
         ↓
    Email Service API
         ↓
   PostgreSQL (logs)
         ↓
    Consola (desarrollo)
```

## 🚀 Instalación y Uso

### 1. Levantar el servicio
```bash
# Construir y levantar solo email-service
docker-compose up --build email

# O levantar todos los servicios
docker-compose up --build
```

### 2. Ejecutar migraciones
```bash
docker-compose exec email python manage.py makemigrations
docker-compose exec email python manage.py migrate
```

### 3. Crear superusuario (opcional)
```bash
docker-compose exec email python manage.py createsuperuser
```

## 📡 API Endpoints

### 🔗 Base URL
```
http://localhost:8003/api/
```

### 1️⃣ Formulario de Contacto (Público)

**Endpoint:** `POST /api/contact/`

**Descripción:** Endpoint público para recibir mensajes de contacto desde el frontend

**Request Body:**
```json
{
  "name": "Carlos",
  "email": "carlos@mail.com", 
  "message": "Me interesa una colaboración"
}
```

**Response:**
```json
{
  "status": "queued"
}
```

### 2️⃣ Notificación entre Servicios (Interno)

**Endpoint:** `POST /api/notify/`

**Descripción:** Endpoint interno para comunicación entre microservicios

**Request Body:**
```json
{
  "to": "usuario@mail.com",
  "subject": "Nuevo Post Publicado", 
  "body": "Se ha publicado un nuevo post: 'Título del post'"
}
```

**Response:**
```json
{
  "status": "queued"
}
```

## 🧪 Pruebas con Postman

### Colección de Postman

#### 1. Mensaje de Contacto
```
Method: POST
URL: http://localhost:8003/api/contact/
Headers: 
  Content-Type: application/json
Body (raw JSON):
{
  "name": "Juan Pérez",
  "email": "juan@ejemplo.com",
  "message": "Hola, me gustaría obtener más información sobre sus servicios."
}
```

#### 2. Notificación Interna
```
Method: POST  
URL: http://localhost:8003/api/notify/
Headers:
  Content-Type: application/json
Body (raw JSON):
{
  "to": "admin@miapp.com",
  "subject": "Nuevo usuario registrado",
  "body": "Un nuevo usuario se ha registrado en la plataforma: juan@ejemplo.com"
}
```

#### 3. Listar Mensajes de Contacto
```
Method: GET
URL: http://localhost:8003/api/contact/
```

## 📊 Modelos de Base de Datos

### ContactMessage
- `name`: CharField(150) - Nombre del remitente
- `email`: EmailField - Email del remitente  
- `message`: TextField - Contenido del mensaje
- `created_at`: DateTimeField - Fecha de creación

### NotificationLog  
- `to`: EmailField - Destinatario
- `subject`: CharField(200) - Asunto del mensaje
- `body`: TextField - Contenido del mensaje
- `created_at`: DateTimeField - Fecha de creación

## 🔧 Configuración

### Variables de Entorno
```env
# Base de datos (compartida)
DB_NAME=main_db
DB_USER=devuser  
DB_PASSWORD=devpass
DB_HOST=postgres
DB_PORT=5432

# Redis (compartido)
REDIS_HOST=redis
REDIS_PORT=6379

# Django
DEBUG=1
SECRET_KEY=tu-clave-secreta
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Puertos
- **Email Service:** `8003:8000`
- **PostgreSQL:** `5432:5432` 
- **Redis:** `6379:6379`

## 📝 Logs de Desarrollo

En modo desarrollo, los mensajes se muestran por consola:

```
📧 Nuevo mensaje de contacto:
   De: Juan Pérez (juan@ejemplo.com)
   Mensaje: Hola, me gustaría obtener más información...

🔔 Nueva notificación:
   Para: admin@miapp.com
   Asunto: Nuevo usuario registrado
   Mensaje: Un nuevo usuario se ha registrado...
```

## 🔄 Integración con otros Servicios

### Desde Blog Service
```python
import requests

# Notificar nuevo post
response = requests.post('http://email:8000/api/notify/', json={
    'to': 'suscriptor@mail.com',
    'subject': 'Nuevo Post: Mi Artículo',
    'body': 'Se ha publicado un nuevo artículo que te puede interesar...'
})
```

### Desde Auth Service  
```python
import requests

# Notificar nuevo registro
response = requests.post('http://email:8000/api/notify/', json={
    'to': 'admin@miapp.com', 
    'subject': 'Nuevo Usuario Registrado',
    'body': f'Usuario {username} se ha registrado exitosamente'
})
```

## 🐳 Docker

El servicio está completamente dockerizado y se integra con la infraestructura existente:

- Comparte la base de datos PostgreSQL con Auth y Blog services
- Utiliza el mismo Redis para cache
- Se comunica internamente via red Docker
- Puerto expuesto: 8003

## 📋 TODO / Próximas Mejoras

- [ ] Implementar envío real de emails via SMTP
- [ ] Agregar Celery para tareas asíncronas  
- [ ] Templates HTML para emails
- [ ] Validaciones adicionales
- [ ] Tests unitarios
- [ ] Autenticación para endpoint /notify/
- [ ] Rate limiting
- [ ] Métricas y monitoreo
