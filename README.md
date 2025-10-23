# 🧪 **Laboratorio de Microservicios (Django + React)**

Este proyecto sirve como un entorno práctico para **aprender microservicios**, integrando **Django** en el backend, **React** en el frontend y **Docker Compose** para la orquestación de los servicios.

---

## ⚙️ **Arquitectura general**

### 🧩 **Servicios principales**

* 🔐 **auth-service/** → Maneja la **autenticación de usuarios**, registro, inicio de sesión y generación de **tokens JWT**.
* 📝 **blog-service/** → Controla las **publicaciones**, **autores** y **categorías** del blog.
* ✉️ **email-service/** → Se encarga del **envío de correos electrónicos** y **notificaciones**.
* 💻 **frontend/** → Interfaz creada con **React**, que consume los endpoints de los microservicios.
* 🌐 **reverse-proxy/** → Actúa como **gateway local** (Nginx o Traefik) para enrutar las peticiones a los servicios correspondientes.

### 🧱 **Servicios base (Docker Compose)**

* 🐘 **PostgreSQL** → Base de datos principal (puerto `5432`).
* ⚡ **Redis** → Sistema de **cache** y **colas de mensajes** (puerto `6379`).

---

## 📂 **Estructura del proyecto**

```
microservices-lab/
│
├── auth-service/
├── blog-service/
├── email-service/
├── frontend/
├── reverse-proxy/
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 **Inicio del entorno base**

Ejecuta los siguientes comandos para levantar los servicios principales:

```bash
docker compose up -d
docker ps
```

✅ Si ves los contenedores **db_postgres** y **cache_redis** en ejecución, ¡el entorno base está listo para usarse!