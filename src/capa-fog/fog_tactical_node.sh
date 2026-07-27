#!/usr/bin/env bash
set -e

# Configuración de variables de infraestructura
PROJECT_ID="ia-models-vm-hub"
GAR_LOCATION="europe-west1"
REPOSITORY="simulador-defensa-repo"
IMAGE_NAME="hornet-edge-ai"
IMAGE_URI="${GAR_LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE_NAME}:latest"

echo "======================================================================"
echo " NODO FOG TÁCTICO - ESTACIÓN DE VANGUARDIA (SECTOR SUR)"
echo "======================================================================"

# 1. Autenticación y Pull del artefacto OCI desde GCP Artifact Registry
echo "[1/4] Sincronizando parche con Cloud Central (Google Artifact Registry)..."
gcloud auth configure-docker ${GAR_LOCATION}-docker.pkg.dev --quiet > /dev/null 2>&1

echo "[2/4] Extrayendo imagen OCI Scratch: ${IMAGE_URI}"
CONTAINER_ID=$(docker create ${IMAGE_URI})

# 2. Extracción del binario Wasm liviano del contenedor Scratch
echo "[3/4] Extrayendo módulo ejecutable .wasm hacia almacenamiento volátil del Dron..."
mkdir -p /tmp/hornet-runtime
docker cp ${CONTAINER_ID}:/handler.wasm /tmp/hornet-runtime/hornet_edge_ai.wasm
docker rm ${CONTAINER_ID} > /dev/null

SIZE_KB=$(du -k "/tmp/hornet-runtime/hornet_edge_ai.wasm" | cut -f1)
echo "   Módulo Wasm desempaquetado con éxito. Tamaño total: ${SIZE_KB} KB."

# 3. Preparación de Telemetría Táctica (Simulación de Sensores Ópticos / Jamming EW)
echo "[4/4] Inyectando vector de telemetría de vuelo (Pérdida de GPS + Detección BTR-80)..."

INPUT_FRAME=$(cat <<EOF
{
  "gps_signal_connected": false,
  "radio_link_dbm": -108,
  "optical_detections": [
    {
      "class": "BTR-80",
      "confidence": 0.96,
      "relative_coords": [15.2, -3.8]
    }
  ]
}
EOF
)

echo ""
echo "======================================================================"
echo " EJECUTANDO LÓGICA AUTÓNOMA EN MOTOR WASM (EDGE DRONE RUNTIME)"
echo "======================================================================"

# 4. Ejecución del binario Wasm pasando la telemetría por stdin
if command -v wasmtime &> /dev/null; then
    echo "$INPUT_FRAME" | wasmtime /tmp/hornet-runtime/hornet_edge_ai.wasm
elif command -v wasmedge &> /dev/null; then
    echo "$INPUT_FRAME" | wasmedge /tmp/hornet-runtime/hornet_edge_ai.wasm
else
    echo " Runtime Wasm (wasmtime/wasmedge) no encontrado localmente."
    echo "Ejecutando simulación a través de fallback de contenedor..."
    echo "$INPUT_FRAME" | docker run --rm -i ${IMAGE_URI}
fi

echo "======================================================================"
echo " PROCESO FINALIZADO - ORDEN TRANSMITIDA A ACTUADORES DE VUELO"
echo "======================================================================"
