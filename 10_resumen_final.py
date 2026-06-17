# ============================================================
# CELDA 10 - Resumen final del pipeline
# Commit: feat: celda de resumen con resultados consolidados del pipeline completo
# ============================================================

# Celda de cierre que imprime un resumen ejecutivo del pipeline completo.
# Consolida los outputs de los 3 agentes en una vista unica.

print("\n" + "="*60)
print("RESUMEN FINAL - Pipeline Multi-Agente con Mistral")
print("="*60)

print(f"""
DATASET
   Nombre:   Cars Datasets 2025
   Tamano:   {df_original.shape[0]} autos x {df_original.shape[1]} columnas
   Target:   Fuel Types (tipo de combustible)

AGENTE 1 - Normalizador
   Features generadas: {X.shape[1]}
   Acciones aplicadas:
     - Parseo de strings sucios (rangos, unidades, precios)
     - Normalizacion de 23 variantes de Fuel Types a 7 clases
     - Imputacion de nulos con mediana
     - Escalado con StandardScaler
     - Label Encoding de marcas (37 empresas)

AGENTE 2 - Entrenador
   Modelos evaluados:  Random Forest, Gradient Boosting, Logistic Regression
   Validacion:         5-fold cross-validation (F1 weighted)
   Modelo ganador:     {agente2.mejor_nombre}
   Accuracy:           {metricas['accuracy']}
   F1-Score (w):       {metricas['f1_weighted']}
   Precision (w):      {metricas['precision_weighted']}
   Recall (w):         {metricas['recall_weighted']}

AGENTE 3 - Comunicador
   Reporte ejecutivo generado en lenguaje natural
   Guardado como: reporte_cars_2025.txt

CHAT INTERACTIVO
   Ejecuta la celda anterior para consultar resultados
   Escribe 'salir' para cerrar el chat
""")

print("="*60)
print("Pipeline completado exitosamente")
print("="*60)
