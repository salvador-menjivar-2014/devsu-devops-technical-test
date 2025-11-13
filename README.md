# Prueba Técnica DevOps - Demo API por Salvador Menjivar

Este repositorio contiene la solución completa para la prueba técnica de DevOps. La solución incluye la aplicación Django, su contenedorización con Docker, un pipeline de CI/CD seguro con GitHub Actions y manifiestos para su despliegue en un entorno de Kubernetes.

## Arquitectura de la Solución

El siguiente diagrama ilustra el flujo de trabajo de DevSecOps implementado, desde el desarrollo hasta el despliegue.

```mermaid
graph TD
    A[👨‍💻 Desarrollador] -- git push --> B[🐱 GitHub];
    B --> C{🤖 GitHub Actions};
    C -- Dispara Workflow --> D[🧪 Job: Test];
    D -- Pasa --> E[🏗️ Job: Build & Push];
    E -- Imagen OK --> F[🛡️ Job: Scan];
    E -- Publica Imagen --> G[🐳 Docker Hub];
    F -- Pasa --> H{✅ Pipeline Exitoso};

    subgraph Kubernetes Cluster (Minikube)
        I[🌐 Ingress] --> J[🚦 Service];
        J --> K[<font size=5>📱</font> Pod 1];
        J --> L[<font size=5>📱</font> Pod 2];
        K -- Conecta a --> M[<font size=5>🗄️</font> Pod BD];
        L -- Conecta a --> M;
    end

    G -- k8s pull image --> K;
    G -- k8s pull image --> L;```

## Características Clave Implementadas

-   **Contenedorización Profesional:** Uso de un `Dockerfile` multi-etapa para crear una imagen de producción ligera y segura, ejecutando la aplicación con un usuario no-root para minimizar la superficie de ataque.
-   **Pipeline CI/CD Completo:** Flujo de trabajo automatizado en GitHub Actions que garantiza la calidad y seguridad del código:
    1.  **Pruebas Unitarias:** Ejecución de la suite de tests de Django contra una base de datos PostgreSQL temporal y aislada.
    2.  **Construcción y Publicación:** Creación de la imagen de Docker y subida a un registro público en Docker Hub.
    3.  **Escaneo de Vulnerabilidades (DevSecOps):** Análisis de la imagen con **Trivy** para detectar vulnerabilidades en el SO y las librerías. El pipeline se detiene si se encuentran vulnerabilidades de severidad `HIGH` o `CRITICAL`.
-   **Despliegue Robusto en Kubernetes:**
    -   **Alta Disponibilidad:** El `Deployment` de la aplicación está configurado con **2 réplicas** para asegurar la disponibilidad.
    -   **Gestión de Configuración Segura:**
        -   **Secrets:** Las credenciales de la base de datos y la Django Secret Key se gestionan a través de `Secrets` de Kubernetes, manteniéndolas fuera del control de versiones.
        -   **ConfigMaps:** La configuración no sensible, como `ALLOWED_HOSTS`, se gestiona a través de un `ConfigMap`.
    -   **Enrutamiento Avanzado:** Un `Ingress` gestiona el acceso externo a la aplicación, permitiendo un enrutamiento basado en host, que es la práctica estándar en producción.

## Cómo Ejecutar Localmente con Minikube

**Prerrequisitos:**
-   Docker
-   Minikube
-   kubectl

1.  **Iniciar Minikube:**
    ```bash
    minikube start
    ```

2.  **Habilitar el Ingress Controller:**
    ```bash
    minikube addons enable ingress
    ```

3.  **Construir la Imagen Localmente:** Debido a las diferencias de arquitectura (local ARM vs. CI AMD64), la imagen debe ser construida en el entorno de Minikube.
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
    *Recuerda crear tus propios `k8s/secrets.yml` y `k8s/postgres-secret.yml` si los valores por defecto no son adecuados.*
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
    Abre tu navegador y ve a la URL: **http://devsu-api.local/api/users/**.

## Resultados del Pipeline y Despliegue

A continuación se presentan las capturas de pantalla que validan la ejecución exitosa del proyecto.

**1. Pipeline de CI/CD Exitoso en GitHub Actions:**
*(Aquí debes pegar tu captura de pantalla de la ejecución del pipeline con los 3 jobs en verde)*

**2. Verificación de Pods en Kubernetes:**
*(Aquí debes pegar tu captura de pantalla de la terminal con el resultado de `kubectl get pods` mostrando los 3 pods en estado `Running`)*

**3. Aplicación Funcionando:**
*(Aquí debes pegar tu captura de pantalla del navegador mostrando la API de Django REST Framework en `http://devsu-api.local/api/users/`)*