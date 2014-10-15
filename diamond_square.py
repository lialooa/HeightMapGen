#diamond-square

from random import *
from math import *


def centerIt(a,step,b):
    c=(a[0]+a[1]+a[2]+a[3])/4
    cP=c+1*randint(-step/b,step/b)+0.001
    return cP

def squareIt(hMap,centerX,centerY,step,rC):
    #print 'in square'
    #if rC[0]>2:rC[0]=0
    #print 'rC=',rC[0],'',step
    stepR=step
    step=step*rC[0]
    a=[0,0,0,0]
    coordS=[[centerX-step,centerY-step],
           [centerX+step,centerY-step],
           [centerX+step,centerY+step],
           [centerX-step,centerY+step]]
    
    for i in range(4):
        try:
            a[i]=hMap[coordS[i][0]][coordS[i][1]]
        except IndexError:
            a[i]=1
        if coordS[i][0]<=0 or coordS[i][1]<=0 or coordS[i][0]>=len(hMap)-1 or coordS[i][1]>=len(hMap[0])-1:
            a[i]=1
        #print 'SQUA a[',i,']=',a[i],'coordS=',coordS[i][0],'x',coordS[i][1]
        if a[i]==0:
            while hMap[coordS[i][0]][coordS[i][1]]==0:
                rC[0]+=1
                
                #print 'step=',step,'rC[1]=',rC[1]
                a[i]=diamondIt(hMap,coordS[i][0],coordS[i][1],stepR,rC)
                hMap[coordS[i][0]][coordS[i][1]]=a[i]

                #print 'squa written coordS',coordS[i][0],coordS[i][1],'step=',step,'rC[0]=',rC[0],'a[',i,']',a[i]
                rC[0]=1

    return centerIt(a,step*2,rC[0])

def diamondIt(hMap,centerX,centerY,step,rC):
    #print 'in dia'
    #if rC[1]>2:rC[1]=0
    #print 'rC=',rC[1]
    stepR=step
    step=step*rC[1]
    a=[0,0,0,0]
    coordD=[[centerX-step,centerY],
           [centerX,centerY-step],
           [centerX+step,centerY],
           [centerX,centerY+step]]
    #print coordD
    for i in range(4):
        try:
            a[i]=hMap[coordD[i][0]][coordD[i][1]]
        except IndexError:
            a[i]=1
        if coordD[i][0]<=0 or coordD[i][1]<=0 or coordD[i][0]>=len(hMap)-1 or coordD[i][1]>=len(hMap[0])-1:
            a[i]=1
        #print 'DIA a[',i,']=',a[i],'coordD=',coordD[i][0],'x',coordD[i][1]
        if a[i]==0:
            while hMap[coordD[i][0]][coordD[i][1]]==0:
                rC[1]+=1
              
                #print 'step=',step,'rC[1]=',rC[1]
                a[i]=squareIt(hMap,coordD[i][0],coordD[i][1],stepR,rC)
                hMap[coordD[i][0]][coordD[i][1]]=a[i]
                #print 'dia written coord',coordD[i][0],coordD[i][1],'step=',step,'rC[1]=',rC[1],'a[',i,']',a[i]
                rC[1]=1

    return centerIt(a,step*2,rC[1])


def heightGenSquare(hMap,startX,startY,mainStep):
    k=1
    a=[0,0,0,0]
    #print '>>>>>>>>next main step',mainStep
    while k<mainStep:
        step=mainStep/k
        #print 'startX, step=',startX,step
        for i in range(startX,startX+mainStep,step):
            startPointX=i
            endPointX=i+step

            #square
            for j in range(startY,startY+mainStep,step):
                #print '>>>>>> start first cycle i,j, step=',i,j,step

                    #print 'startX, endX=',startX,startX+mainStep,'j=',j
                    #print 'startY, endY=',startY,startY+mainStep,'j=',j
                startPointY=j
                endPointY=j+step
                recursiveCounter=rC=[1,1]
                if hMap[startPointX+step/2][startPointY+step/2]==0:
                    #print 'j1=',j,'rC=',rC
                    
                    hMap[startPointX+step/2][startPointY+step/2]=squareIt(hMap,startPointX+step/2,startPointY+step/2,step/2,rC)
                    #print 'written in BC squa',startPointX+step/2,'x',startPointY+step/2,'--',hMap[startPointX+step/2][startPointY+step/2]
                    

        for i in range(startX,startX+mainStep,step):
            startPointX=i
            endPointX=i+step
            #diamond
            for j in range(startY,startY+mainStep,step):
                #print '>>>>>> start second cycle i,j, step=',i,j,step
                startPointY=j
                endPointY=j+step
                diamondPoints=[[startPointX+step/2,startPointY],
                               [endPointX,startPointY+step/2],
                               [startPointX+step/2,endPointY],
                               [startPointX,startPointY+step/2]]
                for dP in range(4):
                    rC=[1,1]
                    if hMap[diamondPoints[dP][0]][diamondPoints[dP][1]]==0:
                        #print 'j2=',j

                        hMap[diamondPoints[dP][0]][diamondPoints[dP][1]]=diamondIt(hMap,diamondPoints[dP][0],diamondPoints[dP][1],step/2,rC)
                        #print 'written in BC dia',diamondPoints[dP][0],'x',diamondPoints[dP][1],'--',hMap[diamondPoints[dP][0]][diamondPoints[dP][1]]
                    
        k=k*2
