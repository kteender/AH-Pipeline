import subprocess
import sys
import os
import imp

import bpy
python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
target = os.path.join(sys.prefix, 'lib', 'site-packages')
sys.path.append("D:\\_CURRENT\\AH\\AH_pipeline\\")
import blender_py_utils as utils
imp.reload(utils)

try:
    from PIL import Image
except:
    #Install the Pillow image processing library
    #Visit link below to ensure compatibility between Blender's python installation and Pillow
    #https://pillow.readthedocs.io/en/stable/installation.html
    subprocess.call([python_exe, "-m", "ensurepip", "--user"])
    subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.call([python_exe, '-m', 'pip', 'install', '--upgrade', 'Pillow', '-t', target])
    from PIL import Image