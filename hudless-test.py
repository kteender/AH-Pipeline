import sys
import os

BLENDER_PATH = os.path("C:\Program Files\Blender Foundation\Blender 3.1\blender.exe")

def launch_blender(**kwargs):
    #pass in flags as str
    blender = BLENDER_PATH
    extension = ""
    for k in kwargs:
        extension.append(" %s" % (k))


launch_blender('--background', '--python', 'scratchpad.py')
