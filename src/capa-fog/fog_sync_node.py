import os
import time
import json
import subprocess

GAR_IMAGE = "europe-west1-docker.pkg.dev/ia-models-vm-hub/simulador-defensa-repo/hornet-edge-ai:latest"
PATCH_FILE = "src/capa-fog/latest_patch.json"

def get_remote_manifest_digest():
    """Consulta el SHA256 actual del artefacto OCI en Google Artifact Registry."""
    try:
        cmd = ["gcloud", "artifacts", "docker", "images", "describe", GAR_IMAGE, "--format=value(image_summary.digest)"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=10)
        return result.stdout.strip()
    except Exception:
        return None

def check_and_propagate_patch():
    print("==================================================")
    print("[FOG NODE - BLINDADO TÁCTICO] Servidor de Parches OTA Activo")
    print("==================================================")
    print(f"[FOG] Monitorizando artefactos en Cloud: {GAR_IMAGE}\n")
    
    last_digest = ""
    
    try:
        while True:
            current_digest = get_remote_manifest_digest()
            
            if current_digest is None:
                print("[ALERTA EW] Interrupción de enlace con Cloud. Manteniendo último parche en caché local.")
            elif current_digest and current_digest != last_digest:
                print(f"\n[ALERTA FOG] ¡Nuevo parche detectado en Cloud!")
                print(f"   Digest SHA256: {current_digest[:30]}...")
                
                # Guardar el parche localmente para transmitírselo al enjambre por RF local
                patch_data = {
                    "digest": current_digest,
                    "timestamp": time.strftime("%H:%M:%S")
                }
                os.makedirs(os.path.dirname(PATCH_FILE), exist_ok=True)
                with open(PATCH_FILE, "w") as f:
                    json.dump(patch_data, f)
                
                print("[FOG] Parche Wasm transmitido por red local Mesh al enjambre de drones.\n")
                last_digest = current_digest
            
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[FOG] Servicio detenido.")

if __name__ == "__main__":
    check_and_propagate_patch()
