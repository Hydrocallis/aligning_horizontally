import bpy
import random
from .gropuping import gropuping
from .dimension import dimensionlist
from .location import loc

def make_sortlists_dimension_list(self,sortlist):
    #次のグループの横への改行移動量
    if self.Determine_the_width_for_each_group != True:
       xlist,ylist,zlist=dimensionlist(self,self.seleobj)
    else:
        xlist,ylist,zlist=dimensionlist(self,sortlist)
    return xlist,ylist,zlist

# ここがグループの改行移動関数 ※　これ、今思えばオブジェクト数と横列数を割って商がでなければって条件式つくればいいだけだったのでは…
def return_gropu(self,numreturn,xlist,ylist,zlist,sortlist):
    if self.yaxisgroupret != True:
        if self.myint >= numreturn: 
            # 一つのグループないのオブジェクト数が指定の指定の数を超えたら※つまり改行は存在しない
            #一行のトータルの値しかｘ軸に移動しない
            self.numreturntotal=numreturn*(max(xlist))+self.numreturntotal+self.Adjustment_of_width_between_groups
            
        else:
            # 改行があるということは指定の数の並びであるという事だからｘ軸の長さは「指定の数×寸法」という計算式である
            self.numreturntotal=self.myint*(max(xlist))+self.numreturntotal+self.Adjustment_of_width_between_groups
    
    elif self.yaxisgroupret == True:
        yreturn=(len(sortlist)//self.myint)+1
        # 割り切れる行はあまりの列が無いので一つ改行を減らしておく
        if len(sortlist) % self.myint == 0:
            # print ("偶数です")
            yreturn-=1
        else:
            # print ("奇数です")
            pass

        #　グループ改行の幅の判定 Stacked_on_a_cube
        
        if self.Z_axis_for_line_breaks== True:
            if self.Stacked_on_a_cube != True:
                return_range = yreturn*max(zlist)
            else:
                return_range = self.z_axis_return_number*max(zlist)

            self.ynumreturntotal=return_range+self.ynumreturntotal+self.Adjustment_of_width_between_groups

        else:
            if self.Stacked_on_a_cube != True:

                return_range = yreturn*max(ylist)
            else:
                
                return_range = self.z_axis_return_number*max(ylist)

            self.ynumreturntotal=return_range+self.ynumreturntotal+self.Adjustment_of_width_between_groups

def Numerous_processes_in_the_group(self,spltname,sortlist):
    for name in spltname:
        sortlist.append(name['object'])

    # グループピングしたソートリストをグループ毎にランダムに配置する
    if self.mybool3 == True:
        random.seed(self.myint2)
        random.shuffle(sortlist)

    xlist,ylist,zlist = make_sortlists_dimension_list(self,sortlist)
    #　ここから各グループごとのオブジェクトを整列していく。
    numreturn = loc(
        self,
        seleobj=sortlist, 
        xlist=xlist,
        ylist=ylist,
        zlist=zlist,
        aligining=self.myint,
        numreturntotal=self.numreturntotal,
        ynumreturntotal=self.ynumreturntotal,
                      )
   
    return_gropu(self,numreturn,xlist,ylist,zlist,sortlist)

    sortlist.clear()

def setting(self):
    self.objlist=[]
    self.seleobj = bpy.context.selected_objects
    # xlist,ylist,zlist = dimensionlist(self,seleobj)

    for i in self.seleobj:
        self.objlist.append({"object":i,"spltname":i.name.split('.', 1)[0]})
    self.sortlist =[]

    # 下記2つはグループの改行移動量
    self.numreturntotal=0
    self.ynumreturntotal=0

# オペレターのセルフと自身のセルフは当然違う。クラスを分けて、クラス内でメソッドを定義することにより、セルフを分けることができる
class GropuAlign:    
#　グループの位置の処理関係
    def gropu_align(self,op_self):
        setting(op_self)

        for object, spltname in gropuping(op_self.objlist):
        
            Numerous_processes_in_the_group(op_self,spltname,op_self.sortlist)