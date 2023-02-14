import bpy, mathutils


#　override function
def get_override(area_type, region_type):
    for area in bpy.context.screen.areas: 
        if area.type == area_type:             
            for region in area.regions:                 
                if region.type == region_type:                    
                    override = {'area': area, 'region': region} 
                    return override
    #error message if the area or region wasn't found
    raise RuntimeError("Wasn't able to find", 
                        region_type,
                        " in area ", 
                        area_type,
                        " Make sure it's open while executing script.")



def transform(transvalue=1.5708,taransaxis="X",minustranmormbool=0):
    #　Save the settings in advance.
    pibotpoint=bpy.context.scene.tool_settings.transform_pivot_point
    cursorloc=bpy.context.scene.cursor.location.xyz
    

    #　Sets the reference cursor position.
    bpy.context.scene.cursor.location.xyz = mathutils.Vector((0,0,0))
    if minustranmormbool == True:
        transvalue=-1.5708


    #we need to override the context of our operator    
    override = get_override( 'VIEW_3D', 'WINDOW' )

    bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
    area = [area for area in bpy.context.screen.areas if area.type == "VIEW_3D"][0]

    bpy.ops.transform.rotate(override,value=-transvalue, orient_axis=taransaxis,)

    bpy.context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
    bpy.ops.transform.rotate(override,value = transvalue, orient_axis=taransaxis,)
    

    #　Restore settings.
    bpy.context.scene.tool_settings.transform_pivot_point = pibotpoint
    bpy.context.scene.cursor.location.xyz = cursorloc












