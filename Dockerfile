FROM python:3.9

WORKDIR /code

# Instalar dependencias del sistema necesarias para h5py y otras librerías
RUN apt-get update && apt-get install -y \
    libhdf5-dev \
    libhdf5-serial-dev \
    hdf5-tools \
    libhdf5-dev \
    libblas-dev \
    liblapack-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# Copiar y instalar dependencias de Python
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . /code/

# Configuración de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Comando por defecto para ejecutar Django
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]
