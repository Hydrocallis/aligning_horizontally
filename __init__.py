
bl_info = {
    "name": "Aligning Horizontally",
    "description": " ",
    "author": "Hydrocallis",
    "version": (1, 0, 0),
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


def dimensionlist(self,seleobj):
    xlist =[]
    ylist =[]

    for i in seleobj:
        xlist.append(i.dimensions[0]+self.myfloatvector[0])
        ylist.append(i.dimensions[1]+self.myfloatvector[1])

    return xlist,ylist


def loc(self,seleobj,xlist=[],ylist=[],aligining=2, numreturntotal=0,ynumreturntotal=0): 
    # ※numretuntotalの値はグループの改行ごとに加算されていく
    
    selelen = len(seleobj)
    # 何回Y軸に改行するか
    kirisute = (selelen//aligining)+1
    ylocdeme =ynumreturntotal+self.myfloatvector2[1]
    xlocdeme =self.myfloatvector2[0]
    #　Y軸のカウント変数
    ynumreturn=0

    for count,i in enumerate(seleobj):

 
        if self.mybool == True:
            i.location[2] =0+self.myfloatvector[2]
        else:
            i.location[2] =i.location[2]+self.myfloatvector[2]
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
                # print('###1',count,aligining,selelen)

                pass
        # グループ内での改行(Y軸)の条件式

        for j in range(kirisute):
            #指定した並び以上になったらY軸へ改行する分岐
            if count >=aligining*j:
    
                i.location[1] = (max(ylist))*j+ylocdeme
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


def gropu_align(self):
    objlist=[]
    seleobj=bpy.context.selected_objects
    xlist,ylist = dimensionlist(self,seleobj)

    for i in seleobj:
        objlist.append({"object":i,"spltname":i.name.split('.', 1)[0]})

    sortlist =[]

    # 下記2つはグループの改行移動量
    numreturntotal=0
    ynumreturntotal=0
    
    for object, spltname in gropuping(objlist):
        
        for name in spltname:
            sortlist.append(name['object'])
        #次のグループの横への改行移動量
        xlist,ylist=dimensionlist(self,seleobj)

        #　ここから各グループごとのオブジェクトを整列していく。
        numreturn = loc(self,
                            seleobj=sortlist, 
                            xlist=xlist,
                            ylist=ylist,
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
            if len(sortlist) % self.myint == 0:
                print ("偶数です")
                yreturn-=1
            else:
                print ("奇数です")
            # if yreturn ==1:
            #     yreturn-=1

            ynumreturntotal=(yreturn*max(ylist))+ynumreturntotal
            print('###1',)
            print('###',self.myint,len(sortlist),yreturn,max(ylist),ynumreturntotal)
            print('###2',)

       

        sortlist.clear()


def look_obname(self):
    if self.look_obname==True:
        for ob in bpy.context.selectable_objects:
            ob.show_name = True

    else:
        for ob in bpy.context.selectable_objects:
            ob.show_name = False


def Align_sigle_gropu(self):
    numreturntotal=0
    seleobj=bpy.context.selected_objects
    
    seleobj.sort(key = lambda o: o.name)

    # ランダムに配置する
    if self.mybool3 == True:

        random.seed(self.myint2)
        random.shuffle(seleobj)

    xlist,ylist = dimensionlist(self,seleobj)


    loc(self,
        seleobj=seleobj, 
        xlist=xlist,
        ylist=ylist,
        aligining=self.myint,
        numreturntotal=numreturntotal,
            )   


def main_draw(self):
    layout = self.layout
    seleobj = bpy.context.selected_objects
    xlist,ylist = dimensionlist(self,seleobj)

    #　グループ数の合計を計算　開始
    objlist =[]
    a=0
    for i in seleobj:
        objlist.append({"object":i,"spltname":i.name.split('.', 1)[0]})

    for object, spltname in gropuping(objlist):
          a+=1
    #　グループ数の合計を計算　終了


    layout.label(text="Dimensition") 
    layout.label(text="x="+str(max(xlist)) )
    layout.label(text="y="+str(max(ylist)) )
    layout.label(text="Total number of groups="+str(a) )

    layout.prop(self, "myint" )
    layout.prop(self, "myfloatvector")
    layout.prop(self, "mybool" )
    layout.prop(self, "yaxisgroupret" )

    box =layout.box()
    box.prop(self, "mybool2" )
    box.prop(self, "mybool3" )
    box.prop(self, "myint2" )

    movebox =layout.box()
    movebox.label(text="Whole Movement") 
    movebox.prop(self, "myfloatvector2")
    layout.prop(self, "look_obname" )



    
def main(self, context):
    look_obname(self)

    if self.mybool2 != True:
        gropu_align(self)
    else:
        Align_sigle_gropu(self)
    

class AH_OP_Aligning_Horizontally(Operator):
    bl_idname = 'object.aligning_horizontally'
    bl_label = 'Aligning Horizontally'
    bl_description = f' CLASS_NAME_IS={sys._getframe().f_code.co_name}/n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n ' 
    bl_options = {'REGISTER', 'UNDO','PRESET'}
    
   
    myfloatvector:bpy.props.FloatVectorProperty(
        name='Relative Offset', 
        description='', 
        default=(0.0, 0.0, 0),
        subtype="XYZ_LENGTH"
        )
        
   
    myfloatvector2:bpy.props.FloatVectorProperty(
        name='Relative Offset', 
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
        name= "z to the origin",
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
    
    look_obname : bpy.props.BoolProperty(
        name= "Look Object name",# 
        default=0
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


def register():
    bpy.utils.register_class(AH_OP_Aligning_Horizontally)
    bpy.utils.register_class(AH_PT_Aligning_HorizontallyPanel)


def unregister():
    bpy.utils.unregister_class(AH_OP_Aligning_Horizontally)
    bpy.utils.unregister_class(AH_PT_Aligning_HorizontallyPanel)


if __name__ == "__main__":
    register()

  
                

