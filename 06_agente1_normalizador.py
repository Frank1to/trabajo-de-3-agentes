# ============================================================
# CELDA 6 - Agente 1: Normalizador
# Commit: feat: Agente 1 - Normalizador que consulta a Mistral la estrategia de preprocesamiento
# ============================================================

# El Agente 1 tiene dos responsabilidades:
#   1. Consultar a Mistral AI con la info del dataset para obtener
#      una estrategia de preprocesamiento recomendada por el LLM.
#   2. Ejecutar esa estrategia: limpiar, imputar, escalar y codificar.
#
# Pasos del preprocesamiento aplicado:
#   - Normalizacion del target (Fuel Types): 23 variantes -> 7 categorias
#   - Eliminacion de columnas de alta cardinalidad (Cars Names, Engines)
#   - Label Encoding de Company Names (37 marcas)
#   - Extraccion de numeros de columnas sucias (CC, HP, Speed, etc.)
#   - Limpieza de Seats (outliers absurdos)
#   - Imputacion de nulos con mediana (robusto frente a autos de lujo outliers)
#   - Escalado con StandardScaler

class AgenteNormalizador:
    def __init__(self, client, model):
        self.client = client
        self.model = model
        self.nombre = "AGENTE 1 - Normalizador"
        self.scaler = StandardScaler()
        self.label_encoder_target = LabelEncoder()
        self.estrategia_mistral = None

    def consultar_mistral(self, info_dataset):
        prompt = f"""
Sos un experto en preprocesamiento de datos para machine learning.
Analiza este dataset de autos y devuelve SOLO un JSON con observaciones y estrategia.

Info del dataset:
{json.dumps(info_dataset, indent=2)}

Devuelve EXACTAMENTE este JSON (sin texto adicional, sin markdown):
{{
  "observaciones": "descripcion breve del estado del dataset",
  "columnas_a_eliminar": ["col1"],
  "imputacion_numericas": "mean o median",
  "recomendacion_target": "recomendacion sobre el target Fuel Types",
  "riesgos": "posibles problemas a considerar"
}}
"""
        response = self.client.chat.complete(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        texto = response.choices[0].message.content.strip()
        texto = texto.replace("```json", "").replace("```", "").strip()
        return json.loads(texto)

    def procesar(self, df, target_col):
        print(f"\n{'='*60}")
        print(f"{self.nombre}")
        print(f"{'='*60}")

        info = {
            "filas": int(df.shape[0]),
            "columnas": list(df.columns),
            "nulos": df.isnull().sum().to_dict(),
            "ejemplo_fila": df.iloc[0].to_dict(),
            "nota": "Todos los valores son strings sucios con unidades, rangos y simbolos de moneda"
        }

        print("Consultando a Mistral para analisis del dataset...")
        self.estrategia_mistral = self.consultar_mistral(info)
        print("\nAnalisis de Mistral:")
        print(json.dumps(self.estrategia_mistral, indent=2, ensure_ascii=False))

        df_clean = df.copy()

        print(f"\nNormalizando columna objetivo '{target_col}'...")
        df_clean[target_col] = df_clean[target_col].apply(normalizar_fuel)
        print(df_clean[target_col].value_counts().to_string())

        cols_eliminar = ['Cars Names', 'Engines']
        df_clean.drop(columns=cols_eliminar, inplace=True)
        print(f"\nColumnas eliminadas: {cols_eliminar}")

        le_company = LabelEncoder()
        df_clean['Company Names'] = le_company.fit_transform(df_clean['Company Names'].astype(str))
        print("Company Names codificado (37 marcas)")

        cols_num_sucias = ['CC/Battery Capacity', 'HorsePower', 'Total Speed',
                           'Performance(0 - 100 )KM/H', 'Cars Prices', 'Torque']
        print("\nLimpiando columnas numericas...")
        for col in cols_num_sucias:
            df_clean[col] = df_clean[col].apply(extraer_numero)
            print(f"   {col}: {df_clean[col].isnull().sum()} nulos restantes")

        df_clean['Seats'] = df_clean['Seats'].apply(limpiar_seats)
        print("   Seats: limpiado (outliers absurdos eliminados)")

        cols_num = cols_num_sucias + ['Seats']
        metodo = self.estrategia_mistral.get('imputacion_numericas', 'median')
        print(f"\nImputando nulos con {metodo}...")
        for col in cols_num:
            if df_clean[col].isnull().sum() > 0:
                val = df_clean[col].mean() if metodo == 'mean' else df_clean[col].median()
                df_clean[col].fillna(val, inplace=True)
                print(f"   {col}: imputado con {val:.2f}")

        y = df_clean[target_col].copy()
        X = df_clean.drop(columns=[target_col])

        X[cols_num] = self.scaler.fit_transform(X[cols_num])
        print(f"\nEscaladas con StandardScaler: {cols_num}")

        y_encoded = self.label_encoder_target.fit_transform(y)
        clases = list(self.label_encoder_target.classes_)
        print(f"\nClases del target: {clases}")
        print(f"\nDataset limpio: {X.shape[0]} filas x {X.shape[1]} features")

        return X, y_encoded, clases


agente1 = AgenteNormalizador(client, MODEL)
X, y, clases_target = agente1.procesar(df_original, TARGET_COLUMN)
