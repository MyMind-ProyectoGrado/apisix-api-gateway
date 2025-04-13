import os
import yaml
import requests
import time


# Variables de entorno
API_KEY = os.getenv("APISIX_ADMIN_API_KEY", "your-default-key")
APISIX_HOST = os.getenv("APISIX_ADMIN_API", "http://localhost:9180")
ROUTES_FILE = "routes.yaml"
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

# Definición explícita de nombres de variables específicas para el backend de usuarios y modelos
if ENVIRONMENT == "local":
    backend_users_url = os.getenv("BACK_SV_USERS_LOCAL", "http://localhost")
    backend_users_port = os.getenv("BACK_SV_USERS_PORT", "8000")
    backend_models_url = os.getenv("BACK_SV_MODELS_LOCAL", "http://localhost")
    backend_models_port = os.getenv("BACK_SV_MODELS_PORT", "8000")
else:
    backend_users_url = os.getenv("BACK_SV_USERS_PROD", "http://localhost")
    backend_users_port = os.getenv("BACK_SV_USERS_PROD_PORT", "8000")
    backend_models_url = os.getenv("BACK_SV_MODELS_PROD", "http://localhost")
    backend_models_port = os.getenv("BACK_SV_MODELS_PROD_PORT", "8000")

# Derivar los hosts desde las URLs
backend_users_host = backend_users_url.replace("http://", "").replace("https://", "").split("/")[0]
backend_models_host = backend_models_url.replace("http://", "").replace("https://", "").split("/")[0]

# Inyectar explícitamente para que el YAML las reemplace
os.environ["BACK_SV_USERS_HOST"] = backend_users_host
os.environ["BACK_SV_USERS_PORT"] = backend_users_port
os.environ["BACK_SV_MODELS_HOST"] = backend_models_host
os.environ["BACK_SV_MODELS_PORT"] = backend_models_port

# Esperar a que APISIX esté listo
print("⌛ Esperando a que APISIX esté listo...")
for attempt in range(10):
    try:
        res = requests.get(f"{APISIX_HOST}/apisix/admin/routes", headers={"X-API-KEY": API_KEY})
        if res.status_code == 200:
            print("✅ APISIX está listo.")
            break
        else:
            print(f"🔄 Intento {attempt + 1}/10 - Código: {res.status_code}")
    except requests.RequestException as e:
        print(f"🔄 Intento {attempt + 1}/10 - Error: {e}")
    time.sleep(2)
else:
    print("❌ APISIX no respondió a tiempo. Abortando carga de rutas.")
    exit(1)

# Carga y procesa el YAML
with open(ROUTES_FILE, 'r') as f:
    routes = yaml.safe_load(f)

# Sustituye variables de entorno
def substitute_env(value):
    if isinstance(value, str):
        return os.path.expandvars(value)
    elif isinstance(value, dict):
        new_dict = {}
        for k, v in value.items():
            new_key = os.path.expandvars(k) if isinstance(k, str) else k
            new_dict[new_key] = substitute_env(v)
        return new_dict
    elif isinstance(value, list):
        return [substitute_env(i) for i in value]
    else:
        return value

# Enviar rutas a APISIX
print("📦 Enviando rutas a APISIX...")
for i, route in enumerate(routes, start=1):
    route = substitute_env(route)

    url = f"{APISIX_HOST}/apisix/admin/routes/{i}"
    headers = {"X-API-KEY": API_KEY}
    response = requests.put(url, headers=headers, json=route)

    print(f"[{i}] Status: {response.status_code} -> {response.text}")

print("✅ Rutas cargadas correctamente.")