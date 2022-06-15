import maya.cmds as cmds

def get_timeline_start_stop():
    start = cmds.playbackOptions(q=True, ast=True)
    stop = cmds.playbackOptions(q=True, aet=True)
    return start, stop

def export_abc():
    start, stop = get_timeline_start_stop()
    #abc export mel command: AbcExport -j "-frameRange 1 200 -dataFormat ogawa -root |pCube1 -file D:/_CURRENT/AH/AH_proj/cache/alembic/cube.abc";
    return
