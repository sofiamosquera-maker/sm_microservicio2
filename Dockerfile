FROM python:3.11-slim

WORKDIR /app

RUN addgroup --system appgroup && adduser --system --group appuser

# Instalar libpq para conexión con PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar código de la aplicación
COPY app.py .
COPY models.py .
COPY database.py .


# Instala Flask
RUN pip install flask
RUN pip install requests

RUN chown -R appuser:appgroup /app

USER appuser
# Expone el puerto en el que corre la app
EXPOSE 3000

# Comando por defecto para ejecutar la app
CMD ["python", "app.py"]
