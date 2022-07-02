import bpy

def apply_material_to_object(obj, mat):
    if len(obj.material_slots) < 1:
        obj.data.materials.append(mat)
    else:
        obj.material_slots[0].material = mat
    return

def create_material_from_dict(matName, d):
    mats = bpy.data.materials
    bpy.data.materials.new()