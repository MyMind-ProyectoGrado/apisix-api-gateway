#!/bin/bash

# Activar entorno virtual
source /home/lflee/pytest-env/bin/activate

# Cambiar al directorio de pruebas
cd /home/lflee/apisix-api-gateway/integration_tests

# Ejecutar pruebas
echo "Ejecutando pruebas de flujo completo (IT-03)..."
pytest -v test_complete_flow.py

# Mostrar resumen
echo "Pruebas completadas."
