# hornet-wasm-autonomous-inference

Simulación académica de una arquitectura **Edge-Fog-Cloud** resiliente frente a denegación de espectro (EW Jamming), basada en la distribución de parches tácticos de IA compilados en **WebAssembly (Wasm)** y orquestados mediante **K3s** y **GitHub Container Registry (GHCR)**. Inspirado en modelos operativos de Edge AI modernos.

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

## Compilación y Despliegue Rápido
1. Compilación del binario Wasm en Rust
```
# Instalar el target WASI si no está configurado
rustup target add wasm32-wasip1

# Compilar binario optimizado para el enjambre
cargo build --target wasm32-wasip1 --release
```
2. Ejecución de la simulación local de Guerra Electrónica (EW)
```
# Iniciar el nodo Fog táctico en segundo plano
python3 src/capa-fog/fog_sync_node.py &

# Iniciar la simulación del enjambre Edge
python3 src/capa-edge/simulador_enjambre.py
```

---

## Cláusula de Exención de Responsabilidad (Disclaimer)
AVISO IMPORTANTE Y EXCLUSIÓN DE RESPONSABILIDAD: Este proyecto ha sido desarrollado exclusivamente con fines académicos, educativos y de investigación para la Facultad de Informática de la Universidad Complutense de Madrid (UCM).

El objetivo principal es modelar, simular y evaluar la eficiencia técnica de arquitecturas de computación distribuida (Edge, Fog y Cloud) empleando tecnologías de virtualización ligera (WebAssembly, K3s) bajo escenarios simulados de alta latencia y pérdida de conectividad.

Este repositorio no contiene:
1. Información clasificada, militar o gubernamental de ningún Estado.
2. Código fuente, algoritmos propietarios o software real de empresas del sector de defensa o iniciativas gubernamentales externas.
3. Sistemas informáticos ofensivos, tácticos o de control de armamento rea.

Todo el software provisto utiliza conjuntos de datos públicos/sintéticos y herramientas de orquestación de código abierto orientadas al ámbito civil. El autor no se responsabiliza de la utilización indebido, alteración o aplicación de los conceptos aquí expuestos fuera del marco estrictamente educativo del presente trabajo de asignaturas de DevOps/Sistemas Distribuidos.
