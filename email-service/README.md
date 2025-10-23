📧 Email Service

Este servicio se encargará del envío de correos electrónicos y notificaciones automáticas dentro del ecosistema de microservicios.
Su función principal es facilitar la comunicación con los usuarios ante eventos importantes, como registros, publicaciones o recuperación de contraseñas.

⚙️ Funcionalidades principales

✉️ Envío de correos automáticos de confirmación y recuperación de contraseña.

🔔 Notificaciones por nuevas publicaciones o eventos del sistema.

🔄 Integración con otros microservicios a través de colas de mensajes o eventos (usando RabbitMQ o Redis Pub/Sub).

🧰 Tecnologías a utilizar

🐍 Python + Celery para la gestión de tareas asíncronas.

⚡ Redis como broker de tareas.

🌐 Servicio SMTP externo (como Gmail, Mailtrap, o similar) para el envío de correos.
