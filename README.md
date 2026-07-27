# hornet-wasm-autonomous-inference
Simulación académica de una arquitectura Edge-Fog-Cloud para entornos denegados basada en WebAssembly y K3s. Inspirado en modelos operativos de Edge AI modernos.

## En el flujo continuo completo:
```
[Operario Mando Central] 
        ↓ (Consulta en Lenguaje Natural)
[Vertex AI / Gemini (Capa Cloud)] 
        ↓ (Genera Payload JSON de Reconfiguración)
[GitHub Actions CI/CD (Factoría de Parches)] 
        ↓ (Compila nuevo módulo .wasm en Scratch)
[Google Artifact Registry]
        ↓ (Push vía Satélite/Mesh)
[Nodo Fog (Vehículo / Estación Terrena)] → [Dron Hornet (Edge Wasm)]
```

## Cláusula de Exención de Responsabilidad (Disclaimer)
**AVISO IMPORTANTE Y EXCLUSIÓN DE RESPONSABILIDAD:** Este proyecto ha sido desarrollado exclusivamente con fines académicos, educativos y de investigación para la Facultad de Informática de la Universidad Complutense de Madrid (UCM). 

El objetivo principal es modelar, simular y evaluar la eficiencia técnica de arquitecturas de computación distribuida (Edge, Fog y Cloud) empleando tecnologías de virtualización ligera (WebAssembly, K3s) bajo escenarios simulados de alta latencia y pérdida de conectividad. 

Este repositorio **no contiene**:
1. Información clasificada, militar o gubernamental de ningún Estado.
2. Código fuente, algoritmos propietarios o software real de la empresa Palantir Technologies ni del ecosistema Brave1.
3. Sistemas informáticos ofensivos, tácticos o de control de armamento real.

Todo el software provisto utiliza conjuntos de datos públicos/sintéticos y herramientas de orquestación de código abierto orientadas al ámbito civil. El autor no se responsabiliza del uso indebido, alteración o aplicación de los conceptos aquí expuestos fuera del marco estrictamente educativo del presente trabajo de asignaturas de DevOps/Sistemas Distribuidos.

---

## Descripción del Módulo Edge (Dron Hornet)
Este componente simula la lógica terminal del dron cuando pierde la señal de radio/GPS. Está desarrollado en **Rust**, compilado a **WebAssembly (wasm32-wasi)** para reducir drásticamente el peso del artefacto (<5MB) y permitir parches en caliente *Over-The-Air* (OTA).
