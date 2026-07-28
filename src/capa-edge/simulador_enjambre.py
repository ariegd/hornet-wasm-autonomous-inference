import os
import time
import json
from threading import Thread

PATCH_FILE = "src/capa-fog/latest_patch.json"

class TacticalDrone(Thread):
    def __init__(self, name, position):
        super().__init__()
        self.name = name
        self.position = position
        self.current_digest = "v1.0-FABRICA"
        self.running = True

    fn_run = None # Para mantener compatibilidad si se requiriera, pero usamos run estándar

    def run(self):
        while self.running:
            # Comprobar si el nodo Fog ha publicado un parche nuevo en la red local
            if os.path.exists(PATCH_FILE):
                try:
                    with open(PATCH_FILE, "r") as f:
                        data = json.load(f)
                        new_digest = data.get("digest", "")[:15]
                        
                        if new_digest and new_digest != self.current_digest:
                            print(f"\n[{self.name}] ¡ACTUALIZACIÓN OTA RECIBIDA!")
                            print(f"   [{self.name}] Reemplazando binario Wasm: {self.current_digest} ➔ {new_digest}...")
                            time.sleep(1) # Simular flashing del chip en el dron
                            self.current_digest = new_digest
                            print(f"   [{self.name}] Parche aplicado correctamente. Inferencia reiniciada.\n")
                except Exception:
                    pass
            
            print(f" [{self.name}] Posición: {self.position} | Wasm Digest: {self.current_digest} | Estado: OPERATIVO")
            time.sleep(4)

if __name__ == "__main__":
    print("==================================================")
    print(" [CAPA EDGE] ENJAMBRE AUTÓNOMO DE DRONES (3 UNIDADES)")
    print("==================================================")
    print("Iniciando motores de inferencia Wasm en cada unidad...\n")
    
    drones = [
        TacticalDrone("DRON-ALPHA", "Sector Norte (10.88.0.2)"),
        TacticalDrone("DRON-BRAVO", "Sector Centro (10.88.0.3)"),
        TacticalDrone("DRON-CHARLIE", "Sector Sur (10.88.0.4)")
    ]
    
    for drone in drones:
        drone.start()
