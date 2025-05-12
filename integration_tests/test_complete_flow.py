import pytest
import requests
import json
import time
import os
import uuid
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Token válido de Auth0 para todas las pruebas
AUTH_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ildwa1htLUROUGppOFRMb0FNVWpGSSJ9.eyJpc3MiOiJodHRwczovL215LW1pbmQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY3ZWM2OGM3NDAwMGFjZDQ5YjliZmVjNyIsImF1ZCI6WyJodHRwczovL2NsaWVudGNyZWRlbnRpYWxzLmNvbSIsImh0dHBzOi8vbXktbWluZC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzQ2NzEyNzY1LCJleHAiOjE3NDgwMDg3NjUsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgYWRkcmVzcyBwaG9uZSIsImd0eSI6InBhc3N3b3JkIiwiYXpwIjoiNDZ1dk9abjM2SmpkMkxNcHlIczhFQVpTV0RxMnh2bFMifQ.Y4zuQgZ2U28DiiHsjv33l9w2zZJYz1fcWB5wxscm32oU0Ja4CBS_2RJKC3Cy8GTAyD4ffi4neiwQsqq3ATuve1rJgHV1ARPKNJ1z_sVej35dXzDz10WjYLt45iE7lpbUd5VKtPwy39PPZ8TVcnGnVUMxsckwFDdmdgRudljvgGf26Nmjv0P5Tzx2iNj1kNgyvhfoL2BznX7JVklsOUwTXhmpzKIOloYhS6zL6Vxsb3ESQxn44nWExtlcMrZ1gVrXnJHJ969ivGj5cZikl7F13pZimpUpXOwHbUQs3e2n0zDGPQUXOopaIqyOt4Ur98K2ieiWr5Wg4slJnmkzc2ItAg"

def test_register_new_user(api_base_url):
    """IT-03-01: Verificar el registro de un nuevo usuario."""
    
    # Endpoint para registro de usuario
    endpoint = f"{api_base_url}/users/register"
    
    # Encabezados con token de autenticación
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Generar un nombre único para evitar conflictos en pruebas repetidas
    unique_id = str(uuid.uuid4())[:8]
    
    # Datos de usuario de prueba
    user_data = {
        "name": f"Test User {unique_id}",
        "email": f"test{unique_id}@example.com",
        "profilePic": "https://example.com/pic.jpg",
        "birthdate": "1990-01-01",
        "city": "Test City",
        "personality": "Introvertido",
        "university": "Test University",
        "degree": "Test Degree",
        "gender": "Masculino",
        "notifications": True,
        "data_treatment": {
            "accept_policies": True,
            "acceptance_date": "2025-05-01T12:00:00",
            "acceptance_ip": "192.168.1.1",
            "privacy_preferences": {
                "allow_anonimized_usage": True
            }
        }
    }
    
    # Realizar la solicitud
    try:
        response = requests.post(endpoint, headers=headers, json=user_data, timeout=10)
        
        # Mostrar información de la respuesta
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
        # Verificar la respuesta
        # Podría ser 200 (exitoso) o 409 (conflicto si el usuario ya existe)
        assert response.status_code in [200, 201, 409], f"Registro fallido con código: {response.status_code}"
        
        print("✅ IT-03-01: Registro de usuario verificado correctamente")
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        assert False, f"La prueba falló con el error: {str(e)}"

def test_text_transcription_processing(api_base_url):
    """IT-03-02: Verificar el procesamiento de una transcripción de texto."""
    
    # Endpoint para enviar texto para transcripción
    endpoint = f"{api_base_url}/transcription/add-transcription/text"
    
    # Encabezados con token de autenticación
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Texto de prueba con emociones claras
    text_data = {
        "text": "Hoy me siento muy contento con todo lo que he logrado. Estoy orgulloso de mi trabajo."
    }
    
    # Realizar la solicitud
    try:
        response = requests.post(endpoint, headers=headers, json=text_data, timeout=10)
        
        # Mostrar información de la respuesta
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
        # Verificar la respuesta
        assert response.status_code in [200, 201, 202], f"Procesamiento de texto fallido con código: {response.status_code}"
        
        # Verificar que la respuesta contiene los campos esperados
        data = response.json()
        assert "task_id" in data, "Respuesta no contiene task_id"
        task_id = data["task_id"]
        
        # Esperar a que se procese la transcripción (podría tomar tiempo)
        print(f"Esperando procesamiento del task_id: {task_id}")
        
        # Verificar resultado usando la API de stream
        stream_endpoint = f"{api_base_url}/transcription/stream/{task_id}"
        
        # Intentar obtener resultado durante un máximo de 30 segundos
        max_attempts = 6  # 6 intentos con 5 segundos entre cada uno = 30 segundos máximo
        stream_response = None
        for attempt in range(max_attempts):
            try:
                stream_response = requests.get(stream_endpoint, headers=headers, timeout=10)
                
                # Si ya tenemos un resultado exitoso, salimos del bucle
                if stream_response.status_code == 200:
                    break
                    
                print(f"Intento {attempt+1}/{max_attempts} - Status: {stream_response.status_code}")
                time.sleep(5)  # Esperar 5 segundos antes del siguiente intento
            except Exception as e:
                print(f"Error en el intento {attempt+1}: {str(e)}")
                time.sleep(5)
        
        # Verificar el resultado final
        assert stream_response is not None, "No se pudo obtener ninguna respuesta del endpoint de stream"
        assert stream_response.status_code == 200, f"No se pudo obtener el resultado de la transcripción: {stream_response.status_code}"
        
        # Verificar que el resultado contiene los campos de análisis esperados
        result_data = stream_response.json()
        assert "result" in result_data, "Respuesta no contiene campo 'result'"
        
        transcription = result_data["result"]
        assert "emotion" in transcription, "Transcripción no contiene campo 'emotion'"
        assert "sentiment" in transcription, "Transcripción no contiene campo 'sentiment'"
        assert "emotionProbabilities" in transcription, "Transcripción no contiene campo 'emotionProbabilities'"
        assert "sentimentProbabilities" in transcription, "Transcripción no contiene campo 'sentimentProbabilities'"
        
        print(f"Emoción detectada: {transcription['emotion']}")
        print(f"Sentimiento detectado: {transcription['sentiment']}")
        
        print("✅ IT-03-02: Procesamiento de texto verificado correctamente")
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        assert False, f"La prueba falló con el error: {str(e)}"

def test_audio_upload_simulation(api_base_url):
    """IT-03-03: Simular la subida de audio para transcripción (simulación básica)."""
    
    # Nota: Esta prueba es una simulación básica ya que no tenemos un archivo de audio real
    # En un entorno real, se usaría un archivo de audio pregrabado
    
    # Endpoint para subir audio
    endpoint = f"{api_base_url}/transcription/add-transcription/audio"
    
    # Encabezados con token de autenticación - sin Content-Type para permitir multipart/form-data
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }
    
    # Realizar la solicitud simulada - solo verificamos que la ruta exista
    # No enviamos archivo real para evitar procesamiento innecesario en este test
    try:
        # Solo verificamos que el endpoint exista, no enviamos archivo real
        # Esto generará un error 400 o 422 (Bad Request/Unprocessable Entity) ya que falta el archivo,
        # pero nos dirá si el endpoint está disponible
        response = requests.post(endpoint, headers=headers, timeout=5)
        
        # Mostrar información de la respuesta
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
        # Verificar que el endpoint existe (400, 422 por falta de archivo, o cualquier otro código excepto 404 o 5xx)
        assert response.status_code not in [404, 502, 503, 504], f"El endpoint de audio no está disponible: {response.status_code}"
        
        print("✅ IT-03-03: Endpoint de subida de audio verificado correctamente")
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        assert False, f"La prueba falló con el error: {str(e)}"

def test_retrieve_processed_transcriptions(api_base_url):
    """IT-03-04: Verificar que se pueden recuperar las transcripciones procesadas."""
    
    # Endpoint para obtener transcripciones del usuario
    endpoint = f"{api_base_url}/users/transcriptions/"
    
    # Encabezados con token de autenticación
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Realizar la solicitud
    try:
        response = requests.get(endpoint, headers=headers, timeout=10)
        
        # Mostrar información de la respuesta
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
        # Verificar la respuesta
        assert response.status_code == 200, f"Obtención de transcripciones fallida con código: {response.status_code}"
        
        # Verificar que la respuesta es una lista (puede estar vacía si el usuario no tiene transcripciones)
        data = response.json()
        assert isinstance(data, list), "La respuesta no es una lista"
        
        print(f"Se encontraron {len(data)} transcripciones")
        
        print("✅ IT-03-04: Obtención de transcripciones verificada correctamente")
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        assert False, f"La prueba falló con el error: {str(e)}"
