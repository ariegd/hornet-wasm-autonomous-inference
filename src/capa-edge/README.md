# Cómo ejecutar y ver la simulación en tiempo real
Abre 3 terminales distintas en nuestro sistema para ver la interacción completa. Verás a los 3 drones imprimiendo su telemetría en pantalla continuamente.
1. Terminal 1 (Drones Edge):
```
python3 src/capa-edge/simulador_enjambre.py
```
2. Terminal 2 (Blindado Fog):
Monitoriza la nube y transmite los parches a la red local.
```
python3 src/capa-fog/fog_sync_node.py
```
3. Terminal 3 (Disparo Cloud / Guerra Electrónica):
Lanza una actualización desde Vertex AI.
```
python3 src/capa-cloud/trigger_tactical_pipeline.py
```
4. Lo que verás en pantalla al lanzar el pipeline
```
 [DRON-CHARLIE] Posición: Sector Sur (10.88.0.4) | Wasm Digest: sha256:cb8ee7c5 | Estado: OPERATIVO
 [DRON-ALPHA] Posición: Sector Norte (10.88.0.2) | Wasm Digest: sha256:cb8ee7c5 | Estado: OPERATIVO
 [DRON-BRAVO] Posición: Sector Centro (10.88.0.3) | Wasm Digest: sha256:cb8ee7c5 | Estado: OPERATIVO
 [DRON-CHARLIE] Posición: Sector Sur (10.88.0.4) | Wasm Digest: sha256:cb8ee7c5 | Estado: OPERATIVO

[DRON-ALPHA] ¡ACTUALIZACIÓN OTA RECIBIDA!
   [DRON-ALPHA] Reemplazando binario Wasm: sha256:cb8ee7c5 ➔ sha256:a6ef5d5a...

[DRON-BRAVO] ¡ACTUALIZACIÓN OTA RECIBIDA!
   [DRON-BRAVO] Reemplazando binario Wasm: sha256:cb8ee7c5 ➔ sha256:a6ef5d5a...

[DRON-CHARLIE] ¡ACTUALIZACIÓN OTA RECIBIDA!
   [DRON-CHARLIE] Reemplazando binario Wasm: sha256:cb8ee7c5 ➔ sha256:a6ef5d5a...
   [DRON-ALPHA] Parche aplicado correctamente. Inferencia reiniciada.

 [DRON-ALPHA] Posición: Sector Norte (10.88.0.2) | Wasm Digest: sha256:a6ef5d5a | Estado: OPERATIVO
   [DRON-BRAVO] Parche aplicado correctamente. Inferencia reiniciada.

 [DRON-BRAVO] Posición: Sector Centro (10.88.0.3) | Wasm Digest: sha256:a6ef5d5a | Estado: OPERATIVO
   [DRON-CHARLIE] Parche aplicado correctamente. Inferencia reiniciada.
```

----

# Prueba Final de la Tesis: Simulación de Guerra Electrónica (EW)
5. Cortar el enlace Cloud (Terminal 3)
Ejecuta el bloqueo de Google Artifact Registry simulando la interferencia RF/EW:
```
echo "127.0.0.1 europe-west1-docker.pkg.dev" | sudo tee -a /etc/hosts

echo "127.0.0.1 artifactregistry.googleapis.com" | sudo tee -a /etc/hosts
```
6. Disparar una orden que no llegará (Terminal 3)
Lanza una nueva actualización desde la nube mientras está el bloqueo:
```
python3 src/capa-cloud/trigger_tactical_pipeline.py
```
7. Cese del ataque EW y autorrecuperación
Elimina el bloqueo para simular que el blindado reestablece el enlace satelital:
```
sudo sed -i '/europe-west1-docker.pkg.dev/d' /etc/hosts

sudo sed -i '/docker.pkg.dev/d; /googleapis.com/d' /etc/hosts
```
En menos de 10 segundos, el nodo Fog detectará el nuevo parche generado en el Paso 6 y los tres drones en la Terminal 1 se actualizarán automáticamente a la nueva versión sin intervención manual.
8. Salida
```
$ python3 src/capa-fog/fog_sync_node.py
==================================================
[FOG NODE - BLINDADO TÁCTICO] Servidor de Parches OTA Activo
==================================================
[FOG] Monitorizando artefactos en Cloud: europe-west1-docker.pkg.dev/ia-models-vm-hub/simulador-defensa-repo/hornet-edge-ai:latest


[ALERTA FOG] ¡Nuevo parche detectado en Cloud!
   Digest SHA256: sha256:a6ef5d5afc5c0d154a8849b...
[FOG] Parche Wasm transmitido por red local Mesh al enjambre de drones.

[ALERTA EW] Interrupción de enlace con Cloud. Manteniendo último parche en caché local.
[ALERTA EW] Interrupción de enlace con Cloud. Manteniendo último parche en caché local.
[ALERTA EW] Interrupción de enlace con Cloud. Manteniendo último parche en caché local.
[ALERTA EW] Interrupción de enlace con Cloud. Manteniendo último parche en caché local.
[ALERTA EW] Interrupción de enlace con Cloud. Manteniendo último parche en caché local.
```
## Lo que acabas de demostrar experimentalmente
1. Aislamiento Cloud (EW Jamming): Al cortar tanto el registro como el endpoint de la API (`artifactregistry.googleapis.com`), simulaste la pérdida total de enlace `satelital/RF` con el centro de mando.

2. Tolerancia a fallos en Fog: El nodo Fog no colapsó con excepciones no controladas; detectó la pérdida de enlace e invocó la contingencia manteniéndose como caché local.

3. Inferencia ininterrumpida en Edge: Los tres drones (ALPHA, BRAVO y CHARLIE) mantuvieron la ejecución de sus modelos Wasm a nivel local sin perder ciclo de CPU ni sufrir tiempo de parada (zero downtime).
