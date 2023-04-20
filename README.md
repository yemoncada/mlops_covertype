# Despliegue Modelo con Dataset de CoverType

Este proyecto presenta una aplicación integral de procesamiento y análisis de datos utilizando Streamlit, una plataforma de desarrollo rápido para aplicaciones web basadas en Python. La aplicación se centra en la implementación de servicios que permiten cargar información desde archivos de texto plano hacia bases de datos, entrenar modelos de inteligencia artificial, realizar inferencias con modelos previamente entrenados, almacenar información utilizada en el proceso de inferencia en archivos de texto plano y ofrecer una interfaz gráfica interactiva para facilitar la interacción con estos servicios.

La aplicación ha sido desarrollada en Python, aprovechando sus capacidades de procesamiento de datos, entrenamiento e inferencia de modelos de inteligencia artificial. Se ha utilizado FastAPI para construir una API REST que sirva como interfaz entre los servicios y la aplicación de Streamlit. Además, se ha empleado Docker y Docker Compose para construir y gestionar contenedores que soporten los servicios y faciliten su despliegue en un entorno local o en la nube.

Con el objetivo de llevar la aplicación a un entorno productivo y garantizar su escalabilidad y resiliencia, se ha optado por utilizar Kubernetes como plataforma de orquestación de contenedores. Esto permite el despliegue automático, ajuste a escala y manejo de aplicaciones basadas en contenedores de manera eficiente y segura.


# Table of contents

- [Requisitos](#requisitos)
- [Instalación](#instalacion)
- [Uso](#uso)
- [Despliegue en Kubernets con Kompose](#despliegue)
- [Estructura del Proyecto](#estructura-proyecto)

# Requisitos

[(Back to top)](#table-of-contents)

* Python 3.7+
* Docker
* Docker Compose
* Kompose
* Microk8s

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
    git clone https://github.com/yemoncad/mlops_covertype.git
```

2. Acceder al directorio del repositorio:

```sh
    cd mlops_docker_compose
```

3. Instale Kompose

```sh
# Linux
curl -L https://github.com/kubernetes/kompose/releases/download/v1.24.0/kompose-linux-amd64 -o kompose
chmod +x kompose
sudo mv ./kompose /usr/local/bin/kompose
```

4. Instale Microk8s

```sh
# Linux (Ubuntu)
sudo snap install microk8s --classic
```

3. Construir y ejecutar los contenedores de Docker utilizando docker-compose:

```sh
    docker-compose up --build
```

Las APIs estaran disponibles en `http://localhost:8000`. Para realizar inferencias con el modelo entrenado, utilice la API de inferencia, que estará disponible en `http://localhost:8001`.


# Despliegue en Kubernets con Kompose

1. Convierta los archivos de Docker Compose a archivos de Kubernetes con Kompose:

```sh
    kompose convert -f docker-compose.yml -o komposefiles/
```

2. Inicie MicroK8s:

```sh
    sudo microk8s start
```

3. Aplique los archivos generados de kubernetes generados:

```sh
sudo microk8s kubectl apply -f komposefiles/
```

4. Verifique el estado de los pods:

```sh
sudo microk8s kubectl get pods -o wide
```

5. Exponga el servicio de la aplicación en su dirección IP local:

```sh
sudo microk8s kubectl port-forward --address 0.0.0.0 service/app 8506:8506
```

6. Visualización grafica del despliegue

```sh
sudo microk8s dashboard-proxy
```

7. limpieza de los recursos de kubernets

```sh
sudo microk8s kubectl delete --all daemonsets,replicasets,services,deployments,pods,rc,ingress --namespace=default
```
