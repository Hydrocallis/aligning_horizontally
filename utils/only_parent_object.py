import bpy

def only_selct_parent_object():
    actobj = bpy.context.object
    seleobj= bpy.context.selected_objects

    bpy.ops.object.select_hierarchy(direction='CHILD', extend=False)

    chidobjs= bpy.context.selected_objects


    bpy.ops.object.select_all(action='DESELECT')
    for obj in seleobj:
        if obj in chidobjs:
            pass
        else:
            obj.select_set(True)
        if obj == actobj:
            bpy.context.view_layer.objects.active = obj


        