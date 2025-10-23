🌐 Reverse Proxy

Este componente funcionará como un gateway local encargado de centralizar y enrutar las solicitudes hacia los diferentes microservicios del sistema.
Su propósito es ofrecer un punto de entrada único que gestione de forma eficiente las peticiones HTTP y la distribución del tráfico.

⚙️ Funcionalidades principales

🔀 Redirección de peticiones según el endpoint (/auth, /blog, /email, etc.).

⚖️ Balanceo de carga entre instancias o servicios.

⚙️ Configuración flexible mediante Nginx o Traefik.

💻 Entrega del frontend desde un único punto de acceso (gateway).

🧰 Tecnologías a utilizar

🌐 Nginx (principalmente)

🐳 Docker Compose para la orquestación de los servicios