

__author__="andrealottarini"
__date__ ="$5-feb-2012 14.42.01$"

import copy

from point import *

class Shape(object):

    def iaddOffset(self,offset):
        for index,item in enumerate(self.points):            
            self.points[index] = self.points[index] + offset

    def addOffset(self,offset):
        out = copy.deepcopy(self)
        out.iaddOffset(offset)
        out.computeOrdine()
        return out

    #FIX: a positive (or negative) shape does not necessarily have ordine which is two times
    # the original one; however this is enforced in order for code generation to work
    def addOffsetTricky(self,offset):
        out = copy.deepcopy(self)
        out.iaddOffset(offset)
        out.ordine += abs(offset)
        return out

    def getNegativeShape(self):
        return self.addOffsetTricky( -self.ordine )

    def getPositiveShape(self):
        return self.addOffsetTricky( self.ordine )

    def computeOrdine(self):
        #shape order is computed from shape points
        self.ordine = 0
        for p in self.points:
            if p.getAbsMax() > self.ordine:
                self.ordine = p.getAbsMax()

    # Inizializzatore della classe
    def __init__(self, data):
        if type(data).__name__=='list':
            self.points = data
        elif type(data).__name__=='str':
            shape_coordinates = data.split('\t')

            #split different points
            for index,item in enumerate(shape_coordinates):
                shape_coordinates[index] = item.split(',')

            #split and converts coordinates of every point
            for index,item in enumerate(shape_coordinates):
                for index_1,item_1 in enumerate(shape_coordinates[index]):
                    item_1 = int(item_1)
                    shape_coordinates[index][index_1] = item_1

            # creates points
            for index,item in enumerate(shape_coordinates):
                shape_coordinates[index] = Point(item)

            self.points = shape_coordinates

        # initialize dim attribute which corresponds to the number of coordinates in a point
        self.dim = len(self[0])

        self.computeOrdine()


    #toString
    def __str__(self):
        return "Shape object in " +str(self.dim)+" spatial dimensions\nordine: "+str(self.ordine)+"\npoints:\n"+str(self.points)

    def __len__(self):
        return len(self.points)

    def __getitem__(self,index):
        return self.points[index]

    def __setitem__(self,index,value):
        self.points[index] = value


if __name__ == "__main__":
    import sys
    a = Point([1,2])
    b = Point([2,3])
    print "a", a
    print "b", b
    c = a + b
    print "a", a
    print "b", b
    print "c=a+b", c
    d = a + 1
    print "a", a
    print "d = a+1", d
