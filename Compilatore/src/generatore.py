# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="andrealottarini"
__date__ ="$15-feb-2012 11.22.26$"

import util

def returnSecId(section):
    out = ""
    for i in section.tag:
        out +=str(i)
    return out

class Generatore(object):

    def __init__(self,section):
        self.section = section

    def generaCodice(self,file):
        albero = self.section.root

        with open(file,'a') as f:
            self.generaNodo(albero,f)

    def generaInit(self,file):
        # in matlab I do not have negative index
        # indexes start from 1
        staticOffset = []
        for i in range(self.section.father.dim):
            staticOffset.append(self.section.father.ordine+1)

        with open(file,"a") as f:
            id = returnSecId(self.section)
            self.start = util.addList(staticOffset, self.section.realCoordinates)
            self.end = util.addList(self.start, self.section.realDim)
            print self.start,self.end

            #internal section
            f.write("s"+str(id)+"=a(")
            count = 0
            merged = zip(self.start,self.end)
            for i in merged:
                print i
                count +=1
                f.write(str(i[0])+":"+str(i[1]-1))
                if count < len(merged):
                    f.write(",")
            #f.seek(f.tell()-1)
            f.write(");\n")

            #external section
            self.ostart = util.addList(staticOffset, self.section.orealCoordinates)
            self.oend = util.addList(self.ostart, self.section.orealDim)
            print self.ostart,self.oend
            f.write("o"+str(id)+"=a(")
            count = 0
            merged = zip(self.ostart,self.oend)
            for i in merged:
                print i
                count +=1
                f.write(str(i[0])+":"+str(i[1]-1))
                if count < len(merged):
                    f.write(",")
            #f.seek(f.tell()-1)
            f.write(");\n")

    def generaClose(self,file):

        staticOffset = []
        for i in range(self.section.father.dim):
            staticOffset.append(1)

        with open(file,"a") as f:
            id = returnSecId(self.section)
            self.start = util.addList(staticOffset, self.section.realCoordinates)
            self.end = util.addList(self.start, self.section.realDim)
            print self.start,self.end
            f.write("b(")
            count = 0
            merged = zip(self.start,self.end)
            for i in merged:
                print i
                count +=1
                f.write(str(i[0])+":"+str(i[1]-1))
                if count < len(merged):
                    f.write(",")
            #f.seek(f.tell()-1)
            f.write(") = s" +str(id)+"_1 ;\n")

    def generaNodo(self,node,f):
        if node is not None:
            tab=""
            if node.start is not -1:
                
                for i in range(node.level):
                    tab +="\t"
                # il +1 e per MATLAB
                f.write(tab+"for i"+str(node.level)+" = "+str(node.start+1)+" : " +str(node.end+1)+"\n")

                # qui il pezzo mui brutto
                if len(node.offsets) > 0:
                    #_1 e per avere output separato da input
                    f.write(tab+"\ts"+returnSecId(self.section)+"_1(")
                    #se ho degli offset allora sono al nodo foglia ecco perche c'e il +1

                    for j in range(node.level):
                        f.write("i"+str(j)+",")
                    f.write("i"+str(j+1)+")")
                    #f.seek(f.tell()-1)                    
                    f.write(" = funzione( " )
                    count = 0
                    for offset in node.offsets:
                        if offset.isOuter is True:
                            f.write("o")
                        else:
                            f.write("s")
                        f.write(returnSecId(offset.father))
                        f.write(offset.getStr())
                        count +=1
                        if count < len(node.offsets):
                            f.write(",")
                    #f.seek(f.tell()-1)
                    f.write(");\n")

            for c in node.childs:
                self.generaNodo(c, f)
            if node.start is not -1:
                f.write(tab+"end\n")



if __name__ == "__main__":
    print "Hello World"