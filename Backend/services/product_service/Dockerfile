# Usa la imagen oficial de Python (versión slim)
FROM python:3.11-slim-buster

# Instala las dependencias del sistema necesarias, incluyendo el conector ODBC para SQL Server
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gnupg2 \
        wget \
        apt-transport-https \
        software-properties-common \
        unixodbc-dev \
        curl && \
    wget -qO- https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requerimientos e instala las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Define las variables de entorno para la ejecución de Flask
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1
ENV FLASK_RUN_PORT=5002

# Expone el puerto definido
EXPOSE 5002

# Comando para iniciar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]
