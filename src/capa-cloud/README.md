# Crear un proyecto con un nombre genérico
1. Comando para crear el proyecto
```
gcloud projects create ia-models-vm-hub --name="AI Models and VMs Hub"
```
2. Vincular tu cuenta de facturación (Billing)
```
# 1. Primero busca el ID de tu cuenta de facturación activa
gcloud billing accounts list

# 2. Vincula ese ID a tu nuevo proyecto
gcloud billing projects link ia-models-vm-hub --billing-account=TU_BILLING_ACCOUNT_ID
```
3. Activar la API de Compute Engine
```
# Cambia tu entorno de gcloud al nuevo proyecto
gcloud config set project ia-models-vm-hub

# Activa la API de Compute Engine (esto puede tardar un minuto)
gcloud services enable compute.googleapis.com
```
4. Crear la cuenta de servicio (Si aún no lo has hecho)
```
gcloud iam service-accounts create mi-cuenta-servicio \
    --description="Cuenta para gestionar repositorios de Artifact Registry" \
    --display-name="Mi Cuenta Servicio"
```
5. Darle los permisos de Escritura (Tu comando original)
```
gcloud artifacts repositories add-iam-policy-binding simulador-defensa-repo \
    --location=europe-west1 \
    --member="serviceAccount:mi-cuenta-servicio@ia-models-vm-hub.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.writer"
```
6. Configurar Docker en tu terminal local
```
gcloud auth configure-docker europe-west1-docker.pkg.dev
```


# Google Artifact Registry
Para aprovisionar el repositorio en Google Artifact Registry y dejar la infraestructura de la "Factoría de Parches" lista para recibir las imágenes OCI de WebAssembly, ejecuta la siguiente secuencia de comandos desde la terminal local configurada con `gcloud`:
1. Configurar el proyecto activo:
```
export PROJECT_ID="tu-proyecto-gcp-id"
gcloud config set project $PROJECT_ID
```
2. Habilitar la API de Artifact Registry
```
gcloud services enable artifactregistry.googleapis.com
```
3. Crear el repositorio OCI/Docker
```
gcloud artifacts repositories create simulador-defensa-repo \
    --repository-format=docker \
    --location=europe-west1 \
    --description="Repositorio OCI para artefactos Edge Wasm (Simulador Defensa)"
```
4.  Verificar la creación del repositorio
```
gcloud artifacts repositories list --location=europe-west1
```





