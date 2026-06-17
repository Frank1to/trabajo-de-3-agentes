# ============================================================
# CELDA 1 - Instalacion de dependencias
# Commit: feat: instalacion de librerias necesarias (mistralai, sklearn, pandas)
# ============================================================

# Se instala mistralai v1.2.5 de forma forzada para evitar conflictos
# con versiones anteriores que usan MistralClient (deprecado).
# Tambien se instalan pandas, scikit-learn y numpy para el pipeline de ML.

!pip install mistralai==1.2.5 --force-reinstall -q
!pip install pandas scikit-learn numpy -q
