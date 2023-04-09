from mathutils import Vector
# from .debug import line_num
# 導入したい機能：　指定の数に達したらｙreturnのYのロケーションをリセットし、
# 代わりにｚ軸を一段上げる　立体積み重ね機能
# 処理が面倒なので、縦軸を揃えてからこの処理を十個するプロセスで

def setting(self, seleobj, xlist=[], ylist=[], zlist=[], aligining=2, numreturntotal=0, ynumreturntotal=0):
    # ※numretuqntotalの値はグループの改行ごとに加算されていく
    self.yaxis=1
    self.depth = 2 #　縦軸用の
    self.subreturn=self.yaxis
    self.subreturnmax=max(ylist)
    self.depthmax=max(zlist)
    # グループ内の改行が終わったら次のグループへ改行を促すためのカウント
    self.ynumreturn = 0 

    # ここでZ軸かY軸が縦軸か判定して入れ替える
    if self.Z_axis_for_line_breaks== True:
        self.subreturn=self.depth
        self.subreturnmaxq=self.depthmax
        self.depth=self.yaxis
        # ※入れ替える
        self.yaxis = 2

    
    self.selelen = len(seleobj)
    # 何回Y軸に改行するか
    self.kirisute = (self.selelen//aligining)+1
    
    self.returnlocdeme =ynumreturntotal+self.myfloatvector2[self.subreturn]
    self.xlocdeme =self.myfloatvector2[0]

def move_y_or_z_return_counted_return(self,count,aligining,kirisute_count_y_or_z,obj):
    #ｊ毎に改行するスクリプト　このスクリプトの後にJかIの条件を合わせてYの軸位置をリセットしてやれば改行がリセットされる。
    if count >= aligining * kirisute_count_y_or_z:
        if self.y_axis_direction_to_reverse == False:
            obj.location[self.subreturn] = (self.subreturnmax) * kirisute_count_y_or_z + self.returnlocdeme
        else:
            obj.location[self.subreturn] = -(self.subreturnmax) * kirisute_count_y_or_z - self.returnlocdeme
        self.ynumreturn += 1

def move_y_or_z_return(self, count, aligining, obj ):
    # グループ内での改行(Y軸OR Z軸)の条件式
    for kirisute_count_y_or_z in range(self.kirisute):
        
        #指定した並び以上になったらY軸へ改行する分岐
        move_y_or_z_return_counted_return(self,count,aligining,kirisute_count_y_or_z,obj)

def move_x_move(self,count,obj,numreturntotal,xlist):
    # グループの初回のXの位置　以降は位置がプラスされていく
    if count == 0:
        if self.x_axis_direction_to_reverse == False:
            obj.location[0] = numreturntotal + self.myfloatvector2[0]
        else:
            obj.location[0] = -numreturntotal - self.myfloatvector2[0]
        pass
    
    else:
            # グループの初回以降のXの位置
        self.xlocdeme = self.xlocdeme+max(xlist)
        if count !=0:
            if self.x_axis_direction_to_reverse == False:
                obj.location[0] = self.xlocdeme + numreturntotal
            else:
                obj.location[0] = -self.xlocdeme - numreturntotal

        elif count+1 == self.selelen:
            pass
    
def move(self,obj,count,numreturntotal,xlist,aligining,seleobj):
   
    # 奥行きの位置 Y軸モードだとZ軸の位置
    if self.to_origin == True:
        obj.location[self.depth] =self.myfloatvector[self.depth]+ self.filerst_obj_loc[self.depth]
    else:
        obj.location[self.depth] =obj.location[self.depth]+self.myfloatvector[self.depth]


    move_x_move(self,count,obj,numreturntotal,xlist)


    move_y_or_z_return(self, count, aligining, obj )
                    

    # 改行後のXの位置の演算
    if len(seleobj) != 1:
        for kirisute_count in range(self.kirisute): 
            if count + 1 == aligining * kirisute_count:
                self.xlocdeme = self.myfloatvector2[0]-max(xlist)

def loc_Move_the_reference_to_the_first_selected_object(self,obj):
    if self.depth ==2:
        obj.location= obj.location+Vector((self.filerst_obj_loc[0],self.filerst_obj_loc[1],0))
    
    elif self.depth ==1:
        obj.location= obj.location+Vector((self.filerst_obj_loc[0],0,self.filerst_obj_loc[2]))

def loc_move_rippoutai(self,seleobj,aligining):
    # 仮に立方体改行を３からとする
    x=self.z_axis_return_number
    locationmovez=0
    locationmovey=0
    
    for index,obj in enumerate(seleobj,start=1):
  
        for count in range(1,self.kirisute):
            # print('###',count,obj)
            if index >(aligining*x*count):
                locationmovez+=self.depthmax
                locationmovey+=self.subreturnmax*x
            #一段上げる
            obj.location[self.depth] +=locationmovez
            #　一旦Y位置を初期化する
            if  self.y_axis_direction_to_reverse == False:
                obj.location[self.yaxis] -=locationmovey
            else:
                obj.location[self.yaxis] +=locationmovey
                
            # 初期化
            if index >aligining*x*count:
                locationmovez+=-self.depthmax
                locationmovey-=self.subreturnmax*x
        
def loc(self, seleobj, xlist=[], ylist=[], zlist=[], aligining=2, numreturntotal=0, ynumreturntotal=0): 
    
    setting(self, seleobj, xlist ,ylist, zlist, aligining, numreturntotal, ynumreturntotal)
    # print('###', aligining,0, self.kirisute)
    #　Y軸のカウント変数
    for count,obj in enumerate(seleobj):
        move(self,obj,count,numreturntotal,xlist,aligining,seleobj)
        # print('###depth',self.depth)

        # 最初に選択したオブジェクトに基準を移動する。
        loc_Move_the_reference_to_the_first_selected_object(self,obj)

    # print('###', aligining, count, self.kirisute)
    if self.Stacked_on_a_cube == True:
        loc_move_rippoutai(self,seleobj,aligining)
    return self.ynumreturn
              
