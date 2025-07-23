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

    Returns:
        _type_: _description_
    """
    
    
import os
import hou
try :
    from PySide2 import QtWidgets, QtUiTools, QtCore, QtGui
except :
    from PySide6 import QtWidgets, QtUiTools, QtCore, QtGui

def build_network():
    obj = hou.node("/obj")
    geo = obj.node("geo1")
    if not geo:
        geo = obj.createNode("geo", "geo1", run_init_scripts=False)
    else:
        for child in geo.children():
            if child.name() != "file1":
                child.destroy()

    file1 = geo.node("file1")
    if not file1:
        file1 = geo.createNode("file", "file1")
        file1.parm("file").set("")

    transform1 = geo.createNode("xform", "transform1")
    transform1.setInput(0, file1)

    box1 = geo.createNode("box", "box1")
    match_size1 = geo.createNode("matchsize", "matchsize1")
    match_size1.setInput(0, transform1)
    match_size1.setInput(1, box1)
    match_size1.parm("doscale").set(1)

    transform2 = geo.createNode("xform", "transform2")
    transform2.setInput(0, match_size1)

    quad_remesh1 = geo.createNode("quadremesh", "quad_remesh1")
    quad_remesh1.setInput(0, transform2)

    uv_transfer1 = geo.createNode("labs::uv_transfer", "uv_transfer1")
    uv_transfer1.setInput(0, quad_remesh1)
    uv_transfer1.setInput(1, transform2)

    rop_fbx1 = geo.createNode("rop_fbx", "rop_fbx1")
    rop_fbx1.setInput(0, uv_transfer1)

    rop_alembic1 = geo.createNode("rop_alembic", "rop_alembic1")
    rop_alembic1.setInput(0, uv_transfer1)

    usd_export1 = geo.createNode("usdexport", "usd_export1")
    usd_export1.setInput(0, uv_transfer1)

    out_high = geo.createNode("null", "OUT_EXP_HIGH")
    out_high.setInput(0, transform2)
    out_high.setDisplayFlag(False)

    out_obj = geo.createNode("null", "OUT_EXPORT_OBJ")
    out_obj.setInput(0, uv_transfer1)
    out_obj.setDisplayFlag(True)
    out_obj.setRenderFlag(True)

    geo.layoutChildren()

def check_uvs():
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
    
def export_geometry(ext):
    geo = hou.node("/obj/geo1")
    if ext == "fbx":
        rop = geo.node("rop_fbx1")
        parm_name = "sopoutput"
    elif ext == "abc":
        rop = geo.node("rop_alembic1")
        parm_name = "filename"
    elif ext == "usd":
        rop = geo.node("usdexport1")
        parm_name = "lopoutput"
    else:
        print("Unknown format:", ext)
        return

    if not rop:
        return
        

def launch_tool():
    build_network()
    check_uvs()

    def load_ui(path):
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(path)
        file.open(QtCore.QFile.ReadOnly)
        widget = loader.load(file)
        file.close()
        return widget

    def import_geometry():
        path = QtWidgets.QFileDialog.getOpenFileName(
            None, "Select Geometry File", os.getcwd(), "Geometry Files (*.fbx *.abc *.usd *.obj);;All Files (*)"
        )[0]
        if path:
            geo = hou.node("/obj/geo1")
            file_node = geo.node("file1")
            file_node.parm("file").set(path)
            print(f"Imported geometry: {path}")
            return path
        return ""

    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, "houdini_tool")
    ui_path = os.path.join(base_path, "scTouv.ui")
    image_path = os.path.join(base_path, "img", "SCtoUV.png")

    widget = load_ui(ui_path)

    if os.path.exists(image_path):
        widget.label.setPixmap(QtGui.QPixmap(image_path))

    def on_export_fbx():
        export_geometry("fbx")

    def on_export_abc():
        export_geometry("abc")

    def on_export_usd():
        export_geometry("usd")

    def on_import_geometry():
        widget.edt_asset.setText(import_geometry())

    widget.btn_add.clicked.connect(on_export_fbx)
    widget.btn_add_2.clicked.connect(on_export_abc)
    widget.btn_add_3.clicked.connect(on_export_usd)
    widget.btn_asset.clicked.connect(on_import_geometry)

    widget.show()
