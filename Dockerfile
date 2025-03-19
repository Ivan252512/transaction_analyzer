FROM python:3.8

WORKDIR /code

# Copiar y instalar dependencias
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . /code/

# Definir variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Comando por defecto para ejecutar la aplicación
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
