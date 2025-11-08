# Imagen base liviana
FROM python:3.11-slim

# Crear usuario y grupo no root
RUN addgroup --system appgroup && adduser --system --group appuser

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de la aplicación
COPY app.py .
COPY models.py .
COPY database.py .
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Cambiar permisos al usuario no root
RUN chown -R appuser:appgroup /app
USER appuser

# Exponer puerto del servicio
EXPOSE 3000

# Comando de inicio
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]
