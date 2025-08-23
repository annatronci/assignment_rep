import sys, os

# Aggiungiamo la cartella lib al path
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

# Importiamo da Qt.py
from Qt import QtWidgets

# Creiamo una piccola finestra
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.setWindowTitle("Qt.py Test - Hello Anna!")
window.resize(300, 100)
window.show()

sys.exit(app.exec_())