# ============================================================
# CELDA 5 - Funciones de limpieza de datos
# Commit: feat: funciones para parsear strings sucios (rangos, unidades, precios)
# ============================================================

# El Cars Dataset 2025 tiene todos sus valores como strings con formato inconsistente:
#   - Numeros con unidades:  "963 hp", "340 km/h", "800 Nm", "3990 cc"
#   - Rangos de valores:     "70-85 hp", "$12,000-$15,000", "100-140 Nm"
#   - Precios con simbolos:  "$460,000", "$1,100,000"
#   - Asientos con errores:  "215", "78", "2+2" (valores imposibles)
#   - Fuel Types inconsist.: "plug in hyrbrid", "Hybrid (Petrol)", "Gas / Hybrid"
#
# Estrategia: extraer el valor numerico promediando rangos cuando los hay.

def extraer_numero(valor):
    """
    Extrae numero de strings sucios. Si hay un rango (ej: '70-85'), promedia.
    Elimina simbolos de moneda, unidades y comas de miles.
    """
    if pd.isna(valor):
        return np.nan
    s = str(valor).replace(',', '').replace('$', '').replace('hp', '') \
                   .replace('km/h', '').replace('sec', '').replace('Nm', '') \
                   .replace('cc', '').replace('kWh', '').strip()
    nums = re.findall(r'\d+\.?\d*', s)
    if not nums:
        return np.nan
    return np.mean([float(n) for n in nums])


def limpiar_seats(valor):
    """
    Limpia columna Seats eliminando valores imposibles (ej: 215, 78).
    Convierte '2+2' a 4. Solo acepta valores entre 1 y 20.
    """
    if pd.isna(valor):
        return np.nan
    s = str(valor).strip()
    if s == '2+2':
        return 4
    try:
        n = int(s)
        return n if 1 <= n <= 20 else np.nan
    except:
        return np.nan


def normalizar_fuel(valor):
    """
    Agrupa las 23 variantes inconsistentes de Fuel Types en 7 categorias limpias.
    Ej: 'plug in hyrbrid', 'Hybrid/Plug-in' -> 'Plug-in Hybrid'
    """
    v = str(valor).lower().strip()
    if 'electric' in v or 'ev' in v:
        return 'Electric'
    if 'plug' in v:
        return 'Plug-in Hybrid'
    if 'hybrid' in v:
        return 'Hybrid'
    if 'diesel' in v and 'petrol' in v:
        return 'Petrol/Diesel'
    if 'diesel' in v:
        return 'Diesel'
    if 'hydrogen' in v or 'cng' in v or 'gas' in v:
        return 'Other'
    return 'Petrol'


print("Funciones de limpieza definidas")
print("   - extraer_numero(): parsea strings con unidades y rangos")
print("   - limpiar_seats(): elimina valores imposibles en Seats")
print("   - normalizar_fuel(): agrupa 23 variantes en 7 categorias")
