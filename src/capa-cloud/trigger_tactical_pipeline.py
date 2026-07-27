import os
import json
import requests
from google import genai
from google.genai import types

# === CONFIGURACIÓN ===
GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY", "ariegd/hornet-wasm-autonomous-inference")
WORKFLOW_FILE = "deploy-edge-wasm.yml"
GITHUB_BRANCH = "main"

def generate_tactical_json():
    """Consulta a Vertex AI y extrae el JSON táctico determinista."""
    project_id = os.environ.get("GCP_PROJECT", "ia-models-vm-hub")
    location = os.environ.get("GCP_LOCATION", "europe-west1")

    print(f"[1. CLOUD] Consultando Vertex AI ({project_id} / {location})...")

    client = genai.Client(
        vertexai=True,
        project=project_id,
        location=location
    )

    system_instruction = (
        "Actúas como el generador de parches tácticos de la plataforma Delta. "
        "Tu única tarea es analizar la orden militar y devolver estrictamente un objeto JSON válido, "
        "sin texto adicional, sin explicaciones y sin bloques de código markdown ```json.\n\n"
        "Estructura obligatoria:\n"
        "{\n"
        '  "ignore_frequency_ghz": 2.4,\n'
        '  "min_confidence_threshold": 0.90,\n'
        '  "target_priority": ["Fuel_Tanker", "BTR-80"]\n'
        "}"
    )

    operator_query = (
        "Inhibidores enemigos activos detectados en 2.4 GHz en el Sector Sur. "
        "Asigna prioridad máxima a camiones de combustible (Fuel_Tanker) y exige una confianza de la IA del 90%."
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[operator_query],
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.1,
        )
    )

    raw_text = response.text.replace("```json", "").replace("```", "").strip()
    return raw_text

def trigger_github_workflow(payload_json, github_token):
    """Envía el JSON a la API de GitHub Actions para disparar el workflow_dispatch."""
    print("[2. GIT-FACTORY] Conectando con la API REST de GitHub...")

    url = f"[https://api.github.com/repos/](https://api.github.com/repos/){GITHUB_REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches"

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    data = {
        "ref": GITHUB_BRANCH,
        "inputs": {
            "tactical_config": payload_json
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 204:
        print("[ÉXITO] Pipeline de compilación y despliegue disparado en GitHub Actions.")
        print(f"Payload inyectado en el artefacto:\n{payload_json}")
    else:
        print(f" [ERROR] Fallo en la API de GitHub. Código HTTP: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    github_token = os.environ.get("GITHUB_TOKEN")

    if not github_token:
        print("Error: La variable de entorno GITHUB_TOKEN no está definida.")
        print("Ejecuta: export GITHUB_TOKEN='tu_personal_access_token'")
        exit(1)

    try:
        json_config = generate_tactical_json()
        
        # Validar sintaxis JSON antes del dispatch
        json.loads(json_config)
        
        trigger_github_workflow(json_config, github_token)

    except Exception as e:
        print(f"Fallo en el Continuo de Automatización: {e}")
