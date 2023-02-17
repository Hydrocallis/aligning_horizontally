
bl_info = {
    "name": "Aligning Horizontally",
    "description": " ",
    "author": "Hydrocallis",
    "version": (1, 0, 2),
    "blender": (3, 2, 0),
    "location": "View3D > Sidebar > AH Tab",
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

from itertools import groupby
import random

# 他のモジュールを読み込み
from .utils.transformrotation import transform

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


def dimensionlist(self,seleobj):
    xlist =[]
    ylist =[]
    zlist =[]


    for i in seleobj:
        xlist.append(i.dimensions[0]+self.myfloatvector[0])
        ylist.append(i.dimensions[1]+self.myfloatvector[1])
        zlist.append(i.dimensions[2]+self.myfloatvector[2])


    return xlist,ylist,zlist


def loc(self, seleobj, xlist=[], ylist=[], zlist=[], aligining=2, numreturntotal=0, ynumreturntotal=0): 
    # ※numretuntotalの値はグループの改行ごとに加算されていく
    yaxis=1
    subreturn=yaxis
    subreturnmax=max(ylist)
    depth = 2
    depthmax=max(zlist)

    if self.Z_axis_for_line_breaks== True:
        subreturn=depth
        subreturnmax=depthmax
        depth=yaxis

    
    selelen = len(seleobj)
    # 何回Y軸に改行するか
    kirisute = (selelen//aligining)+1
    
    returnlocdeme =ynumreturntotal+self.myfloatvector2[subreturn]
    xlocdeme =self.myfloatvector2[0]
    #　Y軸のカウント変数
    ynumreturn=0


    for count,i in enumerate(seleobj):

 
        # 奥行きの位置
        if self.mybool == True:
            i.location[depth] =self.myfloatvector[depth]
        else:
            i.location[depth] =i.location[depth]+self.myfloatvector[depth]


        # グループの初回のXの位置　以降は位置がプラスされていく
        if count == 0:
            i.location[0] =numreturntotal+self.myfloatvector2[0]
            pass
        else:
             # グループの初回以降のXの位置
            xlocdeme = xlocdeme+max(xlist)
            if count !=0:
                i.location[0] = xlocdeme+numreturntotal
            elif count+1 ==selelen:
                pass


        # グループ内での改行(Y軸)の条件式
        for j in range(kirisute):
            #指定した並び以上になったらY軸へ改行する分岐
            if count >=aligining*j:
    
                i.location[subreturn] = (subreturnmax)*j+returnlocdeme
                ynumreturn+=1
            

        # 改行後のXの位置の演算
        if len(seleobj) != 1:
            for j in range(kirisute): 
                if count+1 == aligining*j:
                    xlocdeme = self.myfloatvector2[0]-max(xlist)

        
    return ynumreturn
              

def gropuping(objlist):
    objlist.sort(key=lambda x: x['spltname'])
    outputlist = groupby(objlist, key=lambda x: x['spltname'])
    return outputlist

#　グループの位置の処理関係
def gropu_align(self):
    objlist=[]
    seleobj=bpy.context.selected_objects
    xlist,ylist,zlist = dimensionlist(self,seleobj)

    for i in seleobj:
        objlist.append({"object":i,"spltname":i.name.split('.', 1)[0]})

    sortlist =[]

    # 下記2つはグループの改行移動量
    numreturntotal=0
    ynumreturntotal=0
    
    for object, spltname in gropuping(objlist):
        
        for name in spltname:
            sortlist.append(name['object'])

         # グループピングしたソートリストをグループ毎にランダムに配置する
        if self.mybool3 == True:
            random.seed(self.myint2)
            random.shuffle(sortlist)

        #次のグループの横への改行移動量
        xlist,ylist,zlist=dimensionlist(self,seleobj)

        


        #　ここから各グループごとのオブジェクトを整列していく。
        numreturn = loc(self,
                            seleobj=sortlist, 
                            xlist=xlist,
                            ylist=ylist,
                            zlist=zlist,
                            aligining=self.myint,
                            numreturntotal=numreturntotal,
                            ynumreturntotal=ynumreturntotal,
                    
                            )
        
        # ここがグループの改行移動関数 ※　これ、今思えばオブジェクト数と横列数を割って商がでなければって条件式つくればいいだけだったのでは…
        if self.yaxisgroupret != True:
            if self.myint >= numreturn: 
                # 一つのグループないのオブジェクト数が指定の指定の数を超えたら※つまり改行は存在しない
                #一行のトータルの値しかｘ軸に移動しない
                numreturntotal=numreturn*(max(xlist))+numreturntotal
                
            else:
                # 改行があるということは指定の数の並びであるという事だからｘ軸の長さは「指定の数×寸法」という計算式である
                numreturntotal=self.myint*(max(xlist))+numreturntotal
        
        elif self.yaxisgroupret == True:
            yreturn=(len(sortlist)//self.myint)+1
            # 割り切れる行はあまりの列が無いので一つ改行を減らしておく
            if len(sortlist) % self.myint == 0:
                # print ("偶数です")
                yreturn-=1
            else:
                # print ("奇数です")
                pass

            #　グループ改行の幅の判定
            if self.Z_axis_for_line_breaks== True:
                
                ynumreturntotal=(yreturn*max(zlist))+ynumreturntotal
            else:

                ynumreturntotal=(yreturn*max(ylist))+ynumreturntotal

        sortlist.clear()

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


def main_draw(self):
    layout = self.layout
    seleobj = bpy.context.selected_objects
    xlist,ylist,zlist = dimensionlist(self,seleobj)

    #　グループ数の合計を計算　開始
    objlist =[]
    a=0
    for i in seleobj:
        objlist.append({"object":i,"spltname":i.name.split('.', 1)[0]})

    for object, spltname in gropuping(objlist):
          a+=1
    #　グループ数の合計を計算　終了

    layout.prop(self, "look_obname" )
    layout.label(text="Dimensition") 
    layout.label(text="x="+str(max(xlist)))
    layout.label(text="y="+str(max(ylist)))
    layout.label(text="Total number of groups")
    layout.label(text=str(a) )

    layout.prop(self, "myint" )
    # layout.label(text="Note: z-axis is not available.")

    layout.prop(self, "myfloatvector")
    layout.prop(self, "mybool" )
    layout.prop(self, "yaxisgroupret" )
    layout.prop(self, "Z_axis_for_line_breaks" )

    layout.prop(self, "mybool2" )
    layout.prop(self, "mybool3" )
    layout.prop(self, "myint2" )

    movebox =layout.box()
    movebox.label(text="Whole Movement") 
    movebox.prop(self, "myfloatvector2")

    transrotatebox =layout.box()
    transrotatebox.prop(self, "tranmormbool" )
    transrotatebox.prop(self, "minustranmormbool" )
    grid = layout.grid_flow(row_major=True, columns=3, even_columns=True, even_rows=True, align=True)
    grid.prop(self, "my_enum",  expand=True )

    
def main(self, context):

    look_obname(self)

    if self.mybool2 != True:
        gropu_align(self)
    else:
        Align_sigle_gropu(self)

    if self.tranmormbool == True:
        transform(taransaxis=self.my_enum,minustranmormbool=self.minustranmormbool)


class AH_OP_Aligning_Horizontally(Operator):
    bl_idname = 'object.aligning_horizontally'
    bl_label = 'Aligning Horizontally'
    bl_description = f' CLASS_NAME_IS={sys._getframe().f_code.co_name}/n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n ' 
    bl_options = {'REGISTER', 'UNDO','PRESET'}
    
   
    myfloatvector:bpy.props.FloatVectorProperty(
        name='Constant Offset', 
        description='', 
        default=(0.0, 0.0, 0),
        subtype="XYZ_LENGTH"
        )
        
   
    myfloatvector2:bpy.props.FloatVectorProperty(
        name='Constant Offset', 
        description='', 
        default=(0.0, 0.0, 0),
        subtype="XYZ_LENGTH"
        )
        
  
    myint : bpy.props.IntProperty(
       name= "alignment parameter",
       default=1,
       soft_min=1,
       )
    myint2 : bpy.props.IntProperty(
       name= "Random Seed",
       default=0,
       soft_min=0,

       )

    mybool : bpy.props.BoolProperty(
        name= "To the origin",
        default=0
        )
    mybool2 : bpy.props.BoolProperty(
        name= "Bringing Groups Together",# グループをまとめる
        default=0
        )
    mybool3 : bpy.props.BoolProperty(
        name= "Random",# 
        default=0
        )
    yaxisgroupret : bpy.props.BoolProperty(
        name= "y axis group Return",# 
        default=0
        )
    Z_axis_for_line_breaks : bpy.props.BoolProperty(
        name= "Z-axis for line breaks",# 
        default=0
        )
    
    look_obname : bpy.props.BoolProperty(
        name= "Look Object name",# 
        default=0
        )
    
    tranmormbool : bpy.props.BoolProperty(
        name= "Rotate 90 degrees",# 
        default=0
        )
    
    minustranmormbool : bpy.props.BoolProperty(
        name= "Minus the value of rotation",# 
        default=0
        )
    
    my_enum: bpy.props.EnumProperty(items= [
                               ('X', "X", "", 1),
                               ("Y", "Y", "", 2),
                               ("Z", "Z", "", 3),
                                   
                           ],
                           name="Axis",
                           default='X',
                           )


                
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
        main_draw(self)


class AH_PT_Aligning_HorizontallyPanel(Panel):
    bl_label = "AH PANEL"
    bl_idname = "AH_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AH"


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

  
                

