from mathutils import Vector

def setting(self, seleobj, xlist=[], ylist=[], zlist=[], aligining=2, numreturntotal=0, ynumreturntotal=0):

    # ※numretuntotalの値はグループの改行ごとに加算されていく
    yaxis=1
    self.subreturn=yaxis
    self.subreturnmax=max(ylist)
    self.depth = 2
    depthmax=max(zlist)

    if self.Z_axis_for_line_breaks== True:
        self.subreturn=self.depth
        self.subreturnmax=depthmax
        self.depth=yaxis

    
    self.selelen = len(seleobj)
    # 何回Y軸に改行するか
    self.kirisute = (self.selelen//aligining)+1
    
    self.returnlocdeme =ynumreturntotal+self.myfloatvector2[self.subreturn]
    self.xlocdeme =self.myfloatvector2[0]

def move_y_or_z_return(self, count, aligining, i ,ynumreturn):
    # グループ内での改行(Y軸OR Z軸)の条件式
    for j in range(self.kirisute):
        #指定した並び以上になったらY軸へ改行する分岐
        if count >=aligining*j:
            if self.y_axis_direction_to_reverse == False:
                i.location[self.subreturn] = (self.subreturnmax)*j + self.returnlocdeme
            else:
                i.location[self.subreturn] = -(self.subreturnmax)*j - self.returnlocdeme

            ynumreturn += 1

    return ynumreturn

def move_x_move(self,count,i,numreturntotal,xlist):
    # グループの初回のXの位置　以降は位置がプラスされていく
    if count == 0:
        if self.x_axis_direction_to_reverse == False:
            i.location[0] = numreturntotal + self.myfloatvector2[0]
        else:
            i.location[0] = -numreturntotal - self.myfloatvector2[0]

        pass
    
    else:
            # グループの初回以降のXの位置
        self.xlocdeme = self.xlocdeme+max(xlist)
        if count !=0:
            if self.x_axis_direction_to_reverse == False:
                i.location[0] = self.xlocdeme + numreturntotal
            else:
                i.location[0] = -self.xlocdeme - numreturntotal

        elif count+1 == self.selelen:
            pass

def move(self,i,count,numreturntotal,xlist,aligining,seleobj,ynumreturn):

    
    # 奥行きの位置
    if self.to_origin == True:
        i.location[self.depth] =self.myfloatvector[self.depth]+ self.filerst_obj_loc[self.depth]
    else:
        i.location[self.depth] =i.location[self.depth]+self.myfloatvector[self.depth]


    move_x_move(self,count,i,numreturntotal,xlist)

    ynumreturn = move_y_or_z_return(self, count, aligining, i ,ynumreturn)
                    

    # 改行後のXの位置の演算
    if len(seleobj) != 1:
        for j in range(self.kirisute): 
            if count+1 == aligining*j:
                self.xlocdeme = self.myfloatvector2[0]-max(xlist)

    return ynumreturn

def loc(self, seleobj, xlist=[], ylist=[], zlist=[], aligining=2, numreturntotal=0, ynumreturntotal=0): 
    
    setting(self, seleobj, xlist ,ylist, zlist, aligining, numreturntotal, ynumreturntotal)

    #　Y軸のカウント変数
    ynumreturn = 0
    # filerst_obj_loc =seleobj[0].location 
    for count,i in enumerate(seleobj):
        ynumreturn = move(self,i,count,numreturntotal,xlist,aligining,seleobj,ynumreturn)
        # if count ==0:
        # print('###self.filerst_obj_loc',self.filerst_obj_loc)
        # print('###depth',self.depth)
        if self.depth ==2:
            i.location= i.location+Vector((self.filerst_obj_loc[0],self.filerst_obj_loc[1],0))
        elif self.depth ==1:
            i.location= i.location+Vector((self.filerst_obj_loc[0],0,self.filerst_obj_loc[2]))
        
    return ynumreturn
              
