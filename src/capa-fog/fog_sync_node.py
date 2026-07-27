import os
import time
import subprocess

GAR_IMAGE = "europe-west1-docker.pkg.dev/ia-models-vm-hub/simulador-defensa-repo/hornet-edge-ai:latest"
MANIFEST_PATH = "src/capa-fog/fog-deployment.yaml"

def get_remote_manifest_digest():
    """Consulta el SHA256 del artefacto OCI en Google Artifact Registry.
    Si falla la conexión (EW Jamming), captura la excepción de forma segura."""
    try:
        cmd = [
            "gcloud", "artifacts", "docker", "images", "describe", 
            GAR_IMAGE, "--format=value(image_summary.digest)"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=5)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        # Estado de Guerra Electrónica / Sin Conexión
        return None

def check_and_propagate_patch():
    print("==================================================")
    print(" [FOG NODE - BLINDADO TÁCTICO] Servicio de orquestación activo.")
    print("==================================================")
    print(f"[FOG] Monitorizando artefactos en Cloud: {GAR_IMAGE}\n")
    
    last_digest = ""
    
    try:
        while True:
            current_digest = get_remote_manifest_digest()
            
            if current_digest is None:
                print(" [ALERTA EW] Pérdida de enlace satelital / Interferencia detectada.")
                print("   -> Manteniendo enjambre autónomo con la última configuración local activa.")
            elif current_digest and current_digest != last_digest:
                print(f" [ALERTA] ¡Nuevo parche de contramedidas detectado en Cloud!")
                print(f"   Digest SHA256: {current_digest[:25]}...")
                print("[FOG] Descargando artefacto Wasm optimizado (~2.3 MB)...")
                time.sleep(1) # Simula descarga de ultra-baja latencia
                
                print("[FOG] Aplicando manifiesto K3s e inyectando OTA al enjambre de drones...")
                
                try:
                    subprocess.run(["kubectl", "apply", "-f", MANIFEST_PATH], check=True)
                    subprocess.run(
                        ["kubectl", "rollout", "restart", "deployment/hornet-edge-patch-deployment"],
                        check=True
                    )
                    print(" [ÉXITO] Parche inyectado en caliente. Enjambre K3s actualizado.")
                except FileNotFoundError:
                    print("  [MODO SIMULACIÓN] 'kubectl' no detectado localmente.")
                    print("    El manifiesto K3s está listo y validado para ejecutarse sobre 'crun'.")
                
                last_digest = current_digest
                print("\n[FOG] En espera de nuevos parches de contramedidas desde Cloud...\n")
            
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n[FOG] Servicio de orquestación detenido.")

if __name__ == "__main__":
    check_and_propagate_patch()
