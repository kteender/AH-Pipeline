import maya.cmds as cmds

def get_timeline_start_stop():
    start = cmds.playbackOptions(q=True, ast=True)
    stop = cmds.playbackOptions(q=True, aet=True)
    return start, stop

def get_selected_objects():
    sel = cmds.ls(sl=True)
    selstr = []
    for s in sel:
        selstr.append(str(s))
    return selstr


def export_abc():
    start, stop = get_timeline_start_stop()
    objectsFlag = ""
    selected = get_selected_objects()
    path = "D:/_CURRENT/AH/AH_proj/cache/alembic/cube.abc"
    for s in selected:
        st = "-root |%s " % (s)
        objectsFlag += st 
    command = "-frameRange " + str(start) + " " + str(stop) +" -dataFormat ogawa " + objectsFlag + "-file " + path
    print(command)
    cmds.AbcExport( j = command)
    #command = "-frameRange " + start + " " + stop +" -uvWrite -worldSpace " + root + " -file " + save_name
    #abc export mel command: AbcExport -j "-frameRange 1 200 -dataFormat ogawa -root |pCube1 -file D:/_CURRENT/AH/AH_proj/cache/alembic/cube.abc";']
    #multi-object: AbcExport -j "-frameRange 1 120 -dataFormat ogawa -root |pSphere1 -root |pCube1 -file D:/_CURRENT/AH/AH_proj/cache/alembic/cube.abc";
    #get a namespace fetcher everntually
    return
export_abc()
