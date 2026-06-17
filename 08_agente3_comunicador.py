# ============================================================
# CELDA 8 - Agente 3: Comunicador
# Commit: feat: Agente 3 - Comunicador que genera reporte ejecutivo en lenguaje natural
# ============================================================

# El Agente 3 recibe los resultados de los dos agentes anteriores
# y los convierte en un reporte ejecutivo comprensible.
#
# Recibe como input:
#   - df_original: info del dataset crudo
#   - estrategia de Mistral del Agente 1 (preprocesamiento)
#   - metricas del Agente 2 (modelo seleccionado, accuracy, F1, etc.)
#   - reporte de clasificacion de sklearn por cada clase
#
# Genera un reporte con 7 secciones:
#   1. Resumen Ejecutivo
#   2. Descripcion del Dataset
#   3. Desafios de Preprocesamiento
#   4. Metodologia de entrenamiento
#   5. Resultados con interpretacion practica
#   6. Insights del analisis
#   7. Limitaciones y Recomendaciones
#
# El reporte se guarda como .txt y se descarga automaticamente en Colab.

class AgenteComunicador:
    def __init__(self, client, model):
        self.client = client
        self.model = model
        self.nombre = "AGENTE 3 - Comunicador"
        self.reporte = None

    def generar_reporte(self, df_original, analisis_norm, metricas, reporte_clf):
        print(f"\n{'='*60}")
        print(f"{self.nombre}")
        print(f"{'='*60}")
        print("Generando reporte ejecutivo con Mistral...\n")

        contexto = {
            "dataset": {
                "nombre": "Cars Datasets 2025",
                "filas": int(df_original.shape[0]),
                "columnas": list(df_original.columns),
                "descripcion": "Dataset de 1218 autos con precio, motor, potencia, velocidad y tipo de combustible"
            },
            "preprocesamiento": analisis_norm,
            "objetivo": "Clasificar el tipo de combustible (Petrol, Diesel, Electric, Hybrid, Plug-in Hybrid, Petrol/Diesel, Other)",
            "metricas_modelo": metricas,
            "reporte_sklearn": reporte_clf
        }

        prompt = f"""
Sos un analista de datos especializado en la industria automotriz.
Genera un reporte ejecutivo completo en espanol sobre este analisis de machine learning aplicado a datos de autos 2025.

{json.dumps(contexto, indent=2, ensure_ascii=False)}

El reporte debe incluir:
1. Resumen Ejecutivo
2. Descripcion del Dataset
3. Desafios de Preprocesamiento
4. Metodologia
5. Resultados
6. Insights del Analisis
7. Limitaciones y Recomendaciones

Usa lenguaje profesional pero accesible. Referencia los numeros concretos.
"""
        response = self.client.chat.complete(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2500
        )
        self.reporte = response.choices[0].message.content
        print(self.reporte)
        return self.reporte

    def guardar_reporte(self, path="reporte_cars_2025.txt"):
        if self.reporte:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.reporte)
            print(f"\nReporte guardado en: {path}")
            from google.colab import files
            files.download(path)


agente3 = AgenteComunicador(client, MODEL)
reporte = agente3.generar_reporte(
    df_original=df_original,
    analisis_norm=agente1.estrategia_mistral,
    metricas=metricas,
    reporte_clf=agente2.reporte_detallado
)
agente3.guardar_reporte()
