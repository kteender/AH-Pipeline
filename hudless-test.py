import sys
import os
import subprocess
import datetime
import maya.cmds as cmds

BLENDER_PATH = "C:\\Program Files\\Blender Foundation\\Blender 3.1\\blender.exe"
#TEMPLATE_PATH = "D:\\_CURRENT\\AH\\pipelineTest\\renderingTestScene12_fullRigTestImageComposite.blend"
TEMPLATE_PATH = "D:\\_CURRENT\\AH\\pipelineTest\\demoFile_base.blend"
OUTPUT_PATH = "D:\\_CURRENT\\AH\\outputs\\"

def folder_prep():
    now = datetime.datetime.now()
    dayStr = datetime.datetime.strftime(now, "%y%m%d")
    nowStr = datetime.datetime.strftime(now, "%H%M%S")
    dayDir = os.path.join(OUTPUT_PATH,dayStr)
    nowDir = os.path.join(dayDir, nowStr)
    if not os.path.exists(dayDir):
        os.mkdir(dayDir)
    os.mkdir(nowDir)
    return(nowDir)

def maya_exports(wd):
    #wd = str directory


def launch_blender(*args):
    #pass in flags as str
    blender = BLENDER_PATH
    extension = ""
    for k in args:
        extension += (" %s" % (k))
    sp = blender + extension
    subprocess.run(sp)
    print(sp)


#launch_blender('--background', TEMPLATE_PATH, '--python', 'scratchpad.py')
workingDirectory = folder_prep()
