#!/bin/bash

# $1 es el primer argumento que pasas al script (el nombre del proyecto)
PROJECT_NAME=$1

if [ -z "$PROJECT_NAME" ]; then
  echo "❌ Error: Debes proporcionar un nombre para el proyecto."
  echo "Uso: ./setup_project.sh nombre_del_proyecto"
  exit 1
fi

echo "🚀 Creando estructura para: $PROJECT_NAME..."

# Crear directorios principales (-p crea padres si no existen)
mkdir -p "$PROJECT_NAME/data/raw"
mkdir -p "$PROJECT_NAME/data/processed"
mkdir -p "$PROJECT_NAME/notebooks"
mkdir -p "$PROJECT_NAME/src"
mkdir -p "$PROJECT_NAME/tests"
mkdir -p "$PROJECT_NAME/logs"

# Crear archivos vacíos iniciales
touch "$PROJECT_NAME/README.md"
touch "$PROJECT_NAME/requirements.txt"
touch "$PROJECT_NAME/.gitignore"

# Crear un __init__.py para que src sea un paquete
touch "$PROJECT_NAME/src/__init__.py"

echo "# $PROJECT_NAME" > "$PROJECT_NAME/README.md"
echo "venv/" > "$PROJECT_NAME/.gitignore"
echo "__pycache__/" >> "$PROJECT_NAME/.gitignore"
echo "*.log" >> "$PROJECT_NAME/.gitignore"

echo "✅ Estructura creada exitosamente en ./$PROJECT_NAME"