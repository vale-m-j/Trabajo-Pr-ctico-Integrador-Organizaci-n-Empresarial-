import logica

usuarios_estados = {}
datos_temporales = {}

def manejar_mensaje(user_id, mensaje):
    # Validamos que el mensaje no sea nulo antes de procesar
    if not mensaje:
        return "No se ha recibido ninguna respuesta, por favor intente de nuevo."

    estado = usuarios_estados.get(user_id, 0)
    
    if estado == 0:
        usuarios_estados[user_id] = 1
        return "¡Hola! Ingrese el monto del gasto:"

    elif estado == 1:
        try:
            monto = float(mensaje)
            if monto < 0:
                return "Error: El monto no puede ser negativo. Ingrese un número válido:"
            
            datos_temporales[user_id] = {"monto": monto}
            usuarios_estados[user_id] = 2
            return "Perfecto. Ahora ingrese una descripción del gasto:"
        except ValueError:
            return "Error: No ha ingresado un monto válido. Por favor, ingrese solo números:"

    elif estado == 2:
        monto = datos_temporales[user_id]["monto"]
        descripcion = mensaje.strip()
        
        if not descripcion:
            return "Error: La descripción no puede estar vacía. Por favor, intente de nuevo:"
        
        # --Blindaje de integración--
        try:
            resultado = logica.procesar_gasto(monto, descripcion)
            usuarios_estados[user_id] = 0
            return f"Proceso finalizado. Resultado: {resultado}"
        except Exception as e:
            # Si logica.py falla, el bot no se cierra, avisa el error
            return f"Error al procesar el gasto: {e}"

    return "No comprendo su mensaje."

if __name__ == "__main__":
    print("Bot iniciado. (Escriba 'salir' para finalizar.)")
    user_id = "usuario_test"
    
    # Bucle principal con protección ante interrupciones
    while True:
        try:
            mensaje = input("Usted: ")
            if mensaje.lower() == 'salir':
                print("Cerrando bot...")
                break
            
            respuesta = manejar_mensaje(user_id, mensaje)
            print(f"Bot: {respuesta}")
        except KeyboardInterrupt:
            # Esto captura cuando presionas Ctrl+C en la consola
            print("\nBot detenido por el usuario.")
            break
        except Exception as e:
            print(f"Error inesperado en el sistema: {e}")