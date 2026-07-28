import os
import time
import subprocess

GAR_IMAGE = "europe-west1-docker.pkg.dev/ia-models-vm-hub/simulador-defensa-repo/hornet-edge-ai:latest"
MANIFEST_PATH = "src/capa-fog/fog-deployment.yaml"

def refresh_gcp_k8s_secret():
    """Refresca el token OAuth2 de GCP en K3s para evitar expiraciones de credenciales."""
    try:
        # 1. Obtener token activo de gcloud
        token = subprocess.run(
            ["gcloud", "auth", "print-access-token"], 
            capture_output=True, text=True, check=True
        ).stdout.strip()

        # 2. Generar manifiesto YAML del secreto en memoria
        secret_cmd = [
            "kubectl", "create", "secret", "docker-registry", "gcp-registry-key",
            "--docker-server=europe-west1-docker.pkg.dev",
            "--docker-username=oauth2accesstoken",
            f"--docker-password={token}",
            "--docker-email=not-needed@example.com",
            "--dry-run=client", "-o", "yaml"
        ]
        secret_yaml = subprocess.run(secret_cmd, capture_output=True, text=True, check=True).stdout
        
        # 3. Aplicar el manifiesto directamente en K3s via stdin
        subprocess.run(["kubectl", "apply", "-f", "-"], input=secret_yaml, text=True, capture_output=True, check=True)
        print("[FOG] Credenciales de Google Artifact Registry sincronizadas con K3s.")
    except Exception as e:
        print(f"⚠️ [AVISO] No se pudo refrescar el secreto de GCP: {e}")

def get_remote_manifest_digest():
    """Consulta el SHA256 actual del artefacto OCI en Google Artifact Registry."""
    try:
        cmd = ["gcloud", "artifacts", "docker", "images", "describe", GAR_IMAGE, "--format=value(image_summary.digest)"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=10)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
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
                print(" [ALERTA EW] Interrupción de enlace con Cloud Central. Manteniendo estado local.")
            elif current_digest and current_digest != last_digest:
                print(f" [ALERTA] ¡Nuevo parche OCI detectado en Cloud!")
                print(f"   Digest SHA256: {current_digest[:25]}...")
                
                # Refrescar secreto antes de ordenar a K3s que descargue
                refresh_gcp_k8s_secret()
                
                print("[FOG] Aplicando manifiesto K3s e inyectando OTA al enjambre...")
                try:
                    subprocess.run(["kubectl", "apply", "-f", MANIFEST_PATH], check=True)
                    subprocess.run(
                        ["kubectl", "rollout", "restart", "deployment/hornet-edge-patch-deployment"],
                        check=True
                    )
                    print(" [ÉXITO] Parche inyectado en caliente en el enjambre K3s.")
                except FileNotFoundError:
                    print("  [MODO SIMULACIÓN] 'kubectl' no detectado localmente.")
                
                last_digest = current_digest
                print("\n[FOG] En espera de nuevos parches tácticos desde Cloud...\n")
            
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n[FOG] Servicio detenido.")

if __name__ == "__main__":
    check_and_propagate_patch()
