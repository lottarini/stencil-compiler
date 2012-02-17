import util
import generatore
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="andrealottarini"
__date__ ="$5-feb-2012 14.40.07$"

import numpy as np

from section import *

class Partition(object):

    #tricky magari ripensaci con un iteratore
    def recursiveInit(self,element,level,coordinate):
        #print "ELEMENT:\n"+ str(element) + "\nLEVEL:\n" +str(level) + "\nCOORDINATE\n" +str(coordinate)
        if element is not None:
            for index, item in enumerate(element):
                #print "sono nella recursiveInit" ,index,item,element
                coordinate.append(index)
                isLast = self.recursiveInit(item,level+1,coordinate)
                if isLast:
                    #print "sto per modificare", str(element[index])
                    #print self
                    element[index] = Section(copy.deepcopy(coordinate),self)
                    #print "stampo cosa ho fatto: " +str(index)+" " + str(coordinate)
                    #print self
                coordinate.pop()
            return False
        else:
            return True

    def __init__(self,shape,finalSize):

        # if finalSize is less than size then an error is raised,
        # in order to debug the tree mechanism WITHOUT ESPANSION
        # finalSize should have the same value of self.size

        self.shape = shape

        self.ordine = shape.ordine

        self.dim = shape.dim

        #computes size
        self.size = 5*self.ordine + 1

        if finalSize < self.size:
            raise ValueError("Final Dimension smaller than partition self.father.size")
        elif finalSize == self.size:
            print "TREE WILL NOT BE EXPANDED"
        self.finalSize = finalSize

        #creates array of sections
        dimensioni=[]
        for i in range(self.dim):
            dimensioni.append(3)
        #print dimensioni
        #the dim-dimensional matrix of sections is created empty
        self.sezioni = np.empty(dimensioni,dtype=Section)

        #every section in the matrix is initialized
        self.recursiveInit(self.sezioni,0,[])


    def __getitem__(self,index):
        return self.sezioni.flat[index]

    def __str__(self):
        return "sono una partizione\n" +str(self.sezioni)

    def getCandidates(self, p):
        """ Retrieve all SectionPoints which are contained in partition

            self -- partition which presumably contain multiple instances of point p
            p    -- point that has to be searched

            out  -- a list of SectionPoints which has same global coordinates as point p

        """

        out = []
        #qui potrei fare un iteratore
        for section in self.sezioni.flat:
            for point in section.points.flat:
                if p.isSimilar(point):
                    out.append(point)
            for point in section.opoints.flat:
                if p.isSimilar(point):
                    out.append(point)
        return out

    #DEPRECATED ABBESTIA
    def createMatlabScript(self,file1='scriptsections.m'):
        staticOffset = []
        for i in range(self.dim):
            staticOffset.append(self.ordine+1)

        with open(file1,"w") as f:
            for section in self.sezioni.flat:
                id = generatore.returnSecId(section)
                start = util.addList(staticOffset, section.startingCoordinates)
                end = util.addList(start, section.dim)
                print start,end
                f.write("s"+str(id)+"=a(")
                for i in zip(start,end):
                    print i
                    f.write(str(i[0])+":"+str(i[1]-1)+",")
                f.seek(f.tell()-1)
                f.write(");\n")


if __name__ == "__main__":
    print "No debug for partition"