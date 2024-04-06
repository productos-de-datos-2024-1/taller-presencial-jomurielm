# 
# Docker Client
# =============================================================================
#
# Implementa una app que usa el servidor API para obtener pronósticos de los
# precios de vivienda dadas sus características.
#
# Para ejecutar el servidor y la app web se debe tener creaada una red:
#
# $ docker network create mynetwork
#
# La imagen es creada con:
# 
# $ docker build --tag=jdvelasq/api-client:0.1 . 
#
# Las images actuales se pueden listar con:
#
# $ docker image ls
#
# Para lanzar la aplicación web que consume el servicio se ejecuta:
#
# $ docker run --network=mynetwork --rm -it --name=api-client -p 5002:5000 -v "$PWD"/datalake:/datalake jdvelasq/api-client:0.1
# $ docker run --network=mynetwork --rm -it --name=api-client -p 5002:5000 -v "${PWD}/datalake:/datalake" jomurielm/api-client:0.1

# Definición de la imagen base
FROM python:3.9-alpine

# Folder de la app dentro del contenedor
WORKDIR /app
COPY . /app

# Instalación de dependencias
RUN pip install --upgrade pip
RUN pip install pandas flask requests

# Datalake
RUN mkdir /datalake

# Punto de entrada
EXPOSE 5000
WORKDIR /workspace
ENTRYPOINT ["python", "/app/app.py"]