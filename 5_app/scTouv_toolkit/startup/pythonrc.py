import os
import sys

tool_root = os.environ.get("SC_TOUV_PATH", "")
if tool_root and tool_root not in sys.path:
    sys.path.append(tool_root)

try:
    import qt_test_scTouv
    qt_test_scTouv.launch_tool()
except ImportError as e:
    print("Could not launch tool:", e)
