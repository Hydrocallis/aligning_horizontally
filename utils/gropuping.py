
from itertools import groupby

def gropuping(objlist):
    objlist.sort(key=lambda x: x['spltname'])
    outputlist = groupby(objlist, key=lambda x: x['spltname'])
    return outputlist