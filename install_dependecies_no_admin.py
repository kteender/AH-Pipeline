import subprocess
import sys
import os

python_exe = sys.executable

try:
    from PIL import Image
    lib = os.path.dirname(PIL.__file__)
    print("PIL is %s \n" % lib)
except:
    #Install the Pillow image processing library
    #Visit link below to ensure compatibility between Blender's python installation and Pillow
    #https://pillow.readthedocs.io/en/stable/installation.html
    subprocess.call([python_exe, "-m", "ensurepip"])
    subprocess.call([python_exe, "-m", "pip", "install", "pip"])
    subprocess.call([python_exe, '-m', 'pip', 'install', '--user', '--upgrade', 'Pillow'])

    import PIL
    lib = os.path.dirname(PIL.__file__)
    print("PIL is %s \n" % lib)
