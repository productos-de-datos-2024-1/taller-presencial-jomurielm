# 
# Docker Server
# =============================================================================
#
# Implementa un servicio API en Docker que se ejecuta en el puerto 5000.
#
# Para la comunicación entre el cliente y el servidor se debe crear una red 
# privada en Docker y ejecutarlos en dicha red:
#
# $ docker network create mynetwork
#
# Para consturir la imagen del servidor se ejecuta:
#
# $ docker build --tag=jdvelasq/api-server:0.1 . 
# $ docker build --tag=jomurielm/api-server:0.1 . 
#
# Las inages actuales se pueden listar con:
#
# $ docker image ls
#
# Para lanzar el servidor se ejecuta:
#
# $ docker run --network=mynetwork --rm -it --name=api-server -p 5001:5000 -v "$PWD"/datalake:/datalake jdvelasq/api-server:0.1
# $ docker run --network=mynetwork --rm -it --name=api-server -p 5001:5000 -v "${PWD}/datalake:/datalake" jomurielm/api-server:0.1
#

# Definición de la imagen base
FROM python:3.9-alpine

# Folder de la app dentro del contenedor
WORKDIR /app
COPY . /app/

# Instalación de dependencias
RUN pip install --upgrade pip
RUN pip install pandas flask 
RUN apk update && apk add python3-dev gcc g++ libc-dev libffi-dev
RUN pip install scikit-learn==1.4.0 

# Datalake
RUN mkdir /datalake

# Punto de entrada
EXPOSE 5000
WORKDIR /workspace
ENTRYPOINT ["python", "/app/server.py"]