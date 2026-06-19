import json
import os

tope_maximo = 5000
archivo_json = "datos_gastos.json"

def procesar_gasto(monto, descripcion):
    try:
        monto_float = float(monto)

        # 1. Lógica del "Rombo" del BPMN
        if monto_float > tope_maximo:
            nuevo_gasto = {
                "monto": monto_float,
                "descripcion": descripcion,
                "estado": "Derivado a Auditoría"
            }
        else:
            nuevo_gasto = {
                "monto": monto_float,
                "descripcion": descripcion,
                "estado": "Aprobado"
            }

        gastos = []

        if os.path.exists(archivo_json):
            try:
                with open(archivo_json, "r") as f:
                    gastos = json.load(f)
            except (json.JSONDecodeError, IOError):
                gastos = []

        gastos.append(nuevo_gasto)

        with open(archivo_json, "w") as f:
            json.dump(gastos, f, indent=4)

        if monto_float > tope_maximo:
            return "Gasto alto detectado. Solicitud derivada a Auditoría Manual."
        else:
            return "Gasto aprobado y registrado en sistema."

    except ValueError:
        return "Error interno: El monto proporcionado no es un número válido."
    except Exception as e:
        return f"Error crítico al guardar el gasto: {str(e)}"