import sys
MODULE_PATH = "D:\\_CURRENT\\AH\\AH_pipeline"
sys.path.append(MODULE_PATH)

import os
import subprocess
import datetime
import logging
import imp
import json
import maya.cmds as cmds
import maya_portion as mp
import maya.utils

imp.reload(mp)

BLENDER_PATH = "C:\\Program Files\\Blender Foundation\\Blender 3.1\\blender.exe"
#TEMPLATE_PATH = "D:\\_CURRENT\\AH\\pipelineTest\\renderingTestScene12_fullRigTestImageComposite.blend"
TEMPLATE_PATH = "D:\\_CURRENT\\AH\\pipelineTest\\demoFile_base.blend"
OUTPUT_PATH = "D:\\_CURRENT\\AH\\outputs\\"

def logging_setup():
    """Sets up project to use Maya's GUI logger"""
    projLogger = logging.getLogger("AHPipelineLogger")
    projLogger.propagate = False
    handler = maya.utils.MayaGuiLogHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(message)s")
    handler.setFormatter(formatter)
    projLogger.addHandler(handler)

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
    """wd is a directory"""
    #Export materials JSON
    jsonFile = "materials.json"
    jsonPath = os.path.join(wd, jsonFile)
    jsonObj = mp.create_selected_mat_json()
    with open(jsonPath, 'w') as f:
        f.write(json.dumps(jsonObj, indent="\t"))

    #Export the alembic cache
    abcFile = "scene_cache.abc"
    abcPath = os.path.join(wd, abcFile)
    abcCmd = mp.create_abc_export_cmd() + abcPath
    cmds.AbcExport( j = abcCmd)  
    return

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

#myLogger.warning('is when this event was logged.')
#mp.test_log()
logging_setup()
workingDirectory = folder_prep()
maya_exports(workingDirectory)
