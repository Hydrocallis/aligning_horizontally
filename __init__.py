
bl_info = {
    "name": "Aligning Horizontally",
    "description": " ",
    "author": "Hydrocallis",
    "version": (1, 0, 5),
    "blender": (3, 2, 0),
    "location": "View3D > Sidebar > KSYN Tab",
    "warning": "",
    # "doc_url": "",
    "category": "Object"
    }

import bpy,sys, bmesh
from mathutils import Vector

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )

import random
from bpy.props import IntProperty,BoolProperty,FloatVectorProperty

# 他のモジュールを読み込み
from .utils.transformrotation import transform
from .utils.location import loc
from .utils.dimension import dimensionlist
from .utils.draw import main_draw
from .utils.get_translang import get_translang
from .utils.propaty import AH_OP_Aligning_Horizontally_propaty
from .utils.gropu_align import GropuAlign
from .utils.only_parent_object import only_selct_parent_object



# リロードモジュール　開始
def reload_unity_modules(name):
    import os
    import importlib
   
    utils_modules = sorted([name[:-3] for name in os.listdir(os.path.join(__path__[0], "utils")) if name.endswith('.py')])

    for module in utils_modules:
        impline = "from . utils import %s" % (module)

        # print("###hydoro unity reloading one %s" % (".".join([name] + ['utils'] + [module])))

        exec(impline)
        importlib.reload(eval(module))

    modules = []

    for path, module in modules:
        if path:
            impline = "from . %s import %s" % (".".join(path), module)
        else:
            impline = "from . import %s" % (module)

        print("###hydoro unity reloading second %s" % (".".join([name] + path + [module])))

        exec(impline)
        importlib.reload(eval(module))

if 'bpy' in locals():
    reload_unity_modules(bl_info['name'])
# リロードモジュール　終了
import bpy

from bpy.props import EnumProperty, BoolProperty, FloatProperty
from bpy.types import Operator
from mathutils import Euler
from bpy.props import PointerProperty
from bpy.types import Panel, Operator


class AH_PT_RandomMaterialOperator(Operator):
    bl_idname = "object.random_material"
    bl_label = "Random Face Material"
    
    def execute(self, context):
        # メッシュオブジェクトを取得
        obj = context.object
        
        # マテリアルスロットのリストを取得
        material_slots = obj.material_slots
        
        # MaterialObjectというオブジェクトのマテリアルスロットを取得
        matlist = [slot.material for slot in context.scene.aling_material_object.material_slots]
        
        # メッシュの各フェイスに対してランダムなマテリアルを割り当てる
        for face in obj.data.polygons:
            # ランダムなマテリアルスロットを選択
            random_material = random.choice(matlist)
            atc_matlist = [slot.material for slot in material_slots]
            
            # フェイスにマテリアルを割り当て
            if random_material not in atc_matlist:
                obj.data.materials.append(random_material)
                appendmat_index = material_slots[random_material.name].slot_index
            else:
                appendmat_index = material_slots[random_material.name].slot_index
            
            face.material_index = appendmat_index
        
        return {'FINISHED'}

class AH_OT_objarray(bpy.types.Operator):
    bl_idname = 'object.alin_easy_array'
    bl_label = 'ALing Array'
    bl_description = f' CLASS_NAME_IS={sys._getframe().f_code.co_name}/n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n '
    # 3Dで用のプロパティ
    bl_options = {'REGISTER', 'UNDO','PRESET'}
    
    count : bpy.props.IntProperty(
    name= "count",
    default=1
        )

    ro:bpy.props.FloatVectorProperty(
        name='Relative Offset', 
        description='', 
        default=(1.0, 0.0, 0),
        subtype="XYZ"
        )
        
    co:bpy.props.FloatVectorProperty(
        name='Constant Offset', 
        description='', 
        default=(0.0, 0.0, 0),
        subtype="XYZ_LENGTH"
        )    
            
    link_bool : bpy.props.BoolProperty(
        name="link"
        )

    @classmethod
    def poll(self, context):
        
        return  bpy.context.object
        
        

    def object_duplicate_array(self,):
        cobj = bpy.context.object
        selectedobjenamelist =  [i.name for i  in bpy.context.selected_objects]
        
        # if range ==0:
        x_dimension,y_dimension,z_dimension=cobj.dimensions
        # else:
        #     x_dimension,y_dimension,z_dimension=dimensionss
        value =  (x_dimension*self.ro[0]+self.co[0], 
                  y_dimension*self.ro[1]+self.co[1], 
                  z_dimension*self.ro[2]+self.co[2], 
                  )
        bpy.ops.object.duplicate_move(
            OBJECT_OT_duplicate={
                "linked":self.link_bool,
                "mode":'TRANSLATION'},
                TRANSFORM_OT_translate={
                                    "value":value, 
                                        }
                                    )


 
        return selectedobjenamelist

    def execute(self, context):
        for i in range(self.count):
            selectedobjenamelist = self.object_duplicate_array()
   


        return {'FINISHED'}

class AH_OP_ObjectAlignOperator(Operator):
    bl_idname = "align.next_width"
    bl_label = "Align Next Width Objects"
    bl_options = {'REGISTER', 'UNDO','PRESET'}

    direction: EnumProperty(
        name="Direction",
        items=[
            ("X", "X", "Move objects along the X-axis"),
            ("Y", "Y", "Move objects along the Y-axis"),
            ("Z", "Z", "Move objects along the Z-axis")
        ],
        default="X"
    )
    
    reverse_direction: BoolProperty(
        name="Reverse Direction",
        description="Reverse the direction of alignment",
        default=False
    )
    
    #SCALE

    scale_randam: BoolProperty(
        name="scale_randam",
        description="",
        default=False
    )

    scale_random_seed: bpy.props.IntProperty(
        name="Scale Random Seed",
        default=0
    )

    scale_min_scale: FloatVectorProperty(
        name="min_scale",
        description="min_scale",
        default=(1.0, 1.0, 1.0),

   
    )

    scale_max_scale: FloatVectorProperty(
        name="max_scale",
        description="max_scale",
        default=(1.0, 1.0, 1.0),
    )
    
    #ROTATION
    rotation_randam: BoolProperty(
        name="rotation_randam",
        description="",
        default=False
    )

    rotation_random_seed: bpy.props.IntProperty(
        name="Rotation Random Seed",
        default=0
    )

    min_rotation: bpy.props.FloatVectorProperty(
        name="Min Rotation",
        default=(0.0, 0.0, 0.0),
        subtype='EULER',
        size=3
    )
    max_rotation: bpy.props.FloatVectorProperty(
        name="Max Rotation",
        default=(0, 0, 0),
        subtype='EULER',
        size=3
    )
    
    
    # CAP
    gap: FloatProperty(
        name="Gap",
        description="Gap between objects",
        default=0.0,
    )

 
    def execute(self, context):
        seleobj = bpy.context.selected_objects
        sorted_obj = sorted(seleobj, key=lambda obj: obj.name)

        if self.scale_randam:
            random.seed(self.scale_random_seed)


            for index, obj in enumerate(sorted_obj):

                obj_scale_x = random.uniform(self.scale_min_scale[0], self.scale_max_scale[0])
                obj_scale_y = random.uniform(self.scale_min_scale[1], self.scale_max_scale[1])
                obj_scale_z = random.uniform(self.scale_min_scale[2], self.scale_max_scale[2])
                obj_scale = Euler((obj_scale_x, obj_scale_y, obj_scale_z), 'XYZ')
                obj.scale = obj_scale


            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
        if self.rotation_randam:
            random.seed(self.rotation_random_seed)

  
            # オブジェクトの回転を設定
            for index, obj in enumerate(sorted_obj):
                # ランダムな回転ベクターを生成
                rotation_x = random.uniform(self.min_rotation[0], self.max_rotation[0])
                rotation_y = random.uniform(self.min_rotation[1], self.max_rotation[1])
                rotation_z = random.uniform(self.min_rotation[2], self.max_rotation[2])
                rotation = Euler((rotation_x, rotation_y, rotation_z), 'XYZ')
                obj.rotation_euler = rotation

                # if self.direction == "X":
                #     obj.scale.x = random.uniform(self.rotation_min, self.rotation_max)
                # elif self.direction == "Y":
                #     obj.scale.y = random.uniform(self.rotation_min, self.rotation_max)
                # elif self.direction == "Z":
                #     obj.scale.z = random.uniform(self.rotation_min, self.rotation_max)

            # bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            # bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')



        seleobj = bpy.context.selected_objects
        sorted_obj = sorted(seleobj, key=lambda obj: obj.name)
        default_obj = bpy.context.object
        x_position = default_obj.location.x

    


        for index, obj in enumerate(sorted_obj):



            if self.direction == "X":
                obj.location.x = x_position
                obj.location.y = default_obj.location.y
                obj.location.z = default_obj.location.z
            elif self.direction == "Y":
                obj.location.x = default_obj.location.x
                obj.location.y = x_position
                obj.location.z = default_obj.location.z
            elif self.direction == "Z":
                obj.location.x = default_obj.location.x
                obj.location.y = default_obj.location.y
                obj.location.z = x_position
            
            if index < len(sorted_obj) - 1:
                if self.reverse_direction:
                    reverse = -1
                else:
                    reverse = 1
                if self.direction == "X":
                    x_position += (obj.dimensions.x + sorted_obj[index+1].dimensions.x + self.gap) / 2 * reverse
                elif self.direction == "Y":
                    x_position += (obj.dimensions.y + sorted_obj[index+1].dimensions.y + self.gap) / 2 * reverse
                elif self.direction == "Z":
                    x_position += (obj.dimensions.z + sorted_obj[index+1].dimensions.z + self.gap) / 2 * reverse
       
            
        return {'FINISHED'}

# グルーピングしないで整列
def Align_sigle_gropu(self):
    numreturntotal=0
    seleobj=bpy.context.selected_objects
    
    seleobj.sort(key = lambda o: o.name)

    # ランダムに配置する
    if self.mybool3 == True:
        random.seed(self.myint2)
        random.shuffle(seleobj)

    xlist,ylist,zlist = dimensionlist(self,seleobj)


    loc(self,
        seleobj=seleobj, 
        xlist=xlist,
        ylist=ylist,
        zlist=zlist,
        aligining=self.myint,
        numreturntotal=numreturntotal,
        
            )   

def look_obname(self):
    if self.look_obname==True:
        for ob in bpy.context.selectable_objects:
            ob.show_name = True

    else:
        for ob in bpy.context.selectable_objects:
            ob.show_name = False
    
def main(self, context):
    if self.only_parent_ojbect_select == True:
        only_selct_parent_object()
        
    if self.starting_from_an_active_object == True:
        self.filerst_obj_loc = bpy.context.object.location.xyz
    else:
        self.filerst_obj_loc = (0,0,0)

    look_obname(self)

    if self.mybool2 != True:
        gropu_align=GropuAlign()
        gropu_align.gropu_align(self)
    else:
        Align_sigle_gropu(self)

    if self.tranmormbool == True:
        transform(taransaxis=self.my_enum,minustranmormbool=self.minustranmormbool)

class AH_OP_Aligning_Horizontally(Operator,AH_OP_Aligning_Horizontally_propaty):
    bl_idname = 'object.aligning_horizontally'
    bl_label = get_translang('Aligning Horizontally','整列')
    bl_description = f' CLASS_NAME_IS={sys._getframe().f_code.co_name}/n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n ' 
    bl_options = {'REGISTER', 'UNDO','PRESET'}
    

                
    def execute(self, context):
        main(self, context)


        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None


    # def invoke(self, context, event):
    #     wm = context.window_manager
    #     return wm.invoke_props_dialog(self)


    def draw(self,context):
        main_draw(self,context)

class AH_PT_RandomMaterialPanel(Panel):
    bl_idname = "VIEW3D_PT_random_material"
    bl_label = "Random Material"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "KSYN"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.prop(scene, "aling_material_object", text="Material Object")
        layout.operator(AH_PT_RandomMaterialOperator.bl_idname)
        layout.operator("ksyn.random_material")



class AH_PT_Aligning_HorizontallyPanel(Panel):
    bl_label = get_translang("AH PANEL",'簡単整列')
    bl_idname = "AH_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "KSYN"


    def draw(self, context):

        layout = self.layout
        layout.operator("object.aligning_horizontally")
        layout.operator("align.next_width")
        layout.operator("object.alin_easy_array")

class AH_OP_RandomMaterialOperator(bpy.types.Operator):
    bl_idname = "ksyn.random_material"
    bl_label = "Random Material"
    bl_options = {'REGISTER', 'UNDO',}
    

    
    index_number: IntProperty(name="Index Number", default=1,soft_min =1,)
    random_seed: IntProperty(name="Random Seed", default=0)
    same_material: BoolProperty(name="Same Material", default=False)
    
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'MESH'
    
    def execute(self, context):
        # active_object = bpy.context.object
        selected_objects = bpy.context.selected_objects
        # objects_to_change = [obj for obj in selected_objects if obj != active_object]
        
        random.seed(self.random_seed)
        
        if self.same_material:
            random_material = random.choice(context.scene.aling_material_object.data.materials)
        
        for obj in selected_objects:
            if not self.same_material:
                random_material = random.choice(context.scene.aling_material_object.data.materials)
            try:
                obj.data.materials[self.index_number-1] = random_material
            except IndexError:
                self.report({'WARNING'}, f"Materials Out Of Range.MAX{len(obj.data.materials)}")

        return {'FINISHED'}

# 辞書登録関数　開始
import os,codecs,csv
def GetTranslationDict():
    dict = {}
    # 直下に置かれているcsvファイルのパスを代入
    path = os.path.join(os.path.dirname(__file__), "translation_dictionary.csv")
    with codecs.open(path, 'r', 'utf-8') as f:
        reader = csv.reader(f)
        dict['ja_JP'] = {}
        for row in reader:
            for context in bpy.app.translations.contexts:
                dict['ja_JP'][(context, row[1].replace('\\n', '\n'))] = row[0].replace('\\n', '\n')
    return dict
# 辞書登録関数　終わり

def register():
    bpy.utils.register_class(AH_OP_Aligning_Horizontally)
    bpy.utils.register_class(AH_OP_ObjectAlignOperator)
    bpy.utils.register_class(AH_OP_RandomMaterialOperator)
    bpy.utils.register_class(AH_OT_objarray)
    bpy.utils.register_class(AH_PT_Aligning_HorizontallyPanel)
    bpy.utils.register_class(AH_PT_RandomMaterialOperator)
    bpy.utils.register_class(AH_PT_RandomMaterialPanel)
    bpy.types.Scene.aling_material_object = PointerProperty(type=bpy.types.Object, name="Material Object", description="Select the Material Object")


 	# 翻訳辞書の登録
    try:
        translation_dict = GetTranslationDict()
        bpy.app.translations.register(__name__, translation_dict)
    except: pass

def unregister():
    bpy.utils.unregister_class(AH_OP_Aligning_Horizontally)
    bpy.utils.unregister_class(AH_OP_ObjectAlignOperator)
    bpy.utils.unregister_class(AH_OP_RandomMaterialOperator)
    bpy.utils.unregister_class(AH_OT_objarray)
    bpy.utils.unregister_class(AH_PT_Aligning_HorizontallyPanel)
    bpy.utils.unregister_class(AH_PT_RandomMaterialOperator)
    bpy.utils.unregister_class(AH_PT_RandomMaterialPanel)
    del bpy.types.Scene.aling_material_object
	# 翻訳辞書の登録解除
    try:
        bpy.app.translations.unregister(__name__)
    except: pass

if __name__ == "__main__":
    register()

  
                

