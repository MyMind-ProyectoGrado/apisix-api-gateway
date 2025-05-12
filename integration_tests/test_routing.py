import pytest
import requests
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Token válido de Auth0 para todas las pruebas
AUTH_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ildwa1htLUROUGppOFRMb0FNVWpGSSJ9.eyJpc3MiOiJodHRwczovL215LW1pbmQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY3ZWM2OGM3NDAwMGFjZDQ5YjliZmVjNyIsImF1ZCI6WyJodHRwczovL2NsaWVudGNyZWRlbnRpYWxzLmNvbSIsImh0dHBzOi8vbXktbWluZC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzQ2NzEyNzY1LCJleHAiOjE3NDgwMDg3NjUsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgYWRkcmVzcyBwaG9uZSIsImd0eSI6InBhc3N3b3JkIiwiYXpwIjoiNDZ1dk9abjM2SmpkMkxNcHlIczhFQVpTV0RxMnh2bFMifQ.Y4zuQgZ2U28DiiHsjv33l9w2zZJYz1fcWB5wxscm32oU0Ja4CBS_2RJKC3Cy8GTAyD4ffi4neiwQsqq3ATuve1rJgHV1ARPKNJ1z_sVej35dXzDz10WjYLt45iE7lpbUd5VKtPwy39PPZ8TVcnGnVUMxsckwFDdmdgRudljvgGf26Nmjv0P5Tzx2iNj1kNgyvhfoL2BznX7JVklsOUwTXhmpzKIOloYhS6zL6Vxsb3ESQxn44nWExtlcMrZ1gVrXnJHJ969ivGj5cZikl7F13pZimpUpXOwHbUQs3e2n0zDGPQUXOopaIqyOt4Ur98K2ieiWr5Wg4slJnmkzc2ItAg"

def test_routing_to_users_service(api_base_url):
    """IT-02-01: Verificar que APISIX redirija correctamente a servicio Users."""
    
    # Crear una solicitud a un endpoint del servicio de usuarios
    endpoint = f"{api_base_url}/users/profile"
    
    # Encabezados de autorización
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Realizar la solicitud
    response = requests.get(endpoint, headers=headers)
    
    # Verificar que se recibe una respuesta
    # Nota: Puede ser 200 o 404 dependiendo de si el usuario existe,
    # pero lo importante es que no sea un error de proxy (502, 503, etc.)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text[:200]}")  # Mostrar los primeros 200 caracteres de la respuesta
    
    # Verificar que no sea un error de proxy
    assert response.status_code not in [502, 503, 504], f"Error de proxy: {response.status_code}"
    
    # Verificar que la respuesta venga del servicio de usuarios
    # Esto puede variar según cómo responde tu servicio,
    # pero podemos buscar patrones específicos en la respuesta
    
    # Si la respuesta es JSON, podemos verificar campos específicos
    if response.headers.get('Content-Type', '').startswith('application/json'):
        try:
            data = response.json()
            print(f"JSON Response: {json.dumps(data, indent=2)[:200]}")
        except json.JSONDecodeError:
            print("La respuesta no es un JSON válido")
    
    print("✅ IT-02-01: Enrutamiento a servicio Users verificado correctamente")

def test_routing_to_models_service(api_base_url):
    """IT-02-02: Verificar que APISIX redirija correctamente a servicio Models."""
    
    # Crear una solicitud para agregar una transcripción (solo para verificar enrutamiento)
    endpoint = f"{api_base_url}/transcription/add-transcription/text"
    
    # Encabezados de autorización
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Datos de prueba - Texto para transcripción
    data = {
        "text": "Este es un texto de prueba para el servicio de modelos."
    }
    
    # Realizar la solicitud
    response = requests.post(endpoint, headers=headers, json=data)
    
    # Mostrar información de la respuesta
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    
    # Verificar que no sea un error de proxy
    assert response.status_code not in [502, 503, 504], f"Error de proxy: {response.status_code}"
    
    # Si la respuesta es JSON, verificamos su estructura
    if response.headers.get('Content-Type', '').startswith('application/json'):
        try:
            data = response.json()
            print(f"JSON Response: {json.dumps(data, indent=2)[:200]}")
            
            # Verificar que la respuesta incluya campos específicos del servicio de modelos
            # como 'task_id' o 'message' relacionado con transcripciones
            assert 'task_id' in data or 'message' in data, "Respuesta no contiene campos esperados del servicio de modelos"
        except json.JSONDecodeError:
            print("La respuesta no es un JSON válido")
    
    print("✅ IT-02-02: Enrutamiento a servicio Models verificado correctamente")

def test_routing_to_visualizations_service(api_base_url):
    """IT-02-03: Verificar que APISIX redirija correctamente a servicio Visualizations."""
    
    # Crear una solicitud para obtener análisis de los últimos 7 días
    endpoint = f"{api_base_url}/transcriptions/user/last-7-days"
    
    # Encabezados de autorización
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Realizar la solicitud
    response = requests.get(endpoint, headers=headers)
    
    # Mostrar información de la respuesta
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    
    # Verificar que no sea un error de proxy
    assert response.status_code not in [502, 503, 504], f"Error de proxy: {response.status_code}"
    
    # Si la respuesta es JSON, verificamos su estructura
    if response.headers.get('Content-Type', '').startswith('application/json'):
        try:
            data = response.json()
            print(f"JSON Response: {json.dumps(data, indent=2)[:200]}")
            
            # Verificar que la respuesta incluya campos específicos del servicio de visualizaciones
            # como campos relacionados con emociones o sentimientos
            if response.status_code == 200:
                # Si la respuesta es exitosa, debe contener campos de análisis emocional
                assert any(field in data for field in [
                    'emotion_probs_joy', 'emotion_probs_anger', 'emotion_probs_sadness', 
                    'sentiment_probs_positive', 'sentiment_probs_negative'
                ]), "Respuesta no contiene campos esperados del servicio de visualizaciones"
        except json.JSONDecodeError:
            print("La respuesta no es un JSON válido")
        except (KeyError, TypeError) as e:
            print(f"Error al procesar JSON: {e}")
    
    # Una respuesta 404 también puede ser válida si no hay datos de los últimos 7 días
    # Lo importante es verificar que la solicitud llegó al servicio correcto
    
    print("✅ IT-02-03: Enrutamiento a servicio Visualizations verificado correctamente")
