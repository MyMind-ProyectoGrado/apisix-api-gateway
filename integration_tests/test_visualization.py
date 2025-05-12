import pytest
import requests
import json
import time
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Token válido de Auth0 para todas las pruebas
AUTH_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ildwa1htLUROUGppOFRMb0FNVWpGSSJ9.eyJpc3MiOiJodHRwczovL215LW1pbmQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY3ZWM2OGM3NDAwMGFjZDQ5YjliZmVjNyIsImF1ZCI6WyJodHRwczovL2NsaWVudGNyZWRlbnRpYWxzLmNvbSIsImh0dHBzOi8vbXktbWluZC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzQ2NzEyNzY1LCJleHAiOjE3NDgwMDg3NjUsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgYWRkcmVzcyBwaG9uZSIsImd0eSI6InBhc3N3b3JkIiwiYXpwIjoiNDZ1dk9abjM2SmpkMkxNcHlIczhFQVpTV0RxMnh2bFMifQ.Y4zuQgZ2U28DiiHsjv33l9w2zZJYz1fcWB5wxscm32oU0Ja4CBS_2RJKC3Cy8GTAyD4ffi4neiwQsqq3ATuve1rJgHV1ARPKNJ1z_sVej35dXzDz10WjYLt45iE7lpbUd5VKtPwy39PPZ8TVcnGnVUMxsckwFDdmdgRudljvgGf26Nmjv0P5Tzx2iNj1kNgyvhfoL2BznX7JVklsOUwTXhmpzKIOloYhS6zL6Vxsb3ESQxn44nWExtlcMrZ1gVrXnJHJ969ivGj5cZikl7F13pZimpUpXOwHbUQs3e2n0zDGPQUXOopaIqyOt4Ur98K2ieiWr5Wg4slJnmkzc2ItAg"

def test_get_user_transcriptions(api_base_url):
    """IT-04-01: Verificar que se pueden obtener todas las transcripciones del usuario."""
    
    # Endpoint para obtener todas las transcripciones del usuario
    endpoint = f"{api_base_url}/transcriptions/user"
    
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
        
        # Verificar que la respuesta es una lista
        data = response.json()
        assert isinstance(data, list), "La respuesta no es una lista"
        
        # Verificar la estructura de la respuesta
        if len(data) > 0:
            transcription = data[0]
            assert "transcription_id" in transcription, "Transcripción no contiene ID"
            assert "transcription_date" in transcription, "Transcripción no contiene fecha"
            assert "transcription_time" in transcription, "Transcripción no contiene hora"
            
            print(f"Se encontraron {len(data)} transcripciones")
            print(f"Primera transcripción: ID={transcription['transcription_id']}, Fecha={transcription['transcription_date']}")
        else:
            print("No se encontraron transcripciones para el usuario")
        
        print("✅ IT-04-01: Obtención de transcripciones verificada correctamente")
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        pytest.fail(f"Error en test_get_user_transcriptions: {str(e)}")

def test_get_latest_transcription(api_base_url):
    """IT-04-02: Verificar que se puede obtener la última transcripción con análisis emocional."""
    
    # Endpoint para obtener la última transcripción
    endpoint = f"{api_base_url}/transcriptions/user/latest"
    
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
        
        # Verificar la respuesta - aceptamos 200 (éxito) o 404 (no encontrado)
        # Un 404 es válido si el usuario no tiene transcripciones, pero debemos manejarlo
        if response.status_code == 404:
            print("No se encontraron transcripciones para el usuario (404)")
            print("✅ IT-04-02: Prueba pasada (no hay transcripciones)")
            # No fallamos el test si no hay transcripciones
            return
        
        assert response.status_code == 200, f"Obtención de última transcripción fallida con código: {response.status_code}"
        
        # Verificar la estructura de la respuesta
        data = response.json()
        
        # Verificar campos básicos
        assert "transcription_id" in data, "Respuesta no contiene ID de transcripción"
        assert "transcription_date" in data, "Respuesta no contiene fecha de transcripción"
        assert "transcription_time" in data, "Respuesta no contiene hora de transcripción"
        
        # Verificar campos de análisis emocional
        assert "emotion" in data, "Respuesta no contiene campo 'emotion'"
        assert "sentiment" in data, "Respuesta no contiene campo 'sentiment'"
        
        # Verificar probabilidades
        assert "emotion_probs_joy" in data, "Respuesta no contiene probabilidad de alegría"
        assert "emotion_probs_sadness" in data, "Respuesta no contiene probabilidad de tristeza"
        assert "sentiment_probs_positive" in data, "Respuesta no contiene probabilidad de sentimiento positivo"
        assert "sentiment_probs_negative" in data, "Respuesta no contiene probabilidad de sentimiento negativo"
        
        print(f"Última transcripción: ID={data['transcription_id']}")
        print(f"Emoción: {data['emotion']}, Sentimiento: {data['sentiment']}")
        
        print("✅ IT-04-02: Obtención de última transcripción verificada correctamente")
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        pytest.fail(f"Error en test_get_latest_transcription: {str(e)}")

def test_get_weekly_analysis(api_base_url):
    """IT-04-03: Verificar que se puede obtener el análisis emocional de la última semana."""
    
    # Endpoint para obtener análisis de la última semana
    endpoint = f"{api_base_url}/transcriptions/user/last-7-days"
    
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
        
        # Verificar la respuesta - aceptamos 200 (éxito) o 404 (no encontrado)
        # Un 404 es válido si el usuario no tiene transcripciones en los últimos 7 días
        if response.status_code == 404:
            print("No se encontraron transcripciones para los últimos 7 días (404)")
            print("✅ IT-04-03: Prueba pasada (no hay datos semanales)")
            # No fallamos el test si no hay datos
            return
        
        assert response.status_code == 200, f"Obtención de análisis semanal fallida con código: {response.status_code}"
        
        # Verificar la estructura de la respuesta
        data = response.json()
        
        # Verificar campos de probabilidades emocionales
        assert "emotion_probs_joy" in data, "Respuesta no contiene probabilidad de alegría"
        assert "emotion_probs_anger" in data, "Respuesta no contiene probabilidad de enojo"
        assert "emotion_probs_sadness" in data, "Respuesta no contiene probabilidad de tristeza"
        assert "emotion_probs_fear" in data, "Respuesta no contiene probabilidad de miedo"
        
        # Verificar campos de probabilidades de sentimiento
        assert "sentiment_probs_positive" in data, "Respuesta no contiene probabilidad de sentimiento positivo"
        assert "sentiment_probs_negative" in data, "Respuesta no contiene probabilidad de sentimiento negativo"
        assert "sentiment_probs_neutral" in data, "Respuesta no contiene probabilidad de sentimiento neutral"
        
        # Verificar que las probabilidades son valores numéricos entre 0 y 1
        for key, value in data.items():
            assert isinstance(value, (int, float)), f"El valor de {key} no es numérico: {value}"
            assert 0 <= value <= 1, f"El valor de {key} está fuera del rango [0,1]: {value}"
        
        print("✅ IT-04-03: Obtención de análisis semanal verificada correctamente")
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        pytest.fail(f"Error en test_get_weekly_analysis: {str(e)}")

def test_get_top_emotions_sentiments(api_base_url):
    """IT-04-04: Verificar que se pueden obtener las emociones y sentimientos más frecuentes."""
    
    # Endpoint para obtener top emociones y sentimientos
    endpoint = f"{api_base_url}/transcriptions/user/last-week/top-emotions-sentiments"
    
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
        
        # Verificar la respuesta - aceptamos 200 (éxito) o 404 (no encontrado)
        if response.status_code == 404:
            print("No se encontraron datos para el análisis de top emociones (404)")
            print("✅ IT-04-04: Prueba pasada (no hay datos suficientes)")
            # No fallamos el test si no hay datos
            return
        
        assert response.status_code == 200, f"Obtención de top emociones fallida con código: {response.status_code}"
        
        # Verificar la estructura de la respuesta
        data = response.json()
        
        # Verificar campos de top emociones
        assert "emotion_probs_top1" in data, "Respuesta no contiene emoción top 1"
        assert "emotion_probs_top2" in data, "Respuesta no contiene emoción top 2"
        assert "emotion_probs_top3" in data, "Respuesta no contiene emoción top 3"
        
        # Verificar campo de top sentimiento
        assert "sentiment_probs_top1" in data, "Respuesta no contiene sentimiento top 1"
        
        # Verificar que los valores son strings no vacíos
        for key, value in data.items():
            assert isinstance(value, str), f"El valor de {key} no es string: {value}"
            assert value, f"El valor de {key} está vacío"
        
        print(f"Top emociones: 1={data['emotion_probs_top1']}, 2={data['emotion_probs_top2']}, 3={data['emotion_probs_top3']}")
        print(f"Top sentimiento: {data['sentiment_probs_top1']}")
        
        print("✅ IT-04-04: Obtención de top emociones verificada correctamente")
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        pytest.fail(f"Error en test_get_top_emotions_sentiments: {str(e)}")
