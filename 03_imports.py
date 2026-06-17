# ============================================================
# CELDA 3 - Imports y cliente Mistral
# Commit: feat: importacion de librerias y inicializacion del cliente Mistral
# ============================================================

# Se importan todas las librerias necesarias para el pipeline:
# - mistralai: cliente oficial para la API de Mistral AI
# - pandas/numpy: manipulacion de datos
# - re: expresiones regulares para limpiar strings sucios del dataset
# - sklearn: modelos de ML, metricas y preprocesamiento
# Se inicializa el cliente Mistral con la key configurada en la celda anterior.

import pandas as pd
import numpy as np
import json
import re
from mistralai import Mistral

from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, classification_report
)
import warnings
warnings.filterwarnings('ignore')

client = Mistral(api_key=MISTRAL_API_KEY)
print("Imports listos")
print(f"Cliente Mistral inicializado con modelo: {MODEL}")
