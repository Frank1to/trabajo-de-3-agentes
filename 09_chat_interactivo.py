# ============================================================
# CELDA 9 - Chat interactivo con Mistral sobre los resultados
# Commit: feat: chat interactivo para consultar resultados del pipeline con Mistral
# ============================================================

# Esta celda agrega un chat conversacional al pipeline.
# Mistral recibe como contexto del sistema todos los resultados del analisis:
#   - Modelo seleccionado y metricas
#   - Reporte de clasificacion por clase
#   - Clases del target
#
# El historial de conversacion se mantiene en memoria durante la sesion,
# lo que permite preguntas de seguimiento con contexto acumulado.
#
# Ejemplos de preguntas utiles:
#   "Que tan bien predice autos electricos?"
#   "Cual es la variable mas importante para predecir el combustible?"
#   "Por que el modelo tiene ese accuracy?"
#   "Que recomendas para mejorar el modelo?"
#   "Cuantos autos electricos hay en el dataset?"

print("Chat con Mistral sobre el Cars Dataset 2025")
print("Escribe 'salir' para terminar\n")

historial = [
    {
        "role": "system",
        "content": f"""Sos un experto en analisis de datos automotrices.
Tenes acceso a los resultados de un pipeline de machine learning aplicado al Cars Dataset 2025.

Contexto del analisis:
- Dataset: 1218 autos con datos de precio, motor, potencia, velocidad maxima, rendimiento y tipo de combustible
- Objetivo: clasificar tipo de combustible
- Clases: {clases_target}
- Modelo seleccionado: {agente2.mejor_nombre}
- Accuracy: {metricas['accuracy']}
- F1-Score (weighted): {metricas['f1_weighted']}
- Precision (weighted): {metricas['precision_weighted']}
- Recall (weighted): {metricas['recall_weighted']}

Reporte de clasificacion por clase:
{agente2.reporte_detallado}

Responde preguntas sobre los resultados, el dataset y el analisis en espanol.
Se preciso, usa los numeros del contexto cuando sea relevante."""
    }
]

while True:
    pregunta = input("Vos: ")
    if pregunta.lower().strip() == "salir":
        print("Chat cerrado.")
        break
    if not pregunta.strip():
        continue

    historial.append({"role": "user", "content": pregunta})

    response = client.chat.complete(
        model=MODEL,
        messages=historial
    )

    respuesta = response.choices[0].message.content
    historial.append({"role": "assistant", "content": respuesta})

    print(f"\nMistral: {respuesta}\n")
