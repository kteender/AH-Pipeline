import sys

#from scratchpad import TEMPLATE_PATH
MODULE_PATH = "D:\\_CURRENT\\AH\\AH_pipeline"
sys.path.append(MODULE_PATH)

import os
import subprocess
import shlex
import datetime
import logging
import imp
import json
import maya.cmds as mc
import maya_portion as mp
import maya.utils
imp.reload(mp)
BLENDER_PATH = "C:\\Program Files\\Blender Foundation\\Blender 3.1\\blender.exe"
#TEMPLATE_PATH = "D:\\_CURRENT\\AH\\pipelineTest\\renderingTestScene12_fullRigTestImageComposite.blend"
#TEMPLATE_PATH = "D:\\_CURRENT\\AH\\pipelineTest\\demoFile_base.blend"
TEMPLATE_PATH = "D:\\_CURRENT\\AH\\AH_pipeline\\_template.blend"
OUTPUT_PATH = "D:\\_CURRENT\\AH\\outputs\\"
SCRIPTS_PATH = "D:\\_CURRENT\\AH\\AH_pipeline\\"

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
    """wd is a directory. Returns the files for the materials and the abc cache"""
    #Check for multiple visible cameras
    camL = mp.get_rigged_camera_transform()
    if len(camL) > 1:
        projLogger.critical("More than one visible camera! Please hide cameras you don't want rendered")
        quit()
    
    #Export materials JSON
    jsonFile01 = "materials.json"
    jsonPath01 = os.path.join(wd, jsonFile01)
    jsonObj01 = mp.create_selected_mat_dict()
    projLogger.info(jsonObj01)
    with open(jsonPath01, 'w') as f:
        f.write(json.dumps(jsonObj01, indent=4))
    
    #Export lights JSON
    jsonFile02 = "lights.json"
    jsonPath02 = os.path.join(wd, jsonFile02)
    jsonObj02 = mp.create_selected_light_dict()
    projLogger.info(jsonObj02)
    with open(jsonPath02, 'w') as f:
        f.write(json.dumps(jsonObj02, indent=4))

    #Export the alembic cache
    abcFile = "scene_cache.abc"
    abcPath = os.path.join(wd, abcFile)
    abcCmd = mp.create_abc_export_cmd() + abcPath
    mc.AbcExport( j = abcCmd)  
    return jsonPath01, jsonPath02, abcPath


def launch_blender(*args):
    #pass in flags as str
    blender = BLENDER_PATH
    if sys.version_info[0] >= 3:
        extension = ""
        for a in args:
            extension += (" %s" % (a))
        sp3 = blender + extension
        subprocess.run(sp3)
    else:
        sp2 = [BLENDER_PATH]
        for a in args:
            sp2.append(a)
        print(sp2)
        #subprocess.Popen([BLENDER_PATH, TEMPLATE_PATH, '--python', 'blender_potion.py'])
        subprocess.Popen(sp2)

    #print(sp)

#C:\Program Files\Blender Foundation\Blender 3.1\blender.exe --background D:\_CURRENT\AH\pipelineTest\demoFile_base.blend --python blender_portion.py -- -p1 D:\_CURRENT\AH\outputs\220626\114133\materials.json -p2 D:\_CURRENT\AH\outputs\220626\114133\scene_cache.abc
#launch_blender('--background', TEMPLATE_PATH, '--python', 'scratchpad.py')

#myLogger.warning('is when this event was logged.')
#mp.test_log()
#logging_setup()
workingDirectory = folder_prep()
materialsPath, lightsPath, alembicPath = maya_exports(workingDirectory)
var1 = materialsPath
var2 = lightsPath
var3 = alembicPath
#launch_blender('--background', TEMPLATE_PATH, '--debug', '--python', os.path.join(SCRIPTS_PATH,'blender_portion.py'), '--', '-p1', var1, '-p2', var2, '-p3', var3)
launch_blender(TEMPLATE_PATH, '--python', os.path.join(SCRIPTS_PATH,'blender_portion.py'), '--', '-p1', var1, '-p2', var2, '-p3', var3)
