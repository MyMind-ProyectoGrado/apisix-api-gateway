# Gateway API con APISIX y Auth0 y Monitoreo

Este proyecto implementa un **API Gateway** con **Apache APISIX**, autenticación con **Auth0**, y múltiples servicios backend dockerizados. Todas las rutas están protegidas con `openid-connect` y definidas dinámicamente mediante un script en Python.

## ⚙️ Requisitos

- Docker + Docker Compose  
- Python 3.8+  
- Archivo `.env` con las variables necesarias (Auth0 y hosts de los servicios backend)

## 🏗️ Estructura

```
.
├── app/
│   ├── core/
│   │   ├── auth.py                 # Lógica de autenticación y autorización
│   │   └── database.py             # Conexión a la base de datos MongoDB
│   ├── routes/
│   │   ├── audio.py                # Ruta para procesar audio
│   │   ├── transcriptions.py       # Rutas para agregar y consultar transcripciones
│   │   └── users.py                # Rutas para manejo de usuarios
│   ├── schemas/
│   │   ├── transcription_schema.py # Esquema Pydantic para transcripciones
│   │   └── user_schema.py          # Esquema Pydantic para usuarios
│   └── tests/                      # Pruebas unitarias
├── main.py                         # Punto de entrada de la aplicación FastAPI
├── .env                            # Variables de entorno (puertos, Mongo, Auth0, etc.)
├── .gitignore                      # Archivos a ignorar por Git
├── docker-compose.yml              # Orquestación de contenedores (FastAPI, Mongo, etc.)
├── Dockerfile                      # Imagen para el backend FastAPI
├── README.md                       # Documentación del servicio
├── requirements.txt                # Dependencias del backend
```

## 🚀 Cómo usar

1. Configura tu `.env` con variables como `AUTH0_CLIENT_ID`, `BACK_SV_USERS_HOST`, etc.
2. Levanta los servicios:

```bash
docker-compose up -d
```

3. Accede al APISIX Dashboard en navegador:
```bash
http://localhost:9000
```

## 📌 Notas

- Las rutas usan `openid-connect` para autenticación.
- El archivo `routes.yaml` ya incluye upstreams dinámicos usando variables del `.env`.

---


