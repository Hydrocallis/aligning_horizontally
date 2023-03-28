def dimensionlist(self,seleobj):
    xlist =[]
    ylist =[]
    zlist =[]

    for i in seleobj:
        xlist.append(i.dimensions[0]+self.myfloatvector[0])
        ylist.append(i.dimensions[1]+self.myfloatvector[1])
        zlist.append(i.dimensions[2]+self.myfloatvector[2])


    return xlist,ylist,zlist
