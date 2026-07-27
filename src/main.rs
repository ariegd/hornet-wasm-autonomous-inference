use serde::{Deserialize, Serialize};
use std::io::{self, Read};

#[derive(Serialize, Deserialize, Debug)]
struct CameraFrame {
    gps_signal_connected: bool,
    radio_link_dbm: i32,
    optical_detections: Vec<Target>,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
struct Target {
    class: String,
    confidence: f32,
    relative_coords: (f32, f32),
}

#[derive(Serialize, Debug)]
struct FlightControllerCommand {
    autonomous_mode_active: bool,
    target_locked: Option<Target>,
    action: String,
}

fn main() -> io::Result<()> {
    println!("[EDGE AI] Inicializando subsistema óptico Hornet...");

    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer)?;

    let frame_data = if buffer.trim().is_empty() {
        r#"{
            "gps_signal_connected": false,
            "radio_link_dbm": -110,
            "optical_detections": [
                {"class": "BTR-80", "confidence": 0.94, "relative_coords": [12.4, -5.2]}
            ]
        }"#.to_string()
    } else {
        buffer
    };

    let frame: CameraFrame = serde_json::from_str(&frame_data)
        .map_err(|e| io::Error::new(io::ErrorKind::InvalidData, e))?;

    let ew_jamming_detected = !frame.gps_signal_connected || frame.radio_link_dbm < -95;
    let mut locked_target: Option<Target> = None;
    let mut decision = "MANTENER_RUTA_INICIAL";

    if ew_jamming_detected {
        println!("[ALERTA EW] Interferencia electrónica severa detectada. Transicionando a modo terminal autónomo.");
        if let Some(target) = frame.optical_detections.iter().find(|t| t.class == "BTR-80" && t.confidence > 0.85) {
            locked_target = Some(target.clone());
            decision = "FIJAR_BLANCO_Y_ENFILAR_IMPACTO";
        } else {
            decision = "MANIOBRA_DE_EVASIÓN_Y_RECONEXIÓN";
        }
    } else {
        println!("[ESTADO OK] Conexión estable con el Nodo Fog de control vanguardista.");
    }

    let command = FlightControllerCommand {
        autonomous_mode_active: ew_jamming_detected,
        target_locked: locked_target,
        action: decision.to_string(),
    };

    let output_json = serde_json::to_string_pretty(&command).unwrap();
    println!("\n[COMANDO GENERADO POR WASM]:\n{}", output_json);

    Ok(())
}
