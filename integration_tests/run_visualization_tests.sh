#!/bin/bash

# Activar entorno virtual
source /home/lflee/pytest-env/bin/activate

# Cambiar al directorio de pruebas
cd /home/lflee/apisix-api-gateway/integration_tests

# Ejecutar pruebas
echo "Ejecutando pruebas de visualización de datos (IT-04)..."
pytest -v test_visualization.py

# Mostrar resumen
echo "Pruebas completadas."
