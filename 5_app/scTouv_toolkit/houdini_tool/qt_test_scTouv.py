# #*********************************************************************
# # content = scTouv_toolkit/qt_test_scTouv.py

# # version = 0.0.1
# # date = 2025-07-23

# # hou to = widget.show()
# # dependencies = hou, PySide2 or PySide6, QtWidgets, QtUiTools, QtCore, QtGui
# # todos = add more functionality, improve error handling, and enhance UI

# # license = None
# # author = Anna Tronci <annatronci.com>
# #*********************************************************************

# """
# scTouv_toolkit: A toolkit for exporting scanned geometry with UVs in Houdini.

# This module provides a Qt-based GUI for managing geometry export tasks,
# including importing geometry files, checking UVs, and exporting to various formats
# such as FBX, Alembic, and USD. It builds a network of nodes in Houdini to
# facilitate these tasks and provides a user-friendly interface for artists and developers.

# """
    


import sys
import json
import os
import hou
from pathlib import Path

try:
    from PySide2 import QtWidgets, QtUiTools, QtCore, QtGui
except ImportError:
    from PySide6 import QtWidgets, QtUiTools, QtCore, QtGui

# ---- Configuration ----
CONFIG_PATH = Path(__file__).parent / "config.json"
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

UI_FILENAME = config.get("UI_FILENAME", "scTouv.ui")
IMAGE_FILENAME = config.get("IMAGE_FILENAME", "SCtoUV.png")
SUPPORTED_FORMATS = config.get("SUPPORTED_FORMATS", ["fbx", "abc", "usd"])
DEFAULT_EXPORT_PATH = config.get("DEFAULT_EXPORT_PATH", str(Path.home()))
DEFAULT_QUAD_COUNT = config.get("DEFAULT_QUAD_COUNT", 5000)

# ---- Base Houdini Toolkit ----
class BaseHoudiniToolkit:
    def __init__(self, ui_filename, image_filename):
        self.obj = hou.node("/obj")
        self.geo = self.obj.node("geo1")
        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.ui_path = os.path.join(script_dir, ui_filename)
        self.image_path = os.path.join(script_dir, "img", image_filename)
        self.widget = None

    def load_ui(self):
        if not os.path.exists(self.ui_path):
            raise RuntimeError(f"UI file not found: {self.ui_path}")

        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(self.ui_path)
        file.open(QtCore.QFile.ReadOnly)
        widget = loader.load(file)
        file.close()

        # Main Logo 
        if hasattr(widget, "label") and os.path.exists(self.image_path):
            widget.label.setPixmap(QtGui.QPixmap(self.image_path))

        return widget

    def import_geometry(self):
        start_dir = os.path.dirname(self.widget.edtPath.text()) if hasattr(self.widget, "edtPath") and self.widget.edtPath.text() else os.getcwd()

        path = QtWidgets.QFileDialog.getOpenFileName(
            self.widget, "Select Geometry File",
            start_dir,
            "Geometry Files (*.fbx *.abc *.usd *.obj);;All Files (*)"
        )[0]

        if path:
            if hasattr(self.widget, "edtPath"):
                self.widget.edtPath.setText(path)

            if not self.geo:
                self.geo = self.obj.createNode("geo", "geo1", run_init_scripts=False)

            file_node = self.geo.node("file1")
            if file_node:
                file_node.parm("file").set(path)
                print(f"Imported geometry: {path}")
                return path
        return ""

    def export_geometry(self, ext):
        rop = None
        parm_name = ""

        if ext == "fbx":
            rop = self.geo.node("rop_fbx1")
            parm_name = "sopoutput"
        elif ext == "abc":
            rop = self.geo.node("rop_alembic1")
            parm_name = "filename"
        elif ext == "usd":
            # FIX: USD node is in LOP network, not in geo!
            lopnet = self.obj.node("LOP_EXPORT")
            if lopnet:
                rop = lopnet.node("usd_rop1")
                parm_name = "lopoutput"
            else:
                print("LOP_EXPORT network not found.")
                return
        else:
            print("Unknown format:", ext)
            return

        if not rop:
            print(f"ROP node for {ext} not found.")
            return

        initial_dir = DEFAULT_EXPORT_PATH if os.path.isdir(DEFAULT_EXPORT_PATH) else str(Path.home())
        suggested_name = f"export.{ext}"
        initial_path = os.path.join(initial_dir, suggested_name)

        selected_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.widget,
            f"Save {ext.upper()} File",
            initial_path,
            f"{ext.upper()} Files (*.{ext});;All Files (*)"
        )

        if not selected_path:
            print("Export canceled")
            return

        if not selected_path.lower().endswith(f".{ext}"):
            selected_path = selected_path + f".{ext}"

        # Configuration USD
        if ext == "usd":
            # Set output path
            rop.parm(parm_name).set(selected_path)
            # Set parameters only for USD ROP
            if rop.parm("trange"):
                rop.parm("trange").set(0)  # Current frame
            
        else:
            rop.parm(parm_name).set(selected_path)

        print(f"Exporting {ext} to {selected_path}")

        try:
            rop.render()
            # USD file creation check
            if ext == "usd" and os.path.exists(selected_path):
                print(f"Export {ext} completed successfully.")
            elif ext != "usd":
                print(f"Export {ext} completed.")
        except Exception as e:
            # Special case for USD export warnings
            if ext == "usd" and os.path.exists(selected_path):
                print(f"Export {ext} completed successfully (warning ignored).")
            else:
                print(f"Error while export {ext}: {e}")

# ---- Specialized Toolkit ----
class ScTouvToolkit(BaseHoudiniToolkit):
    def __init__(self):
        super().__init__("scTouv.ui", "SCtoUV.png")

    def build_network(self):
        if not self.geo:
            self.geo = self.obj.createNode("geo", "geo1", run_init_scripts=False)
        else:
            for child in self.geo.children():
                if child.name() != "file1":
                    child.destroy()

        file1 = self.geo.node("file1")
        if not file1:
            file1 = self.geo.createNode("file", "file1")
            file1.parm("file").set("")

        transform1 = self.geo.createNode("xform", "transform1")
        transform1.setInput(0, file1)

        box1 = self.geo.createNode("box", "box1")
        match_size1 = self.geo.createNode("matchsize", "matchsize1")
        match_size1.setInput(0, transform1)
        match_size1.setInput(1, box1)
        match_size1.parm("doscale").set(1)

        transform2 = self.geo.createNode("xform", "transform2")
        transform2.setInput(0, match_size1)

        quad_remesh1 = self.geo.createNode("quadremesh", "quad_remesh1")
        quad_remesh1.setInput(0, transform2)
        quad_remesh1.parm("targetquadcount").set(DEFAULT_QUAD_COUNT)

        uv_transfer1 = self.geo.createNode("labs::uv_transfer", "uv_transfer1")
        if not uv_transfer1:
            uv_transfer1 = self.geo.createNode("uvunwrap", "uv_transfer1")
        uv_transfer1.setInput(0, quad_remesh1)
        uv_transfer1.setInput(1, transform2)

        rop_fbx1 = self.geo.createNode("rop_fbx", "rop_fbx1")
        rop_fbx1.setInput(0, uv_transfer1)

        rop_alembic1 = self.geo.createNode("rop_alembic", "rop_alembic1")
        rop_alembic1.setInput(0, uv_transfer1)

        lopnet = self.obj.node("LOP_EXPORT")
        if not lopnet:
            lopnet = self.obj.createNode("lopnet", "LOP_EXPORT")

        usd_rop = lopnet.node("usd_rop1")
        if not usd_rop:
            usd_rop = lopnet.createNode("usd_rop", "usd_rop1")

        usd_import = lopnet.node("sopimport1")
        if not usd_import:
            usd_import = lopnet.createNode("sopimport", "sopimport1")
            usd_import.parm("soppath").set(self.geo.path() + "/uv_transfer1")
            usd_import.setDisplayFlag(True)
            usd_import.setCurrent(True, clear_all_selected=True)

        usd_rop.setInput(0, usd_import)

        out_high = self.geo.createNode("null", "OUT_EXP_HIGH")
        out_high.setInput(0, transform2)
        out_high.setDisplayFlag(False)

        out_obj = self.geo.createNode("null", "OUT_EXPORT_OBJ")
        out_obj.setInput(0, uv_transfer1)
        out_obj.setDisplayFlag(True)
        out_obj.setRenderFlag(True)

        self.geo.layoutChildren()
        lopnet.layoutChildren()

    def check_uvs(self):
        uv_node = self.geo.node("uv_transfer1")
        if not uv_node:
            print("uv_transfer1 not found.")
            return

        geo = uv_node.geometry()
        if not geo:
            print("No geometry found on uv_transfer1.")
            return

        if geo.findPrimAttrib("uv"):
            print("UVs are present.")
        else:
            print("No UVs found.")

    def set_quad_count(self):
        text = self.widget.editQuad.text().strip()
        try:
            count = float(text)
        except Exception:
            print("Invalid quad count input")
            return

        quad_node = self.geo.node("quad_remesh1")
        if quad_node:
            quad_node.parm("targetquadcount").set(count)
            print(f"Quad count set to {count}")

    def launch(self):
        self.build_network()
        self.check_uvs()
        self.widget = self.load_ui()

        if hasattr(self.widget, "btnFbx"):
            self.widget.btnFbx.clicked.connect(lambda: self.export_geometry("fbx"))
        if hasattr(self.widget, "btnAbc"):
            self.widget.btnAbc.clicked.connect(lambda: self.export_geometry("abc"))
        if hasattr(self.widget, "btnUsd"):
            self.widget.btnUsd.clicked.connect(lambda: self.export_geometry("usd"))
        if hasattr(self.widget, "btnImport"):
            self.widget.btnImport.clicked.connect(lambda: self.import_geometry())

        if hasattr(self.widget, "editQuad"):
            self.widget.editQuad.editingFinished.connect(self.set_quad_count)

        # Force loading icon in lblQuad
        try:
            if hasattr(self.widget, "lblQuad"):
                quad_icon_path = str(Path(__file__).parent / "img" / "quad_remesh.jpg")
                if os.path.exists(quad_icon_path):
                    pix = QtGui.QPixmap(quad_icon_path).scaled(
                        24, 24, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
                    )
                    self.widget.lblQuad.setPixmap(pix)
        except Exception as e:
            print(f"Impossibile impostare iconcina lblQuad: {e}")

        self.widget.show()


if __name__ == "__main__":
    tool = ScTouvToolkit()
    tool.launch()

def launch_tool():
    tool = ScTouvToolkit()
    tool.launch()