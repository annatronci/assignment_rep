import os
import sys
from Qt import QtCompat, QtWidgets


class ReferenceApp:
    def __init__(self):
        # Build absolute path to the UI file inside "ui" folder
        base_dir = os.path.dirname(__file__)
        ui_file = os.path.join(base_dir, "ui", "referenceApp.ui")
        
        # Load UI
        self.win = QtCompat.loadUi(ui_file)
        self.win.show()

        # ---- Connect signals to slots (example, adapt to your widgets) ----
        if hasattr(self.win, "btnScreenshot"):
            self.win.btnScreenshot.clicked.connect(self.take_screenshot)
        if hasattr(self.win, "btnOptions"):
            self.win.btnOptions.clicked.connect(self.show_options)
        if hasattr(self.win, "btnSave"):
            self.win.btnSave.clicked.connect(self.save_file)
        if hasattr(self.win, "btnPublish"):
            self.win.btnPublish.clicked.connect(self.publish_file)

    # ---- Slots ----
    def take_screenshot(self):
        print("📸 Screenshot button pressed")

    def show_options(self):
        print("⚙️ Options button pressed")

    def save_file(self):
        path = self.win.txtPath.text()
        print(f"💾 Save pressed. Path: {path}")

    def publish_file(self):
        publish = self.win.chkPublish.isChecked()
        print(f"🚀 Publish pressed. Publish to server? {publish}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = ReferenceApp()
    sys.exit(app.exec_())

