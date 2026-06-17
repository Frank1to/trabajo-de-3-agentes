# ============================================================
# CELDA 4 - Carga del dataset Cars 2025
# Commit: feat: carga del Cars Dataset 2025 desde zip con manejo de encoding latin1
# ============================================================

# El dataset viene comprimido en archive.zip.
# Se usa zipfile para extraer el CSV directamente en Colab sin pasos manuales.
# Problemas encontrados y soluciones aplicadas:
#   - Encoding: el CSV usa latin1 (no utf-8), contiene caracteres especiales
#   - Lineas corruptas: algunas filas tienen comas dentro de valores -> on_bad_lines='skip'
#   - Parser: se usa engine='python' que es mas tolerante que el parser C por defecto

from google.colab import files
import zipfile

print("Subi el archivo archive.zip")
uploaded = files.upload()
filename = list(uploaded.keys())[0]

with zipfile.ZipFile(filename, 'r') as z:
    csv_name = [f for f in z.namelist() if f.endswith('.csv')][0]
    z.extract(csv_name)
    print(f"Extraido: {csv_name}")

df_original = pd.read_csv(
    csv_name,
    encoding='latin1',
    on_bad_lines='skip',
    sep=',',
    quotechar='"',
    engine='python'
)

TARGET_COLUMN = "Fuel Types"

print(f"Dataset cargado: {df_original.shape[0]} filas x {df_original.shape[1]} columnas")
print(f"Columna objetivo: {TARGET_COLUMN}")
print(f"Columnas: {list(df_original.columns)}")
display(df_original.head())
