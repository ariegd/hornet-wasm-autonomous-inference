# Capa Fog / Edge: Estación Terrena y Ejecución Táctica Wasm
Este componente simula la **Estación Terrena de Vanguardia (Nodo Fog)**, que actúa como puente táctico entre el Centro de Mando en la Nube (Google Cloud / Vertex AI) y los vectores autónomos no tripulados (*Edge Drones*).

---

## Herramientas y Requisitos Previos
Para que el Nodo Fog opere correctamente, la estación terrena o vehículo de mando debe contar con las siguientes herramientas instaladas:
```
| Herramienta | Rol en la Capa Fog | Comando de Instalación / Verificación |
| :--- | :--- | :--- |
| **`gcloud` CLI** | Autenticación con Google Cloud para acceder al registro de artefactos privado. | `gcloud auth configure-docker` |
| **`docker` / `podman`** | Motor auxiliar utilizado únicamente para descargar la imagen OCI y extraer el binario Wasm. | `docker --version` |
| **`wasmtime`** *(Recomendado)* | Motor de ejecución (*runtime*) nativo de WebAssembly. Ejecuta el binario directamente sobre el hardware del dron sin necesitar un sistema operativo huésped. | `curl https://wasmtime.dev/install.sh -sSf \| bash` |
```
---

## ¿Qué hace exactamente `fog_tactical_node.sh` paso a paso?
El script simula el ciclo de vida completo de sincronización, desempaquetado e inferencia autónoma ante eventos de Guerra Electrónica (EW):
```
+-----------------------------------------------------------------------------------+
| 1. Sincronización GCP  ──>  2. Extraer .wasm  ──>  3. Inyectar Telemetría  ──>  4. Inferencia Wasm |
|    (Artifact Registry)       (De Scratch a RAM)       (Sensores / Jamming)         (Wasmtime Engine)   |
+-----------------------------------------------------------------------------------+
```

### Paso 1: Autenticación y Descarga del Artefacto OCI
Se conecta a **Google Artifact Registry** (`europe-west1-docker.pkg.dev/ia-models-vm-hub/simulador-defensa-repo/hornet-edge-ai:latest`) y descarga la imagen en contenedor Scratch generada por la factoría de integración continua (GitHub Actions).

### Paso 2: Desempaquetado del Binario Ultra-Ligero
Crea un contenedor temporal sin ejecutarlo para copiar el binario `/handler.wasm` hacia la memoria volátil `/tmp/hornet-runtime/`.
* **Resultado clave:** La imagen completa pesa apenas megabytes, y el ejecutable Wasm extraído ocupa escasamente **128 KB**.

### Paso 3: Inyección de Telemetría Táctica
Simula la entrada de datos provenientes del subsistema óptico y del receptor de radio del dron. En la prueba se inyecta un escenario de ataque de Guerra Electrónica:
* Pérdida total de señal GPS (`gps_signal_connected: false`).
* Degradación de radioenlace a **-108 dBm** (por encima del umbral crítico de -95 dBm).
* Identificación óptica de un transporte blindado enemigo clase **BTR-80** con un 96% de confianza.

### Paso 4: Inferencia Autónoma Nativa (Wasmtime)
Pasa la telemetría JSON directamente a la entrada estándar (`stdin`) de `wasmtime /tmp/hornet-runtime/hornet_edge_ai.wasm`.
* El motor Wasm inicializa en menos de **5 milisegundos**.
* La lógica compilada en Rust detecta el bloqueo de comunicaciones, pasa a modo autónomo terminal, fija el objetivo y emite la orden estructurada hacia los servomotores y actuadores de vuelo: `"action": "FIJAR_BLANCO_Y_ENFILAR_IMPACTO"`.

---

## Justificación de Arquitectura para la Memoria (UCM)

1. **Aislamiento de la Capa de Ejecución:** El dron en el Edge no ejecuta Docker ni tiene un Kernel de Linux completo consumiendo recursos. La estación Fog descarga el paquete OCI estándar y le entrega únicamente el binario estático WebAssembly de 128 KB al microcontrolador/procesador del dron.
2. **Resistencia a Guerra Electrónica (EW):** Al medir solo 128 KB, el parche táctico puede propagarse entre nodos de una red *mesh* táctica o enlaces satelitales degradados en una pequeña fracción de segundo.
3. **Arranque Inmediato (*Cold Start*):** Frente a los 2-5 segundos que tarda un contenedor en levantar su espacio de nombres y procesos Linux, el entorno sandbox de Wasm entra en ejecución de forma determinista en tiempo real (<5ms).

## Salida
```
(base) zodd@nootbster:~/Documentos/@Documentos/Doctorado2026/projects/hornet-wasm-autonomous-inference$ ./src/capa-fog/fog_tactical_node.sh
======================================================================
 NODO FOG TÁCTICO - ESTACIÓN DE VANGUARDIA (SECTOR SUR)
======================================================================
[1/4] Sincronizando parche con Cloud Central (Google Artifact Registry)...
[2/4] Extrayendo imagen OCI Scratch: europe-west1-docker.pkg.dev/ia-models-vm-hub/simulador-defensa-repo/hornet-edge-ai:latest
[3/4] Extrayendo módulo ejecutable .wasm hacia almacenamiento volátil del Dron...
   Módulo Wasm desempaquetado con éxito. Tamaño total: 128 KB.
[4/4] Inyectando vector de telemetría de vuelo (Pérdida de GPS + Detección BTR-80)...

======================================================================
 EJECUTANDO LÓGICA AUTÓNOMA EN MOTOR WASM (EDGE DRONE RUNTIME)
======================================================================
[EDGE AI] Inicializando subsistema óptico Hornet...
[ALERTA EW] Interferencia electrónica severa detectada. Transicionando a modo terminal autónomo.

[COMANDO GENERADO POR WASM]:
{
  "autonomous_mode_active": true,
  "target_locked": {
    "class": "BTR-80",
    "confidence": 0.96,
    "relative_coords": [
      15.2,
      -3.8
    ]
  },
  "action": "FIJAR_BLANCO_Y_ENFILAR_IMPACTO"
}
======================================================================
 PROCESO FINALIZADO - ORDEN TRANSMITIDA A ACTUADORES DE VUELO
======================================================================
```

# Probar la resiliencia del nodo Fog (Blindado) y del enjambre Edge (Drones)
Para probar la resiliencia del nodo Fog (Blindado) y del enjambre Edge (Drones) ante una interrupción total de comunicaciones con la nube (escenario de Guerra Electrónica / EW Jamming), debemos validar tres propiedades fundamentales de la arquitectura:
1. **Inmunidad del Demonio de Sincronización:** El script `fog_sync_node.py` debe manejar la pérdida de conectividad sin colapsar (graceful degradation).
2. **Autonomía Operativa de K3s:** Los pods Wasm en ejecución deben permanecer intactos y funcionales en los drones sin importar que Google Artifact Registry no responda.
3. **Resiliencia de Réplicas (Cache Local):** Si un pod se reinicia o cae en medio del apagón de red, K3s debe ser capaz de re-instanciarlo utilizando la imagen OCI almacenada en la caché local de crun/containerd.

# Ejecutar el Protocolo de Prueba de Resiliencia
1. Iniciar la Capa Fog y verificar el estado base
```
kubectl get pods -l app=hornet-edge-ai -o wide

# Lanza el demonio de la Capa Fog
python3 src/capa-fog/fog_sync_node.py
```
2. Simular el Bloqueo de Guerra Electrónica (Corte a GCP)
```
# Simular ataque EW / Inhibición de frecuencia satelital
sudo sh -c 'echo "127.0.0.1 europe-west1-docker.pkg.dev" >> /etc/hosts'
```

# Observar la reacción del sistema
1. En la consola de `fog_sync_node.py`:
Verás cómo el script detecta el fallo de enlace sin dar un error de Python (`Traceback`), informando de la pérdida de comunicación con Cloud Central y manteniendo el enjambre operando en modo local desconectado.
2. Verificar la estabilidad de los Drones (K3s):
```
kubectl get pods -l app=hornet-edge-ai
```
3. Probar la recuperación ante fallos de hardware en el Edge (Simular caída de un dron):
```
kubectl delete pod -l app=hornet-edge-ai --field-selector status.phase=Running --tail=1
```

# Restablecer la Conectividad (Fin de la Interferencia EW)
Esto demuestra empíricamente la hipótesis principal de la arquitectura: el sistema desacopla la inteligencia de control (Cloud) de la ejecución táctica (Edge/Fog), garantizando la supervivencia del enjambre en entornos denegados.
```
# Eliminar la regla de inhibición de red
sudo sed -i '/europe-west1-docker.pkg.dev/d' /etc/hosts
```
