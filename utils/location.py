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
    #　Y軸のカウント変数
    

def loc(self, seleobj, xlist=[], ylist=[], zlist=[], aligining=2, numreturntotal=0, ynumreturntotal=0): 
    
    setting(self, seleobj, xlist ,ylist, zlist, aligining, numreturntotal, ynumreturntotal)
    ynumreturn=0

    for count,i in enumerate(seleobj):

 
        # 奥行きの位置
        if self.mybool == True:
            i.location[self.depth] =self.myfloatvector[self.depth]
        else:
            i.location[self.depth] =i.location[self.depth]+self.myfloatvector[self.depth]


        # グループの初回のXの位置　以降は位置がプラスされていく
        if count == 0:
            i.location[0] =numreturntotal+self.myfloatvector2[0]
            pass
        else:
             # グループの初回以降のXの位置
            self.xlocdeme = self.xlocdeme+max(xlist)
            if count !=0:
                i.location[0] = self.xlocdeme+numreturntotal
            elif count+1 == self.selelen:
                pass


        # グループ内での改行(Y軸)の条件式
        for j in range(self.kirisute):
            #指定した並び以上になったらY軸へ改行する分岐
            if count >=aligining*j:
    
                i.location[self.subreturn] = (self.subreturnmax)*j + self.returnlocdeme
                ynumreturn += 1
            

        # 改行後のXの位置の演算
        if len(seleobj) != 1:
            for j in range(self.kirisute): 
                if count+1 == aligining*j:
                    self.xlocdeme = self.myfloatvector2[0]-max(xlist)

        
    return ynumreturn
              
