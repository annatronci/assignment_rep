# author : Anna Tronci
# Executed on Houdini startup

print(">>> pythonrc.py loaded!")

import os
import sys
import inspect

# Safely get directory of this script
this_file = inspect.getfile(inspect.currentframe())
this_dir = os.path.dirname(os.path.abspath(this_file))

# Add parent directory to sys.path (so we can import call_me.py)
houdini_tool_path = os.path.abspath(os.path.join(this_dir, ".."))


if houdini_tool_path not in sys.path:
    sys.path.insert(0, houdini_tool_path)

# Try to import your startup checker
try:
    import call_me
    call_me.check_startup()
except Exception as e:
    print(">>> ERROR importing call_me:", e)

# Debug: check if toolbar path exists
toolbar_path = os.path.join(hou.getenv("HOUDINI_USER_PREF_DIR"), "toolbar")
print(">>> toolbar path exists:", os.path.exists(toolbar_path))







