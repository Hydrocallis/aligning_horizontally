
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

import bpy,sys
from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )

import random

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

class AH_PT_Aligning_HorizontallyPanel(Panel):
    bl_label = get_translang("AH PANEL",'簡単整列')
    bl_idname = "AH_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "KSYN"


    def draw(self, context):

        layout = self.layout
        layout.operator("object.aligning_horizontally")

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
    bpy.utils.register_class(AH_PT_Aligning_HorizontallyPanel)

 	# 翻訳辞書の登録
    try:
        translation_dict = GetTranslationDict()
        bpy.app.translations.register(__name__, translation_dict)
    except: pass

def unregister():
    bpy.utils.unregister_class(AH_OP_Aligning_Horizontally)
    bpy.utils.unregister_class(AH_PT_Aligning_HorizontallyPanel)

	# 翻訳辞書の登録解除
    try:
        bpy.app.translations.unregister(__name__)
    except: pass

if __name__ == "__main__":
    register()

  
                

