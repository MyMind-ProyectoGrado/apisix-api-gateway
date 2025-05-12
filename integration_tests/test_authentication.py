import pytest
import requests
import time
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_access_without_token(api_base_url):
    """IT-01-01: Verificar que el acceso sin token sea denegado."""
    # Intentar acceder a una ruta protegida sin token
    endpoint = f"{api_base_url}/users/profile"
    response = requests.get(endpoint)
    
    # Verificar que se recibe error de autenticación
    assert response.status_code in [401, 403], f"Expected 401/403, got {response.status_code}"
    print(f"✅ IT-01-01: Acceso sin token denegado correctamente con código {response.status_code}")

def test_access_with_invalid_token(api_base_url, generate_invalid_token):
    """IT-01-02: Verificar que el acceso con token inválido sea denegado."""
    # Obtener un token inválido
    invalid_token = generate_invalid_token()
    
    # Intentar acceder a una ruta protegida con token inválido
    endpoint = f"{api_base_url}/users/profile"
    headers = {"Authorization": f"Bearer {invalid_token}"}
    response = requests.get(endpoint, headers=headers)
    
    # Verificar que se recibe error de autenticación
    assert response.status_code in [401, 403], f"Expected 401/403, got {response.status_code}"
    print(f"✅ IT-01-02: Acceso con token inválido denegado correctamente con código {response.status_code}")

def test_access_with_valid_token(api_base_url):
    """IT-01-03: Verificar que el acceso con token válido sea permitido."""
    # Usar el token real de Auth0 proporcionado
    valid_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ildwa1htLUROUGppOFRMb0FNVWpGSSJ9.eyJpc3MiOiJodHRwczovL215LW1pbmQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY3ZWM2OGM3NDAwMGFjZDQ5YjliZmVjNyIsImF1ZCI6WyJodHRwczovL2NsaWVudGNyZWRlbnRpYWxzLmNvbSIsImh0dHBzOi8vbXktbWluZC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzQ2NzEyNzY1LCJleHAiOjE3NDgwMDg3NjUsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgYWRkcmVzcyBwaG9uZSIsImd0eSI6InBhc3N3b3JkIiwiYXpwIjoiNDZ1dk9abjM2SmpkMkxNcHlIczhFQVpTV0RxMnh2bFMifQ.Y4zuQgZ2U28DiiHsjv33l9w2zZJYz1fcWB5wxscm32oU0Ja4CBS_2RJKC3Cy8GTAyD4ffi4neiwQsqq3ATuve1rJgHV1ARPKNJ1z_sVej35dXzDz10WjYLt45iE7lpbUd5VKtPwy39PPZ8TVcnGnVUMxsckwFDdmdgRudljvgGf26Nmjv0P5Tzx2iNj1kNgyvhfoL2BznX7JVklsOUwTXhmpzKIOloYhS6zL6Vxsb3ESQxn44nWExtlcMrZ1gVrXnJHJ969ivGj5cZikl7F13pZimpUpXOwHbUQs3e2n0zDGPQUXOopaIqyOt4Ur98K2ieiWr5Wg4slJnmkzc2ItAg"
    
    # Intentar acceder a una ruta protegida con token válido
    endpoint = f"{api_base_url}/users/profile"
    headers = {"Authorization": f"Bearer {valid_token}"}
    
    try:
        response = requests.get(endpoint, headers=headers)
        
        # Verificar que se permite el acceso (no sea 401/403)
        # Nota: Aceptamos 200 (OK) o 404 (Not Found) como casos válidos
        # ya que depende de si el usuario existe en la base de datos
        assert response.status_code not in [401, 403], f"Expected success, got {response.status_code}"
        print(f"✅ IT-01-03: Acceso con token válido permitido correctamente con código {response.status_code}")
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        # Para depuración, veamos el contenido de la respuesta
        if 'response' in locals():
            print(f"Respuesta: {response.text}")
        raise
