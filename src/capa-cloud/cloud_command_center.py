import os
import json
from google import genai
from google.genai import types

def run_cloud_command_center():
    # 1. Configurar variables de entorno y cliente de Vertex AI
    project_id = os.environ.get("GCP_PROJECT", "ia-models-vm-hub")
    location = os.environ.get("GCP_LOCATION", "europe-west1")

    print(f"[CLOUD] Inicializando cliente Vertex AI (Proyecto: {project_id}, Región: {location})...")

    # Inicializamos el cliente indicando explícitamente el uso de Vertex AI
    client = genai.Client(
        vertexai=True,
        project=project_id,
        location=location
    )

    # 2. Instrucciones del sistema (System Instructions Doctrinales)
    system_instruction = (
        "Actúas como el Núcleo de Inteligencia Táctica Centralizado (Plataforma Delta/Brave1). "
        "Tu objetivo es procesar solicitudes en lenguaje natural de operarios militares, analizar logs de "
        "guerra electrónica (EW) y generar de forma estructurada planes de vuelo, prioridades de ataque o "
        "parámetros de reconfiguración para los drones en el Edge.\n\n"
        "Reglas de respuesta:\n"
        "1. Mantén un tono técnico, conciso y estrictamente militar.\n"
        "2. Si el operador pide rutas o prioridades, responde con un análisis estratégico y un bloque JSON final "
        "con los parámetros vectorizados listos para compilar en un parche de software Edge."
    )

    # Modelo de lenguaje rápido y optimizado para razonamiento táctico
    model_name = "gemini-2.5-flash"

    # 3. Datos de telemetría agregados del frente (Fog Consolidation)
    battlefield_context = """
    CONTEXTO OPERATIVO DEL SECTOR SUR:
    - Inhibidores enemigos activos detectados en la frecuencia de radio 2.4 GHz cerca de la coordenada UTM 36UXB1234.
    - Se ha detectado una columna de suministro enemiga moviéndose de Este a Oeste por la carretera principal P50.
    - El nodo Fog (Vehículo Blindado de Control Avanzado) informa que los drones Hornet locales requieren parches para ignorar la frecuencia 2.4 GHz y priorizar vehículos de logística pesada.
    """

    # 4. Consulta en lenguaje natural del oficial al mando
    operator_query = (
        "Muestra rutas de suministro activas en el sector sur, asigna prioridad de ataque al convoy logístico "
        "y prepara el perfil de evasión de EW para los Hornets."
    )

    print("[CLOUD] Procesando inteligencia de combate con Gemini...")

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=[
                f"Contexto Reciente del Frente:\n{battlefield_context}\n\nConsulta del Operario: {operator_query}"
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2, # Baja temperatura para respuesta determinista
            )
        )

        print("\n======================================================================")
        print("RESPUESTA DEL SISTEMA DE MANDO CENTRAL (DELTA / VERTEX AI):")
        print("======================================================================")
        print(response.text)
        print("======================================================================\n")

    except Exception as e:
        print(f"[ERROR CLOUD] Fallo al consultar Vertex AI: {e}")

if __name__ == "__main__":
    run_cloud_command_center()
