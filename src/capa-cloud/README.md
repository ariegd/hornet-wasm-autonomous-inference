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

# Paso imprescindible en GCP para la autenticación sin claves fijas
Como estamos utilizando Workload Identity Federation en la acción `google-github-actions/auth@v2` (la práctica recomendada por Google para evitar guardar claves JSON privadas en GitHub Secrets), debemos ejecutar estos 4 comandos en nuestra terminal local para vincular GitHub con el Service Account:
1. Obtener el número numérico de tu proyecto GCP
```
PROJECT_NUMBER=$(gcloud projects describe ia-models-vm-hub --format="value(projectNumber)")
```
2. Crear el Workload Identity Pool
```
gcloud iam workload-identity-pools create "github-pool" \
  --project="ia-models-vm-hub" \
  --location="global" \
  --display-name="GitHub Actions Pool"
```
3. Crear el Proveedor dentro del Pool autorizando a tu repositorio de GitHub
```
# (Sustituye 'tu-usuario-o-org/tu-repositorio' por el nombre real en GitHub)
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --project="ia-models-vm-hub" \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --display-name="GitHub Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --attribute-condition="assertion.repository == 'ariegd/hornet-wasm-autonomous-inference'" \
  --issuer-uri="https://token.actions.githubusercontent.com"
```
4. Conceder permiso a tu repositorio de GitHub para asumir la Service Account
```
gcloud iam service-accounts add-iam-policy-binding "mi-cuenta-servicio@ia-models-vm-hub.iam.gserviceaccount.com" \
  --project="ia-models-vm-hub" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/github-pool/attribute.repository/ariegd/hornet-wasm-autonomous-inference"
```

# La API de Vertex AI con el SDK de Google GenAI
 para interactuar con modelos masivos de lenguaje (LLM).
1. Habilitar la API de Vertex AI en tu proyecto
```
gcloud services enable aiplatform.googleapis.com --project=ia-models-vm-hub
```
2. Generar credenciales locales de aplicación (ADC)
```
gcloud auth application-default login
```
3. Instalar la librería oficial de Google GenAI
```
pip install google-genai
```

# Salida 
```
(base) zodd@nootbster:~/Documentos/@Documentos/Doctorado2026/projects/hornet-wasm-autonomous-inference$ python3 src/capa-cloud/cloud_command_center.py
[CLOUD] Inicializando cliente Vertex AI (Proyecto: ia-models-vm-hub, Región: europe-west1)...
[CLOUD] Procesando inteligencia de combate con Gemini...

======================================================================
RESPUESTA DEL SISTEMA DE MANDO CENTRAL (DELTA / VERTEX AI):
======================================================================
**ANÁLISIS TÁCTICO - SECTOR SUR**

1.  **Rutas de Suministro Activas:**
    *   Se confirma una ruta de suministro enemiga activa en la carretera principal P50, con movimiento detectado de Este a Oeste. Esta es la única ruta de suministro activa identificada en el contexto actual.

2.  **Prioridad de Ataque:**
    *   Se asigna prioridad de ataque máxima a la columna de suministro enemiga en la carretera P50. La clasificación del objetivo es "Logística Pesada".

3.  **Perfil de Evasión EW para Hornets:**
    *   Los drones Hornet deben reconfigurar sus parámetros de espectro para mitigar la interferencia enemiga. Se implementará una exclusión activa de la banda de 2.4 GHz. Esta medida es crítica para mantener la operatividad en la zona de influencia del inhibidor en UTM 36UXB1234.

---

**PARÁMETROS DE RECONFIGURACIÓN - PLATAFORMA DELTA/BRAVE1**

`json
{
  "drone_patch_config": {
    "target_priorities": [
      {
        "target_id": "convoy_P50_logistics",
        "target_type": "logistics_heavy_vehicle",
        "priority_level": 1,
        "description": "Columna de suministro enemiga en carretera P50",
        "coordinates_utm_approx": "36UXB_P50_corridor"
      }
    ],
    "ew_evasion_profile": {
      "frequency_exclusion": [
        {
          "band": "2.4_GHz",
          "action": "ignore_filter",
          "reason": "enemy_jamming_detected",
          "jamming_source_utm_approx": "36UXB1234"
        }
      ],
      "mode_selection": "passive_ew_avoidance",
      "reconfig_status": "active"
    },
    "operational_directives": {
      "identified_supply_routes": [
        {
          "route_id": "P50",
          "direction": "east_to_west",
          "status": "active_enemy_logistics",
          "threat_level": "high"
        }
      ]
    }
  }
}
`
======================================================================

```

# DevOps Táctico Dirigido por Intenciones (Intent-Driven GitOps)
1. Crear el Script Integrador: `src/capa-cloud/trigger_tactical_pipeline.py`
Este script es la pieza central que materializa el concepto de DevOps Táctico Dirigido por Intenciones (Intent-Driven GitOps): transforma una orden en lenguaje natural en un artefacto compilado binario en la nube en cuestión de segundos, sin intervención humana manual en la base de código.
2. Obtención del Token de GitHub (PAT)
Para que el script tenga permisos de disparar el pipeline en tu repositorio ariegd/hornet-wasm-autonomous-inference:
```
1. En GitHub, ve a Settings → Developer Settings → Personal Access Tokens → Tokens (classic) (o Fine-grained tokens).

2. Haz clic en Generate new token.

3. Asigna un nombre (ej. script-tactico-cloud) y marca el scope:
    repo (o al menos workflows para disparar acciones).

4. Copia el token generado.
```
3. Ejecución de Prueba Integrada
```
# 1. Exportar el token de GitHub
export GITHUB_TOKEN="ghp_tuTokenGeneradoEnGitHubAqui"

# 2. Ejecutar la integración Cloud -> GitHub Actions
python3 src/capa-cloud/trigger_tactical_pipeline.py
```
