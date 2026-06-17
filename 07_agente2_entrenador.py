# ============================================================
# CELDA 7 - Agente 2: Entrenador
# Commit: feat: Agente 2 - Entrenador con validacion cruzada y seleccion de modelo via Mistral
# ============================================================

# El Agente 2 se encarga del entrenamiento y seleccion del mejor modelo.
# Modelos evaluados:
#   - Random Forest:       ensemble de arboles, robusto con datos tabulares
#   - Gradient Boosting:   boosting secuencial, generalmente alta precision
#   - Logistic Regression: modelo lineal, baseline interpretable
#
# Metodologia:
#   - Split 80/20 estratificado (mantiene proporcion de clases)
#   - Validacion cruzada 5-fold sobre el set de entrenamiento
#   - Metrica principal: F1-Score weighted (maneja desbalance de clases)
#   - class_weight='balanced' en RF y LR para compensar que Petrol >> otras clases
#
# Mistral analiza los resultados de CV y selecciona el mejor modelo
# con una justificacion en lenguaje natural.

class AgenteEntrenador:
    def __init__(self, client, model):
        self.client = client
        self.model = model
        self.nombre = "AGENTE 2 - Entrenador"
        self.mejor_modelo = None
        self.mejor_nombre = None
        self.metricas = {}
        self.reporte_detallado = None

    def seleccionar_con_mistral(self, resultados_cv, clases):
        prompt = f"""
Sos un experto en machine learning evaluando modelos para clasificar tipos de combustible de autos.
Clases a predecir: {clases}

Resultados de validacion cruzada (5-fold, metrica: F1 weighted):
{json.dumps(resultados_cv, indent=2)}

Devuelve SOLO este JSON (sin texto adicional, sin markdown):
{{
  "modelo_seleccionado": "nombre exacto del modelo",
  "razon": "explicacion de 2-3 oraciones considerando el desbalance de clases",
  "alerta": "advertencia importante o null"
}}
"""
        response = self.client.chat.complete(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        texto = response.choices[0].message.content.strip()
        texto = texto.replace("```json", "").replace("```", "").strip()
        return json.loads(texto)

    def entrenar(self, X, y, clases):
        print(f"\n{'='*60}")
        print(f"{self.nombre}")
        print(f"{'='*60}")

        print("\nDistribucion de clases:")
        valores, conteos = np.unique(y, return_counts=True)
        for v, c in zip(valores, conteos):
            print(f"   {clases[v]}: {c} ({c/len(y)*100:.1f}%)")

        modelos = {
            "Random Forest": RandomForestClassifier(
                n_estimators=100, class_weight='balanced', random_state=42
            ),
            "Gradient Boosting": GradientBoostingClassifier(
                n_estimators=100, random_state=42
            ),
            "Logistic Regression": LogisticRegression(
                max_iter=1000, class_weight='balanced', random_state=42
            )
        }

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        resultados_cv = {}
        modelos_entrenados = {}

        print("\nValidacion cruzada (5-fold)...")
        for nombre, modelo in modelos.items():
            scores = cross_val_score(modelo, X_train, y_train, cv=5, scoring='f1_weighted')
            resultados_cv[nombre] = {
                "cv_mean_f1": round(float(scores.mean()), 4),
                "cv_std": round(float(scores.std()), 4),
            }
            modelo.fit(X_train, y_train)
            y_pred = modelo.predict(X_test)
            resultados_cv[nombre]["test_accuracy"] = round(accuracy_score(y_test, y_pred), 4)
            resultados_cv[nombre]["test_f1_weighted"] = round(f1_score(y_test, y_pred, average='weighted'), 4)
            modelos_entrenados[nombre] = (modelo, y_pred, y_test)
            print(f"   {nombre}: CV F1={scores.mean():.4f} +/- {scores.std():.4f} | Test Acc={resultados_cv[nombre]['test_accuracy']}")

        print("\nConsultando a Mistral para seleccion de modelo...")
        decision = self.seleccionar_con_mistral(resultados_cv, clases)

        print(f"\nModelo seleccionado: {decision['modelo_seleccionado']}")
        print(f"Razon: {decision['razon']}")
        if decision.get('alerta'):
            print(f"Alerta: {decision['alerta']}")

        self.mejor_nombre = decision["modelo_seleccionado"]
        self.mejor_modelo, y_pred_final, y_test_final = modelos_entrenados[self.mejor_nombre]

        self.metricas = {
            "modelo": self.mejor_nombre,
            "clases": clases,
            "accuracy": round(accuracy_score(y_test_final, y_pred_final), 4),
            "precision_weighted": round(precision_score(y_test_final, y_pred_final, average='weighted'), 4),
            "recall_weighted": round(recall_score(y_test_final, y_pred_final, average='weighted'), 4),
            "f1_weighted": round(f1_score(y_test_final, y_pred_final, average='weighted'), 4),
            "cv_resultados": resultados_cv,
            "decision_mistral": decision
        }
        self.reporte_detallado = classification_report(
            y_test_final, y_pred_final, target_names=clases
        )

        print(f"\nMetricas finales ({self.mejor_nombre}):")
        print(f"   Accuracy:      {self.metricas['accuracy']}")
        print(f"   Precision (w): {self.metricas['precision_weighted']}")
        print(f"   Recall (w):    {self.metricas['recall_weighted']}")
        print(f"   F1-Score (w):  {self.metricas['f1_weighted']}")
        print(f"\nReporte por clase:\n{self.reporte_detallado}")

        return self.metricas, self.mejor_modelo


agente2 = AgenteEntrenador(client, MODEL)
metricas, modelo_final = agente2.entrenar(X, y, clases_target)
