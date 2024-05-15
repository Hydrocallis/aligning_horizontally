
bl_info = {
    "name": "Aligning Horizontally",
    "description": " ",
    "author": "Hydrocallis",
    "version": (1, 1, 2),
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



# リロードモジュール　開始
def reload_unity_modules(name):
    import os
    import importlib
   
    utils_modules = sorted([name[:-3] for name in os.listdir(os.path.join(__path__[0], "utils")) if name.endswith('.py')])

    for module in utils_modules:
        impline = "from . utils import %s" % (module)


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

# 他のモジュールを読み込み
from .utils.transformrotation import transform
from .utils.location import loc
from .utils.dimension import dimensionlist
from .utils.draw import main_draw
from .utils.get_translang import get_translang
from .utils.propaty import AH_OP_Aligning_Horizontally_propaty
from .utils.gropu_align import GropuAlign
from .utils.only_parent_object import only_selct_parent_object
from . import addon_updater_ops

# リロードモジュール　終了


import bpy

from bpy.props import EnumProperty, BoolProperty, FloatProperty
from bpy.types import Operator
from mathutils import Euler
from bpy.props import PointerProperty,StringProperty
from bpy.types import Panel, Operator,AddonPreferences



class UpdaterProps:
    
    auto_check_update : bpy.props.BoolProperty(
		name="Auto-check for Update",
		description="If enabled, auto-check for updates using an interval",
		default=False) # type: ignore

    updater_interval_months : bpy.props.IntProperty(
		name='Months',
		description="Number of months between checking for updates",
		default=0,
		min=0)# type: ignore

    updater_interval_days : bpy.props.IntProperty(
		name='Days',
		description="Number of days between checking for updates",
		default=7,
		min=0,
		max=31)# type: ignore

    updater_interval_hours : bpy.props.IntProperty(
		name='Hours',
		description="Number of hours between checking for updates",
		default=0,
		min=0,
		max=23)# type: ignore

    updater_interval_minutes : bpy.props.IntProperty(
		name='Minutes',
		description="Number of minutes between checking for updates",
		default=0,
		min=0,
		max=59)# type: ignore

class KSYNAlingnHorizonaddonPreferences(AddonPreferences,UpdaterProps):

    bl_idname = __package__

    split_string: StringProperty(
        name=get_translang("String of criteria to be arrayed","配列する基準の文字列"),
        default=".",

        )# type: ignore
    



    def draw(self, context):
        layout = self.layout
        addon_prefs = context.preferences.addons["aligning_horizontally"].preferences
        layout.prop(addon_prefs, "split_string")
        addon_updater_ops.update_settings_ui(self, context)


# オペレーター

class AH_OP_ObjectAlignOperator(Operator):
    bl_idname = "align.next_width"
    bl_label = get_translang("Align Next Width Objects",'直列配列機能')
    bl_options = {'REGISTER', 'UNDO','PRESET'}

    direction: EnumProperty(
        name=get_translang("Direction",'方向'),
        items=[
            ("X", "X", "Move objects along the X-axis"),
            ("Y", "Y", "Move objects along the Y-axis"),
            ("Z", "Z", "Move objects along the Z-axis")
        ],
        default="X"
    ) # type: ignore
    
    reverse_direction: BoolProperty(
        name=get_translang("Reverse Direction",'逆方向'),
        description="Reverse the direction of alignment",
        default=False
    ) # type: ignore

    randam_shuffle: BoolProperty(
        name=get_translang("Randam Shuffle",'順序の入れ替え'),
        description="Randam Shuffle",
        default=False
    ) # type: ignore

    shuffle_random_seed: bpy.props.IntProperty(
        name=get_translang("shuffle Random Seed",'シード'),
        default=0
    ) # type: ignore
    
    #SCALE

    scale_randam: BoolProperty(
        name=get_translang("scale_randam",'スケールをランダム化'),
        description="",
        default=False
    ) # type: ignore

    scale_random_seed: bpy.props.IntProperty(
        name=get_translang("Scale Random Seed",'シード'),
        default=0
    ) # type: ignore

    scale_min_scale: FloatVectorProperty(
        name="min_scale",
        description="min_scale",
        default=(1.0, 1.0, 1.0),

   
    ) # type: ignore

    scale_max_scale: FloatVectorProperty(
        name="max_scale",
        description="max_scale",
        default=(1.0, 1.0, 1.0),
    ) # type: ignore
    
    #ROTATION
    rotation_randam: BoolProperty(
        name=get_translang("rotation_randam",'回転のランダム化'),
        description="",
        default=False
    ) # type: ignore

    rotation_random_seed: bpy.props.IntProperty(
        name=get_translang("Rotation Random Seed",'シード'),
        default=0
    ) # type: ignore

    min_rotation: bpy.props.FloatVectorProperty(
        name="Min Rotation",
        default=(0.0, 0.0, 0.0),
        subtype='EULER',
        size=3
    ) # type: ignore
    max_rotation: bpy.props.FloatVectorProperty(
        name="Max Rotation",
        default=(0, 0, 0),
        subtype='EULER',
        size=3
    ) # type: ignore
    
    
    # CAP
    gap: FloatProperty(
        name=get_translang("Gap",'オブジェトの距離'),
        description="Gap between objects",
        default=0.0,
    ) # type: ignore

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        seleobj = bpy.context.selected_objects
        # print('###1',seleobj)
        if self.randam_shuffle:
            random.seed(self.shuffle_random_seed)
            random.shuffle(seleobj)
            # print('###2',seleobj)
            sorted_obj = seleobj
        else:
            sorted_obj = sorted(seleobj, key=lambda obj: obj.name)



        if self.scale_randam:
            random.seed(self.scale_random_seed)


            for index, obj in enumerate(sorted_obj):

                obj_scale_x = random.uniform(self.scale_min_scale[0], self.scale_max_scale[0])
                obj_scale_y = random.uniform(self.scale_min_scale[1], self.scale_max_scale[1])
                obj_scale_z = random.uniform(self.scale_min_scale[2], self.scale_max_scale[2])
                obj_scale = (obj_scale_x, obj_scale_y, obj_scale_z)
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

        seleobj = bpy.context.selected_objects
        # sorted_obj = sorted(seleobj, key=lambda obj: obj.name)
        default_obj = bpy.context.object
        if self.direction == "X":
            x_position = default_obj.location.x
        elif self.direction == "Y":
            x_position = default_obj.location.y
        elif self.direction == "Z":
            x_position = default_obj.location.z


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

class AH_OP_Aligning_Horizontally(Operator,AH_OP_Aligning_Horizontally_propaty):
    bl_idname = 'object.aligning_horizontally'
    bl_label = get_translang('Aligning Horizontally','整列')
    bl_description = f' CLASS_NAME_IS={sys._getframe().f_code.co_name}/n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n ' 
    bl_options = {'REGISTER', 'UNDO','PRESET'}
        
    # グルーピングしないで整列
    def Align_sigle_gropu(self):
        numreturntotal=0
        seleobj = bpy.context.selected_objects
        act_obj = bpy.context.active_object

        # act_obj.name を先頭に持ってくるためのソート関数
        def custom_sort(obj):
            if obj == act_obj:
                return -1  # act_obj を最初に持ってくる
            else:
                return 0

        # ソートする
        seleobj.sort(key=lambda o: o.name)
        if self.pass_act_obj:  # pass_act_obj が True の場合
            seleobj.sort(key=custom_sort)
        

        # ランダムに配置する
        if self.randam_all_gropu == True:
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

    # 名前の表示
    def lookobname(self):
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

        self.lookobname()

        if self.gropu_toge != True:
            gropu_align=GropuAlign()
            gropu_align.gropu_align(self)
        else:
            self.Align_sigle_gropu()

        if self.tranmormbool == True:
            transform(taransaxis=self.my_enum,minustranmormbool=self.minustranmormbool)

                
    def execute(self, context):
        self.main(context)


        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None


    def draw(self,context):
        main_draw(self,context)

class KSYNAH_OPAddonPreferences(bpy.types.Operator):
    bl_idname = "ksynah.open_addonpreferences"
    bl_label = "Open Addon Preferences"

    cmd: bpy.props.StringProperty(default="", options={'HIDDEN'}) # type: ignore


    def execute(self, context):


        preferences = bpy.context.preferences
        addon_prefs = preferences.addons["aligning_horizontally"].preferences

        bpy.ops.screen.userpref_show("INVOKE_DEFAULT")
        preferences.active_section = 'ADDONS'
        bpy.ops.preferences.addon_expand(module = "aligning_horizontally")
        bpy.ops.preferences.addon_show(module = "aligning_horizontally")

        return {'FINISHED'}


# パネル

class AH_PT_Aligning_HorizontallyPanel(Panel):
    bl_label = get_translang("AH PANEL",'簡単整列')
    bl_idname = "AH_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "KSYN"


    def draw(self, context):

        layout = self.layout

        layout.operator("ksynah.open_addonpreferences",text="Setting",  icon="TOOL_SETTINGS")
        layout.operator("object.aligning_horizontally")
        layout.operator("align.next_width")


class AH_PT_Aligning_Horizontallyhelppanel(Panel):
    bl_label = get_translang("AH Help",'簡単整列 助けて')
    bl_idname = "AH_PT_PANEL_help"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "KSYN"

    def split_by_n(self, string, n):
        result = [string[i:i+n] for i in range(0, len(string), n)]
        return result

    def longtext_set(self, context,layout,long_text):
            # Get 3D viewport area
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    break

            # Automatically set the width of the UI region to the width of the panel
            for region in area.regions:
                if region.type == 'UI':
                    panel_width = region.width
                    break

            # Calculate the maximum width of the label
            font_scale= 15
            uifontscale = font_scale * context.preferences.view.ui_scale
            max_label_width = int(panel_width // uifontscale)

            save_alignment=layout.alignment

            layout.alignment = 'RIGHT'
            box = layout.box()
            # Split the text into lines and format each line
            for line in long_text.splitlines():
                # Remove leading and trailing whitespace
                line = line.strip()

                # Split the line into chunks that fit within the maximum label width
                
                for chunk in self.split_by_n(line, max_label_width):

                # for chunk in textwrap.wrap(line, width=max_label_width, break_long_words=False, break_on_hyphens=False):
                    box.label(text=chunk)
            layout.alignment = save_alignment
    
    def draw(self, context):

        layout = self.layout
        
        layout.label(text= get_translang("1 alignment",'1 整列'))
        long_text = get_translang("If the objects are to be aligned horizontally, rotate the objects in advance.",
                                  '横向きにに並べる場合はオブジェクトの回転を事前に適応しておくこと。')
        self.longtext_set(context,layout,long_text)
        self.longtext_set(context,layout,long_text)

register_cls=[
    KSYNAH_OPAddonPreferences,
    AH_OP_Aligning_Horizontally,
    AH_OP_ObjectAlignOperator,
    AH_PT_Aligning_HorizontallyPanel,
    KSYNAlingnHorizonaddonPreferences,
    AH_PT_Aligning_Horizontallyhelppanel,
    ]

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
    addon_updater_ops.register(bl_info)

    for reg_cl in register_cls:
        bpy.utils.register_class(reg_cl)
 

 	# 翻訳辞書の登録
    try:
        translation_dict = GetTranslationDict()
        bpy.app.translations.register(__name__, translation_dict)
    except: pass


def unregister():
    addon_updater_ops.unregister()

    for reg_cl in register_cls:

        bpy.utils.unregister_class(reg_cl)

	# 翻訳辞書の登録解除
    try:
        bpy.app.translations.unregister(__name__)
    except: pass


if __name__ == "__main__":
    register()

  
                

