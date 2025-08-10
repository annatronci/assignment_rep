#*********************************************************************
# content = scTouv_toolkit/qt_test_scTouv.py

# version = 0.0.1
# date = 2025-07-23

# hou to = widget.show()
# dependencies = hou, PySide2 or PySide6, QtWidgets, QtUiTools, QtCore, QtGui
# todos = add more functionality, improve error handling, and enhance UI

# license = None
# author = Anna Tronci <annatronci.com>
#*********************************************************************

"""
scTouv_toolkit: A toolkit for exporting scanned geometry with UVs in Houdini.

This module provides a Qt-based GUI for managing geometry export tasks,
including importing geometry files, checking UVs, and exporting to various formats
such as FBX, Alembic, and USD. It builds a network of nodes in Houdini to
facilitate these tasks and provides a user-friendly interface for artists and developers.

"""
    
    

import os
import hou

import json
from pathlib import Path

try:
    from PySide2 import QtWidgets, QtUiTools, QtCore, QtGui
except ImportError:
    from PySide6 import QtWidgets, QtUiTools, QtCore, QtGui

CONFIG_PATH = Path(__file__).parent / "config.json"

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

UI_FILENAME = config["UI_FILENAME"]
IMAGE_FILENAME = config["IMAGE_FILENAME"]
SUPPORTED_FORMATS = config["SUPPORTED_FORMATS"]
DEFAULT_EXPORT_PATH = config["DEFAULT_EXPORT_PATH"]
DEFAULT_QUAD_COUNT = config["DEFAULT_QUAD_COUNT"]


class BaseHoudiniToolkit:
    """
    Base class for Houdini toolkits with common UI and node-handling functionality.

    Benefits of parenting:
    - Centralizes common methods (UI loading, file importing, export handling).
    - Reduces code duplication across multiple tools.
    - Allows subclasses to override only the parts they need (e.g., network building).
    - Maintains consistency in UI and workflow for all derived tools.
    """

    def __init__(self, ui_filename, image_filename):
        self.obj = hou.node("/obj")
        self.geo = self.obj.node("geo1")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(script_dir, "houdini_tool")

        self.ui_path = os.path.join(base_path, ui_filename)
        self.image_path = os.path.join(base_path, "img", image_filename)
        self.widget = None

    def load_ui(self):
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(self.ui_path)
        file.open(QtCore.QFile.ReadOnly)
        widget = loader.load(file)
        file.close()

        if os.path.exists(self.image_path):
            widget.label.setPixmap(QtGui.QPixmap(self.image_path))

        return widget

    def import_geometry(self):
        path = QtWidgets.QFileDialog.getOpenFileName(
            None, "Select Geometry File",
            os.getcwd(),
            "Geometry Files (*.fbx *.abc *.usd *.obj);;All Files (*)"
        )[0]

        if path:
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
            rop = self.geo.node("usd_export1")
            parm_name = "lopoutput"
        else:
            print("Unknown format:", ext)
            return

        if not rop:
            print(f"ROP node for {ext} not found.")
            return

        output_path = os.path.join(DEFAULT_EXPORT_PATH, f"export.{ext}")
        rop.parm(parm_name).set(output_path)
        print(f"Exporting {ext} to  {output_path}")


class ScTouvToolkit(BaseHoudiniToolkit):
    """
    Specialized toolkit for importing, checking UVs, and exporting geometry in Houdini.

    Inherits from BaseHoudiniToolkit to reuse:
    - UI loading
    - geometry import/export
    - base Houdini node handling

    Why parenting improves this module:
    - Allows reuse of UI logic and export/import code across multiple toolkits.
    - Makes adding new specialized Houdini tools easier by only overriding the
      `build_network()` or `check_uvs()` methods.
    - Keeps specialized tools focused on their unique features while maintaining
      consistent behavior.
    """

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

        uv_transfer1 = self.geo.createNode("labs::uv_transfer", "uv_transfer1")
        uv_transfer1.setInput(0, quad_remesh1)
        uv_transfer1.setInput(1, transform2)

        rop_fbx1 = self.geo.createNode("rop_fbx", "rop_fbx1")
        rop_fbx1.setInput(0, uv_transfer1)

        rop_alembic1 = self.geo.createNode("rop_alembic", "rop_alembic1")
        rop_alembic1.setInput(0, uv_transfer1)

        usd_export1 = self.geo.createNode("usdexport", "usd_export1")
        usd_export1.setInput(0, uv_transfer1)

        out_high = self.geo.createNode("null", "OUT_EXP_HIGH")
        out_high.setInput(0, transform2)
        out_high.setDisplayFlag(False)

        out_obj = self.geo.createNode("null", "OUT_EXPORT_OBJ")
        out_obj.setInput(0, uv_transfer1)
        out_obj.setDisplayFlag(True)
        out_obj.setRenderFlag(True)

        self.geo.layoutChildren()

    def check_uvs(self):
        uv_node = hou.node("/obj/geo1/uv_transfer1")
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

    def launch(self):
        self.build_network()
        self.check_uvs()
        self.widget = self.load_ui()

        self.widget.btn_add.clicked.connect(lambda: self.export_geometry("fbx"))
        self.widget.btn_add_2.clicked.connect(lambda: self.export_geometry("abc"))
        self.widget.btn_add_3.clicked.connect(lambda: self.export_geometry("usd"))
        self.widget.btn_asset.clicked.connect(lambda: self.import_geometry())

        self.widget.show()


if __name__ == "__main__":
    tool = ScTouvToolkit()
    tool.launch()
