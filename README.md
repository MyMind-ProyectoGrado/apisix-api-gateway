# Gateway API con APISIX y Auth0 y Monitoreo

Este proyecto implementa un **API Gateway** con **Apache APISIX**, autenticación con **Auth0**, y múltiples servicios backend dockerizados. Todas las rutas están protegidas con `openid-connect` y definidas dinámicamente mediante un script en Python.

## ⚙️ Requisitos

- Docker + Docker Compose  
- Python 3.8+  
- Archivo `.env` con las variables necesarias (Auth0 y hosts de los servicios backend)

## 🏗️ Estructura

```
.
apisix-api-gateway/
├── apisix_conf/
├── dashboard_conf/
├── etcd_conf/
├── grafana_conf/
├── prometheus_conf/
├── .env
├── .gitignore
├── docker-compose.yml
├── load_routes.py
├── README.md
└── routes.yaml

```

## 🚀 Cómo usar

1. Configura tu `.env` con variables como `AUTH0_CLIENT_ID`, `BACK_SV_USERS_HOST`, `Rutas métricas`, etc.
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


