# 1. Usar una imagen base oficial de Python (ligera)
FROM python:3.11-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar el archivo de dependencias primero (para aprovechar el caché de Docker)
COPY requirements.txt .

# 4. Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del código fuente
COPY src/ src/

# 6. Comando por defecto al ejecutar el contenedor
CMD ["python", "src/app.py"]