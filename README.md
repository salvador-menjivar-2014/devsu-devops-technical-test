# Prueba Técnica DevOps - Demo API por Salvador Menjivar

Este repositorio contiene la solución completa para la prueba técnica de DevOps. La solución incluye la aplicación Django, su contenedorización con Docker, un pipeline de CI/CD seguro con GitHub Actions y manifiestos para su despliegue en un entorno de Kubernetes.

## Arquitectura de la Solución

El siguiente diagrama ilustra el flujo de trabajo de DevSecOps implementado, desde el desarrollo hasta el despliegue.

![Diagrama de Arquitectura](https://raw.githubusercontent.com/salvador-menjivar-2014/devsu-devops-technical-test/main/docs/architecture.png)


## Características Clave Implementadas

-   **Contenedorización Profesional:** Uso de un `Dockerfile` multi-etapa para crear una imagen de producción ligera y segura, ejecutando la aplicación con un usuario no-root.
-   **Pipeline CI/CD Completo (DevSecOps):**
    1.  **Pruebas Unitarias:** Ejecución de la suite de tests de Django contra una base de datos PostgreSQL temporal.
    2.  **Construcción y Publicación:** Creación de la imagen de Docker y subida a un registro público en Docker Hub.
    3.  **Escaneo de Vulnerabilidades:** Análisis con **Trivy** para detectar vulnerabilidades `HIGH` o `CRITICAL` y detener el pipeline si se encuentran.
-   **Despliegue Robusto en Kubernetes:**
    -   **Alta Disponibilidad:** El `Deployment` de la aplicación está configurado con **2 réplicas**.
    -   **Gestión de Configuración Segura:** Uso de `Secrets` de Kubernetes para gestionar credenciales y claves sensibles, manteniéndolas fuera del control de versiones.
    -   **Exposición de Servicio:** Un `Service` de tipo `LoadBalancer` expone la aplicación para el acceso local a través de un túnel de Minikube.

## Cómo Ejecutar Localmente con Minikube

**Prerrequisitos:**
-   Docker, Minikube, kubectl

1.  **Iniciar Minikube:**
    ```bash
    minikube start
    ```

2.  **Habilitar el Ingress Controller:**
    ```bash
    minikube addons enable ingress
    ```

3.  **Construir la Imagen Localmente:** (Necesario por diferencias de arquitectura ARM vs AMD64).
    ```bash
    eval $(minikube docker-env)
    docker build -t salvadormenjivar/devsu-app:latest .
    eval $(minikube docker-env -u)
    ```

4.  **Obtener la IP de Minikube y Configurar Host:**
    ```bash
    minikube ip
    ```
    Añade la siguiente línea a tu archivo `/etc/hosts` (necesitarás `sudo`), reemplazando `<MINIKUBE_IP>` con la IP del paso anterior:
    ```
    <MINIKUBE_IP> devsu-api.local
    ```

5.  **Aplicar los Manifiestos de Kubernetes:**
    *Asegúrate de que el archivo `k8s/secrets.yml` está configurado con los valores correctos.*
    ```bash
    kubectl apply -f k8s/
    ```

6.  **Ejecutar las Migraciones de la Base de Datos:**
    ```bash
    # Espera a que los pods de la aplicación estén en estado 'Running'
    POD_NAME=$(kubectl get pods -l app=devsu-api -o jsonpath='{.items.metadata.name}')
    kubectl exec -it $POD_NAME -- python manage.py migrate
    ```

7.  **Acceder a la Aplicación:**
    Abre tu navegador y ve a la URL: **http://devsu-api.local/api/users/**

## Resultados del Proyecto

A continuación se presentan las capturas de pantalla que validan la ejecución exitosa del proyecto.

**1. Pipeline de CI/CD Exitoso en GitHub Actions:**  
![Pipeline Exitoso](https://raw.githubusercontent.com/salvador-menjivar-2014/devsu-devops-technical-test/main/docs/pipeline.png)

**2. Verificación de Pods en Kubernetes:**  
![Pods en Running](https://raw.githubusercontent.com/salvador-menjivar-2014/devsu-devops-technical-test/main/docs/pods.png)

**3. Aplicación Funcionando:**  
![Aplicación Funcionando](https://raw.githubusercontent.com/salvador-menjivar-2014/devsu-devops-technical-test/main/docs/app.png)
