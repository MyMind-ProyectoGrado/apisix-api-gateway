import os
import pytest
import requests
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración para las pruebas
@pytest.fixture(scope="session")
def api_base_url():
    """URL base de APISIX para pruebas."""
    # Puerto donde APISIX está escuchando
    return "http://localhost:9080"  # Ajustar si es diferente

@pytest.fixture(scope="session")
def auth0_config():
    """Configuración de Auth0."""
    return {
        "client_id": os.getenv("AUTH0_CLIENT_ID"),
        "client_secret": os.getenv("AUTH0_CLIENT_SECRET"),
        "discovery_url": os.getenv("AUTH0_DISCOVERY_URL")
    }

@pytest.fixture
def generate_valid_token():
    """Genera un token JWT válido simulando Auth0."""
    def _generate_token(user_id="test_user_123"):
        # Simular un token JWT simple
        # En producción, este token vendría de Auth0
        payload = {
            "sub": user_id,  # Subject (identificador del usuario)
            "iss": "https://my-mind.us.auth0.com/",  # Issuer
            "aud": os.getenv("AUTH0_CLIENT_ID"),  # Audience
            "iat": datetime.now(timezone.utc),  # Issued At
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)  # Expiration
        }
        
        # En pruebas reales usaríamos un secreto adecuado
        # Aquí usamos un valor arbitrario para firmar el token
        token = jwt.encode(payload, "test_secret", algorithm="HS256")
        return token
    
    return _generate_token

@pytest.fixture
def generate_invalid_token():
    """Genera un token JWT inválido."""
    def _generate_invalid_token():
        # Token con formato incorrecto
        return "invalid.token.format"
    
    return _generate_invalid_token
