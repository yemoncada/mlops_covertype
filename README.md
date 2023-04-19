# Despliegue Modelo con Dataset de Penguins

Este proyecto proporciona una `API` para la clasificación del dataset de `Pengüins` basada en datos de características de pingüinos. Se utiliza SQLAlchemy para conectarse a una base de datos MySQL, y carga los datos del conjunto de datos `penguins` de Seaborn datasets. Luego, los datos se limpian y se insertan en la base de datos en la tabla `penguins`.

La aplicación también define un modelo de clasificación RandomForest utilizando la biblioteca Scikit-learn. El modelo se entrena con los datos de penguins de la base de datos y luego se guarda en un archivo utilizando la biblioteca joblib.


# Table of contents

- [Requisitos](#requisitos)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-proyecto)

# Requisitos

[(Back to top)](#table-of-contents)

Para ejecutar este proyecto, necesitará tener Docker y docker-compose instalados en su sistema.

```sh
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

    sudo chmod +x /usr/local/bin/docker-compose

    docker compose version

```

# Uso

[(Back to top)](#table-of-contents)

Para ejecutar la API de clasificación de pingüinos, siga los siguientes pasos:

1. Clonar el repositorio:

```sh
    git clone https://github.com/yemoncad/mlops_docker_compose.git
```

2. Acceder al directorio del repositorio:

```sh
    cd mlops_docker_compose
```

3. Construir y ejecutar los contenedores de Docker utilizando docker-compose:

```sh
    docker-compose up --build
```

La API estará disponible en `http://localhost:8000`. Para realizar inferencias con el modelo entrenado, utilice la API de inferencia, que estará disponible en `http://localhost:8001`.

# Estructura del Proyecto

[(Back to top)](#table-of-contents)

El proyecto consta de tres servicios de Docker:

* db: un contenedor de MySQL utilizado para almacenar los datos de pingüinos.
* api: un contenedor de FastAPI utilizado para entrenar el modelo de clasificación de bosques aleatorios y exponer una API para realizar predicciones.
* inference: un contenedor de FastAPI utilizado para realizar inferencias utilizando el modelo de clasificación previamente entrenado.

El archivo `docker-compose.yaml` se encarga de configurar y ejecutar los contenedores Docker necesarios para el proyecto. Los archivos `requirements.txt`, `Dockerfile` y `Dockerfile.inference` se utilizan para construir los contenedores de Docker.

El proyecto también contiene los siguientes archivos:

* train.py: un script de Python utilizado para entrenar el modelo de clasificación de bosques aleatorios.
* app/penguin_api.py: un archivo Python que define la API de clasificación de pingüinos utilizando FastAPI.
* app/penguin_inference.py: un archivo Python que define la API de inferencia utilizando FastAPI.
* weights/model.joblib: el archivo de pesos del modelo de clasificación con Random Forest.

