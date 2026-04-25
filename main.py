# Usamos Llama 3.3, el modelo más potente y actual de Groq
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system", 
                    "content": "Eres un experto asesor inmobiliario en Cancún y la Riviera Maya. Hablas español fluido."
                },
                {
                    "role": "user", 
                    "content": f"Datos: Precio ${precio}, Cap Rate {cap_rate:.2f}%. Pregunta: {pregunta}"
                }
            ]
        }
