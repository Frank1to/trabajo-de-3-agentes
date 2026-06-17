# ============================================================
# CELDA 2 - Configuracion de la API Key de Mistral
# Commit: feat: configuracion del cliente Mistral con API key segura
# ============================================================

# Se usa getpass para que la API key no quede visible en el notebook.
# La key se guarda en una variable de entorno para mayor seguridad.
# Modelo elegido: mistral-small-latest (rapido y economico).
# Se puede cambiar a mistral-large-latest para mayor capacidad.

import os
from getpass import getpass

MISTRAL_API_KEY = getpass("Ingresa tu Mistral API Key: ")
os.environ["MISTRAL_API_KEY"] = MISTRAL_API_KEY

MODEL = "mistral-small-latest"
print(f"Configurado. Modelo: {MODEL}")
