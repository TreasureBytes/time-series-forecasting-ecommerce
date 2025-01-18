import sys
import os

def setup_path():
    # Get the root directory (where main.ipynb is located)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.append(project_root)

setup_path()
