import sys
import os

# Otteniamo la cartella base (scTouv_toolkit/)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Percorso alla cartella houdini_tool/
HOUDINI_TOOL_PATH = os.path.join(BASE_DIR, "houdini_tool")

# Aggiungi al sys.path solo se non già presente
if HOUDINI_TOOL_PATH not in sys.path:
    sys.path.insert(0, HOUDINI_TOOL_PATH)

# Importa il tuo modulo principale
try:
    import qt_test_scTouv
except ImportError as e:
    print("[scTouv] Errore importando qt_test_scTouv:", e)
else:
    print("[scTouv] Toolkit caricato con successo.")
