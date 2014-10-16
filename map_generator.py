
from random import *
from math import *

from diamond_square import *
from map_handler import *

import pygame, sys
from pygame import *

#генератор карты работает следующим образом:
#    1) сначала генерируется карта высот методом diamomd-square
#    2) потом уничтожаются внутренние моря
#    3) потом высчитывается эрозия методом, безирующимся на методе тепловой эрозии
#    4) потом высчитываются реки.

def bwIt(a,world):  #black and white it. раскрашивание карты в ч/б цвет
    minH=0
    maxH=0
    for row in world:
        if min(row)<minH:minH=min(row)
    if minH<0:
        world=[[x+abs(minH) for x in row] for row in world]
    for row in world:
        if max(row)>maxH:maxH=max(row)
    r=maxH/float(255)
    world=[[int(x/r) for x in row] for row in world]
    for i in range(len(world)):
        for j in range(len(world[0])):
            a[i][j]=(world[i][j],world[i][j],world[i][j])

def colorizeIt(a,hMap):     #раскрашивание карты в различные цвета
    for i in range(len(hMap)):
        for j in range(len(hMap[0])):
            k=(hMap[i][j],hMap[i][j],hMap[i][j])
            if k[0]<=deepestWaterLine0:
                a[i][j]=(deepestWaterColor0)
            if k[0]<underwaterLine2 and k[0]>deepestWaterLine0:                        #впадины
                a[i][j]=(underwaterColor2)
            elif k[0]>=underwaterLine2 and k[0]<underwaterLine1:        #глубины
                a[i][j]=(underwaterColor1)
            if k[0]>=underwaterLine1 and k[0]<seaLine:        #шельф
                a[i][j]=(underwaterColor0)
            if k[0]==seaLine:     #береговая линия
                a[i][j]=(seaLineColor)
            if k[0]>seaLine and k[0]<landLine0:   #суша1
                a[i][j]=(landLineColor0)
            if k[0]>=landLine0 and k[0]<landLine1:   #суша1
                a[i][j]=(landLineColor1)
            if k[0]>=landLine1 and k[0]<landLine2:   #суша1
                a[i][j]=(landLineColor2)
            if k[0]>=mountainLineBottom and k[0]<mountainLine1:   #горы
                a[i][j]=(mountainColor)
            if k[0]>=mountainLine1 and k[0]<mountainLineTop:   #горы
                a[i][j]=(mountainColor1)
            if k[0]>=pikeLine:# and k[0]<=maxHeight:       #пики
                a[i][j]=(pikeColor)

            '''if k[0]==0:                             #ноль
                a[i][j]=(255,0,0)'''
def colorizeRiver(a,rivers):    #раскрашивание рек
    for i in range(hMW):
        for j in range(hMH):
            if rivers[i][j]>0:
                a[i][j]=(0,100,255)

def colorizeContour(a,contour):
    for i in range(hMW):
        for j in range(hMH):
            if contour[i][j]==0:
                a[i][j]=(0,100,255)
            elif contour[i][j]==1:
                a[i][j]=(0,255,100)
            else:
                a[i][j]=(255,0,0)

                



#================== MAIN PART =======================

            #генерируем карту высот

#размер рабочего квадрата (степень двойки!)

mainMultiplier=6    
mainSquareSize=mSS=2**mainMultiplier+1

#из скольких квадратов будет состоять карта
mainSquareNumberX=mSNX=3
mainSquareNumberY=mSNY=3

seaLvl=0.5     #это проценты от нуля до максимальной высоты!
pikeLvl=1.25
maxHeight=mSS#maxN  #назначем максимум
minHeight=-mSS#minN

#точкой нуля по оси Х считается уровень моря, следовательно все отсчеты идут вниз или вверх от этой линии
#высота уровня моря
seaLine=maxHeight*seaLvl

#-----------
#сначала мы генерим опорную сетку высот минимального размера
#(края квадратов должны перекрывать друг друга)
    
heightMap=[]
heightMapWidth=hMW=mSS*mSNX-mSNX+1#mSS+(mSS-1)*(mSNX-1)
heightMapHeight=hMH=mSS*mSNY-mSNY+1#mSS+(mSS-1)*(mSNX-1)

for i in range(hMW):
    heightMap.append([0]*hMH)
print 'matrix size=',hMW,hMH

#потом заполняем ключевые точки высотами

step=mSS-1
for i in range(0,hMW,step):
    #if  i==hMW:i-=1
    for j in range(0,hMH,step):
     #   if  j==hMH:j-=1
        #print i,j,'hMh-1',hMH-1
        if i==0 or j==0 or i==hMW-1 or j==hMH-1:
            heightMap[i][j]=1
        else:
            heightMap[i][j]=randint(1,mSS/4*3)+0.001
        #print 'i,j=',i,j,'H=',heightMap[i][j]


#print 'H=',heightMap[0][0],heightMap[-1][-1]

#теперь считаем квадраты и даймонды проходя по основным квадратам
#print hMW, hMH

for i in range(0,hMW-1,step):
    for j in range(0,hMH-1,step):
        #print i,j, step
        heightGenSquare(heightMap,i,j,step)
        print 'square done'


                #убираем озера
            
www=lakeSearching(heightMap, seaLine)
#print www

                #erosion

talusAngle=mSS/4
portion=1#talusAngle/16
erosionStep=2
        
for i in range(0,hMW-1,erosionStep):
    for j in range(0,hMH-1,erosionStep):
        #erosion(heightMap,i,j,talusAngle,portion)
        pass
print 'erozion done'

#contour=lakeSearching()

                #rivers

'''minSpringLvl=[mSS/6*4,mSS/6*2]
rivers=[]
riversNumber=mSNX*mSNY*1.5
riverSquare=[]
riverSquare=[[0,-1],[1,0],[0,1],[-1,0]]

for i in range(hMW) :
    rivers.append([0]*hMH)

for i in minSpringLvl:
    a=0
    while a<riversNumber:
        startX=randint(1,hMW-1)
        startY=randint(1,hMH-1)
        if heightMap[startX][startY]>=i:'''
            #river2(rivers,startX,startY,riverSquare,mSS*0.5)
            #a+=1
            #for i in range(len(r)):
             #   rivers[r[i][0]][r[i][1]]=1
            #print 'river added'
            
            
print 'rivers done'


#===================ВЫВОД НА ЭКРАН===========================

#найдем максимальный элемент матрицы
maxN=0
minN=0
for row in heightMap:
    maxR=max(row)
    minR=min(row)
    if maxR>maxN:maxN=maxR
    if minR<minN:minN=minR


pygame.init()
DISPLAYSURF = pygame.display.set_mode((hMW, hMH))
pygame.display.set_caption('World!')




seaLineColor=(225,246,97)   #желтенький такой, как песок на берегу

#подводные впадины
deepestWaterLine0=minHeight+(abs(minHeight)*0.4)
deepestWaterColor0=(0,0,70)

#подводные глубины (коэффициент может меняться от 0 до 1) (отсчет идет вниз!)
underwaterLine0=maxHeight*(seaLvl*1.0) #шельф
underwaterColor0=(0,64,255)
underwaterLine1=maxHeight*(seaLvl*0.5)
underwaterColor1=(0,40,198)
underwaterLine2=maxHeight*(seaLvl*0.25)
underwaterColor2=(0,0,150)


#суша (коэффициент может меняться от 0 до нижней границы гор)
landLvl=pikeLvl-seaLvl  #промежуток между линией моря и линией вечных снегов в горах

landLine0=maxHeight*(seaLvl+landLvl*0.25)
landLineColor0=(110,195,0)
landLine1=maxHeight*(seaLvl+landLvl*0.65)
landLineColor1=(77,136,0)
#landLineColor1=(145,167,84)

landLine2=maxHeight*(seaLvl+landLvl*0.7)    #hills?
#landLineColor2=(105,106,40)
landLineColor2=(70,116,0)

#горы. фактически это часть суши. указана верхняя и нижняя граница. коэффициент может меняться от максимального коэффициента уровня суши до 1
mountainLineBottom=maxHeight*(seaLvl+landLvl*0.7)   #bottom
mountainColor=(130,85,45)
mountainLine1=maxHeight*(seaLvl+landLvl*0.8)  
mountainColor1=(106,70,30)
mountainLineTop=maxHeight*(seaLvl+landLvl*1.0)      #top

#пики
pikeLine=maxHeight*pikeLvl
pikeColor=(250,250,250)


a=PixelArray(DISPLAYSURF)
#colorizeIt(a,heightMap)
#colorizeRiver(a,rivers)
#bwIt(a,heightMap)

colorizeContour(a,www)
del a

        

while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
