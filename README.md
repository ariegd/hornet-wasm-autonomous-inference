# hornet-wasm-autonomous-inference

![Pipeline Status](https://img.shields.io/github/actions/workflow/status/ariegd/hornet-wasm-autonomous-inference/publish-package.yml?branch=master&label=CI%2FCD%20Pipeline&logo=githubactions&logoColor=white)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
![GHCR Package](https://img.shields.io/badge/GHCR-hornet--wasm--autonomous--inference-2496ED?logo=github&logoColor=white)
![Wasm Target](https://img.shields.io/badge/Wasm_Target-wasm32--wasip1-624FE8?logo=webassembly&logoColor=white)

Simulación académica de una arquitectura **Edge-Fog-Cloud** resiliente frente a denegación de espectro (EW Jamming), basada en la distribución de parches tácticos de IA compilados en **WebAssembly (Wasm)** y orquestados mediante **K3s** y **GitHub Container Registry (GHCR)**. Inspirado en modelos operativos de Edge AI modernos.

---

### Stack Tecnológico

**Infraestructura & Cloud:**  
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-GCP_/_Vertex_AI-4285F4?logo=googlecloud&logoColor=white)](https://cloud.google.com/)
[![K3s](https://img.shields.io/badge/K3s-Lightweight_Kubernetes-FFC61C?logo=k3s&logoColor=white)](https://k3s.io/)
[![Docker](https://img.shields.io/badge/Docker-OCI_Containers-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04_LTS-E95420?logo=ubuntu&logoColor=white)](https://ubuntu.com/)

**DevOps & Continuous Delivery:**  
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD_Pipeline-2088FF?logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![GHCR](https://img.shields.io/badge/GHCR-Package_Registry-2496ED?logo=github&logoColor=white)](https://ghcr.io)
[![Cargo](https://img.shields.io/badge/Cargo-Wasm_Build_System-000000?logo=rust&logoColor=white)](https://doc.rust-lang.org/cargo/)

**Core Runtimes & Edge AI:**  
[![Rust](https://img.shields.io/badge/Rust-Inference_Engine-000000?logo=rust&logoColor=white)](https://www.rust-lang.org/)
[![WebAssembly](https://img.shields.io/badge/WebAssembly-WASI_Target-624FE8?logo=webassembly&logoColor=white)](https://webassembly.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)

**Protocolos & Resiliencia Táctica:**  
[![CoAP](https://img.shields.io/badge/Protocol-CoAP_/_UDP-00599C)](#)
[![SHA256 Sync](https://img.shields.io/badge/Resilience-SHA256_Local_Cache-4CAF50)](#)
[![Air-Gapped](https://img.shields.io/badge/EW_Support-Air--Gapped_Fallback-D32F2F)](#)

---

## Tabla de Contenidos
- [Tecnologías y Stack por Capa](#tecnologías-y-stack-por-capa)
- [Arquitectura y Navegación del Proyecto](#arquitectura-y-navegación-del-proyecto)
- [Flujo Continuo Operativo](#flujo-continuo-operativo)
- [Puesta en Marcha (Entorno Táctico Completo)](#puesta-en-marcha-entorno-táctico-completo)
  - [Paso 0: Prerrequisitos y Compilación del Artefacto Wasm](#paso-0-prerrequisitos-y-compilación-del-artefacto-wasm)
  - [Terminal 1: Capa Fog (Nodo Blindado Táctico)](#terminal-1-capa-fog-nodo-blindado-táctico)
  - [Terminal 2: Capa Edge (Simulador de Enjambre Wasm)](#terminal-2-capa-edge-simulador-de-enjambre-wasm)
  - [Terminal 3: Capa Cloud (Trigger / Factoría de Parches)](#terminal-3-capa-cloud-trigger-factoría-de-parches)
- [Prueba Opcional: Simulación de Guerra Electrónica (EW Jamming)](#prueba-opcional-simulación-de-guerra-electrónica-ew-jamming)
- [Demostración en Vídeo](#demostración-en-vídeo)
- [Cláusula de Exención de Responsabilidad (Disclaimer)](#cláusula-de-exención-de-responsabilidad-disclaimer)

---

##  Tecnologías y Stack por Capa

| Capa | Componentes y Herramientas | Función Principal |
| :--- | :--- | :--- |
| **Cloud Layer** | **Vertex AI / Gemini**, **GitHub Actions**, **GHCR / GAR** | Generación de modelos, factoría CI/CD de parches tácticos y empaquetado de artefactos OCI. |
| **Fog Layer** | **Python 3**, **K3s**, **Docker / OCI**, **SHA256 Cache Engine** | Nodo blindado táctico con sincronización remota y caché local resiliente para funcionamiento en aislamiento (*Air-Gapped*). |
| **Edge Layer** | **Rust**, **Cargo** (`wasm32-wasip1`), **Wasm Runtime** | Ejecución ultra-ligera y segura de inferencia en enjambre de drones con inyección OTA *zero-downtime*. |

---

## Arquitectura y Navegación del Proyecto

El código fuente está modularizado en tres sub-capas independientes. Puedes explorar el detalle de cada subsistema en sus respectivos módulos:

* 📁 [**`src/capa-cloud/`**](https://github.com/ariegd/hornet-wasm-autonomous-inference/tree/master/src/capa-cloud) — Pipeline de CI/CD, definición de triggers y empaquetado OCI para GitHub Container Registry.
* 📁 [**`src/capa-fog/`**](https://github.com/ariegd/hornet-wasm-autonomous-inference/tree/master/src/capa-fog) — Lógica de orquestación local (`fog_sync_node.py`), monitorización de registros y fallback automático durante guerra electrónica (EW).
* 📁 [**`src/capa-edge/`**](https://github.com/ariegd/hornet-wasm-autonomous-inference/tree/master/src/capa-edge) — Código fuente en **Rust**, simulador multihilo de enjambre (`simulador_enjambre.py`) y motor de ejecución Wasm.

---

##  Flujo Continuo Operativo

```text
[ Capa Cloud: Vertex AI / GHCR ]
       │  (Push de parche OCI compilado con Cargo: target/wasm32-wasip1)
       ▼
[  Capa Fog: Puesto Táctico / Nodo K3s ]
       │  (Verificación SHA256 + Caché local resiliente)
       ├─── [Conexión activa] ──> Sincronización continua con Cloud
       └─── [Ataque EW / Air-Gap] ──> Autonomía local desde caché interna
       │
       ▼  (Distribución OTA vía Red Mesh / CoAP)
[  Capa Edge: Enjambre Drones Hornet ]
       └─► DRON-ALPHA | DRON-BRAVO | DRON-CHARLIE (Infeccioso / Hot-swapping Wasm)
```

---

## Puesta en Marcha (Entorno Táctico Completo)

Sigue este orden secuencial abriendo **3 terminales independientes** para observar en tiempo real la orquestación distribuida y la inyección OTA de parches Wasm.

### Paso 0: Prerrequisitos y Compilación del Artefacto Wasm
Antes de lanzar las capas, compila el motor de inferencia en Rust para generar el binario ultra-ligero:

```bash
# 1. Cargar las variables de entorno de Rust en la sesión actual (si ya está instalado)
source "$HOME/.cargo/env"

# 2. Si Rust no está instalado en el sistema, ejecuta el instalador oficial y carga el PATH:
# curl --proto '=https' --tlsv1.2 -sSf [https://sh.rustup.rs](https://sh.rustup.rs) | sh
# source "$HOME/.cargo/env"

# 3. Asegurar el target WASI en el compilador de Rust
rustup target add wasm32-wasip1

# 4. Compilar el binario optimizado para el enjambre
cargo build --target wasm32-wasip1 --release
```

### Terminal 1: Capa Fog (Nodo Blindado Táctico)
El nodo Fog actúa como servidor/proxy local. Debe iniciarse primero para establecer la caché local SHA256 y escuchar la conexión del enjambre.
```bash
# Ejecutar el monitor y sincronizador de parches del nodo Fog
python3 src/capa-fog/fog_sync_node.py
```
> **Salida esperada:** Inicialización de la base de datos de caché local y escucha activa de registros OCI/GHCR en segundo plano.

### Terminal 2: Capa Edge (Simulador de Enjambre Wasm)
Inicia la simulación concurrente del enjambre de drones (`DRON-ALPHA`, `DRON-BRAVO`, `DRON-CHARLIE`) ejecutando la inferencia Wasm en bucle.
```bash
# Lanzar el simulador de enjambre táctico
python3 src/capa-edge/simulador_enjambre.py
```
> **Salida esperada:** Los tres drones comenzarán a ejecutar ciclos de inferencia con la versión `v1.0.0` del binario `.wasm` y quedarán a la espera de parches OTA.

### Terminal 3: Capa Cloud (Trigger / Factoría de Parches)
Simula la generación de un nuevo payload de reconfiguración desde Vertex AI / Gemini y su publicación en la factoría de CI/CD.
```bash
# Disparar la actualización del nuevo parche táctico Wasm
python3 src/capa-cloud/trigger_tactical_pipeline.py
```
>  **Efecto visual:** Observamos cómo **Terminal 1 (Fog)** descarga el nuevo artefacto, valida la hash SHA256 y **Terminal 2 (Edge)** actualiza los tres drones en caliente (hot-swapping) sin detener la ejecución de los hilos.
---

## Prueba Opcional: Simulación de Guerra Electrónica (EW Jamming)
Para verificar la resiliencia y autonomía local del sistema en aislamiento (Air-Gapped):

1. **Bloquear la conexión con la nube:** Simula un ataque EW o pérdida de enlace satelital añadiendo una redirección nula en `/etc/hosts` o desconectando la red:
```bash
sudo sh -c 'echo "127.0.0.1 ghcr.io artifactregistry.googleapis.com" >> /etc/hosts'
```

2. **Reejecutar el Trigger Cloud:** Vuelve a lanzar
`python3 src/capa-cloud/trigger_tactical_pipeline.py` en la Terminal 3.

3. **Resultado:**Verás cómo el Nodo Fog (Terminal 1) detecta la denegación de red, conmuta inmediatamente al modo de contingencia autónomo y distribuye el último parche válido almacenado en su caché local hacia el Enjambre Edge (Terminal 2) sin interrupción del servicio.

4. **Restablecer red:**
```bash
sudo sed -i '/artifactregistry/d; /ghcr.io/d' /etc/hosts
```
---

##  Demostración en Vídeo

Haz clic en la imagen a continuación para ver la simulación completa de la arquitectura y la prueba de resiliencia a Guerra Electrónica (EW):

[![Demostración Simulación Edge-Fog-Cloud Wasm](https://youtu.be/UEbs_qBAtEA)](https://youtu.be/UEbs_qBAtEA)

---

## Cláusula de Exención de Responsabilidad (Disclaimer)
AVISO IMPORTANTE Y EXCLUSIÓN DE RESPONSABILIDAD: Este proyecto ha sido desarrollado exclusivamente con fines académicos, educativos y de investigación para la Facultad de Informática de la Universidad Complutense de Madrid (UCM).

El objetivo principal es modelar, simular y evaluar la eficiencia técnica de arquitecturas de computación distribuida (Edge, Fog y Cloud) empleando tecnologías de virtualización ligera (WebAssembly, K3s) bajo escenarios simulados de alta latencia y pérdida de conectividad.

Este repositorio no contiene:
1. Información clasificada, militar o gubernamental de ningún Estado.
2. Código fuente, algoritmos propietarios o software real de empresas del sector de defensa o iniciativas gubernamentales externas.
3. Sistemas informáticos ofensivos, tácticos o de control de armamento rea.

Todo el software provisto utiliza conjuntos de datos públicos/sintéticos y herramientas de orquestación de código abierto orientadas al ámbito civil. El autor no se responsabiliza de la utilización indebido, alteración o aplicación de los conceptos aquí expuestos fuera del marco estrictamente educativo del presente trabajo de asignaturas de DevOps/Sistemas Distribuidos.
