
import bpy
from .get_translang import get_translang

class ohter_option:
    only_parent_ojbect_select : bpy.props.BoolProperty(
        name= get_translang('Move only parent','親のみ移動'),# 
        default=False
        ) # type: ignore
    
class change_direction:
    yaxisgroupret : bpy.props.BoolProperty(
        name= "y axis group Return",# 
        default=0
        ) # type: ignore
    Z_axis_for_line_breaks : bpy.props.BoolProperty(
        name= "Z-axis for line breaks",# 
        default=0
        ) # type: ignore

    y_axis_direction_to_reverse : bpy.props.BoolProperty(
        name= get_translang('Y-axis direction to reverse','Y軸方向を反対へ'),# 
        default=False
        ) # type: ignore
    
    x_axis_direction_to_reverse : bpy.props.BoolProperty(
        name= get_translang('X-axis direction to the opposite direction','X軸方向を反対へ'),# 
        default=False
        ) # type: ignore
    
class AH_OP_Aligning_Horizontally_propaty(change_direction,ohter_option):
   
    myfloatvector:bpy.props.FloatVectorProperty(
        name='Constant Offset', 
        description='', 
        default=(0.0, 0.0, 0),
        subtype="XYZ_LENGTH"
        ) # type: ignore
        
    Adjustment_of_width_between_groups:bpy.props.FloatProperty(
        name=get_translang('Adjustment of width between groups','グループ間の幅の調整'),# 
        description='', 
        default=0.0,
        subtype="DISTANCE"
        ) # type: ignore
        
   
    myfloatvector2:bpy.props.FloatVectorProperty(
        name='Constant Offset', 
        description='', 
        default=(0.0, 0.0, 0),
        subtype="XYZ_LENGTH"
        ) # type: ignore
        
  
    myint : bpy.props.IntProperty(
       name= "alignment parameter",
       default=5,
       soft_min=1,
       ) # type: ignore
    
    myint2 : bpy.props.IntProperty(
       name= "Random Seed",
       default=0,
       soft_min=0,
       ) # type: ignore
    
    z_axis_return_number : bpy.props.IntProperty(
       name= get_translang("heap up in a heap","立体の奥行き数"),
       default=2,
       soft_min=1,
       ) # type: ignore

    to_origin : bpy.props.BoolProperty(
        name= get_translang("align vertically","縦軸を揃える"),
        default=True
        ) # type: ignore
    
    gropu_toge : bpy.props.BoolProperty(
        name= get_translang("Bringing Groups Together","全オブジェクトを整列"),# グループをまとめる
        default=0
        ) # type: ignore
    
    randam_all_gropu : bpy.props.BoolProperty(
        name= "Random",# 
        default=0
        ) # type: ignore
    

    
    look_obname : bpy.props.BoolProperty(
        name= "Look Object name",# 
        default=0
        ) # type: ignore
    
    tranmormbool : bpy.props.BoolProperty(
        name= "Rotate 90 degrees",# 
        default=0
        ) # type: ignore
    
    minustranmormbool : bpy.props.BoolProperty(
        name= "Minus the value of rotation",# 
        default=0
        ) # type: ignore
    
    starting_from_an_active_object : bpy.props.BoolProperty(
        name= get_translang('Starting from an active object','アクティブなオブジェクトを起点にする'),# 
        default=False
        ) # type: ignore

    Determine_the_width_for_each_group : bpy.props.BoolProperty(
        name= get_translang('Determine the width for each group','グループ毎に幅を決定する'),# 
        default=False
        ) # type: ignore
    
    Stacked_on_a_cube : bpy.props.BoolProperty(
        name= get_translang('Stacked on a cube','立方体上に積み重ねる'),# 
        default=True
        ) # type: ignore
    
    pass_act_obj : bpy.props.BoolProperty(
        name= get_translang('Active object is at the top of the sort','アクティブオブジェクトをソートの先頭にする'),# 
        default=False
        ) # type: ignore
    
    my_enum: bpy.props.EnumProperty(items= [
                               ('X', "X", "", 1),
                               ("Y", "Y", "", 2),
                               ("Z", "Z", "", 3),
                                   
                           ],
                           name="Axis",
                           default='X',
        ) # type: ignore
    