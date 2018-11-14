import sys
sys.path.append('../')
sys.path.append('../../')
from CHECLabPy.core.io import DL1Reader
import numpy as np
from scipy.stats import norm

def testreadin():
    path='C:/Users/Jamie Williams/Desktop/New folder/meangm200PEdiffNSB.npy'
    meangm200PEdiffNSB=np.load(path)
    data=meangm200PEdiffNSB[:,:,0] #read in first data set
    size = len(data)
    (mu,sigma)=norm.fit(data)
    okpixel2 = np.ones((size, size))      
    for i in range (0,size):
        for j in range (0,size):
            if data[i,j]<mu-sigma:
                data[i,j]=0         # create dead pixels    
                okpixel2[i,j]=0
    return {'data':data,'okpixel2':okpixel2,'size':size}
def datareadin(ieve):
    #path=(b'C:\Users\Jamie Williams\Desktop\New folder\NSB200PE\data_Run030_dl1.h5')
    path=(b'C:\Users\Jamie Williams\Desktop\New folder\Old data sets\Run17473_dl1.h5')            
    ievcount=10
    reader = DL1Reader(path)
    reader.load_entire_table()
    charge = reader.select_column('charge').values
    iev = reader.select_column('iev').values
    charge = charge [iev == ievcount]
    #okpixel= okpixel[iev == ievcount]
    m=reader.mapping
    row = m['row'].values
    col = m['col'].values
    n_rows = m.metadata['n_rows']
    n_cols = m.metadata['n_columns']
    size=max(row+1)
    okpixel=np.ones(len(charge),)
    lencharge=len(charge)
    okpixel[ieve]=0
    data = np.ma.zeros((n_rows, n_cols))  
    data[row, col] = np.multiply(charge,okpixel)
    okpixel2=np.ma.zeros((n_rows, n_cols))
    okpixel2[row, col]=okpixel
    if size==480:
        (mu,sigma)=norm.fit(data)  #used to identify dead pixels
        for i1 in range (0,48):
            for j1 in range (0,48):
                if (data[i1,j1]<mu-sigma):
                #if (data[row,col]<mu-10*sigma):   #do it without the loop?
                    okpixel2[i1,j1]=0
    return {'data':data,'okpixel2':okpixel2,'size':size, 'lencharge':lencharge}
###################################################################################
def sumoffour(meangmt2,i,j,size):
    print('Sum of Four')
    count=0
    a=0
    b=0
    c=0
    d=0
    e=0
    ok=0
    if j-1>-1:
        if meangmt2[i,j-1]!=0:
            a=meangmt2[i,j-1]
            count=count+1
    if j+1<size:
        if meangmt2[i,j+1]!=0: 
            b=meangmt2[i,j+1]
            count=count+1
    if i+1<size:
        if meangmt2[i+1,j]!=0:
            c=meangmt2[i+1,j]
            count=count+1
    if i-1>-1:
        if meangmt2[i-1,j]!=0: 
            d=meangmt2[i-1,j]
            count=count+1
    if count>2:
    #    if a>0 and b>0 and c>0 and d>0:
        e=(a+b+c+d)/count
        ok=1
    return {'e':e,'ok':ok}
def sumofeight(meangmt2,i,j,size):
    count=0
    aok=0
    bok=0
    cok=0
    dok=0
    eok=0
    fok=0
    gok=0
    hok=0
    j1=0
    j2=0
    i1=0
    i2=0
    ok=0
    e=0
    if j-1>-1:
        j1=1
    if j+1<size:
        j2=1
    if i-1>-1:
        i1=1
    if i+1<size:
        i2=1
    if i1==1:           #where i-1 allowed        
        if meangmt2[i-1,j]!=0:
            c=meangmt2[i-1,j]
            count=count+1
            cok=1
        if j1==1:
            if meangmt2[i-1,j-1]!=0:
                h=meangmt2[i-1,j-1]
                count=count+1
                hok=1 
        if j2==1:
            if meangmt2[i-1,j+1]!=0:
                g=meangmt2[i-1,j+1]
                count=count+1
                gok=1 
    if i2==1:
        if meangmt2[i+1,j]!=0:
            b=meangmt2[i+1,j]
            count=count+1
            bok=1
        if j1==1:
            if meangmt2[i+1,j-1]!=0:
                f=meangmt2[i+1,j-1]
                count=count+1
                fok=1                  
        if j2==1:
            if meangmt2[i+1,j+1]!=0:
                e1=meangmt2[i+1,j+1]
                count=count+1
                eok=1
    if j1==1:
        if meangmt2[i,j-1]!=0:
            a=meangmt2[i,j-1]
            count=count+1
            aok=1                
    if j2==1:        
        if meangmt2[i,j+1]!=0:           
            d=meangmt2[i,j+1]
            count=count+1
            dok=1 
    if count>4:
        e=((aok*a)+(bok*b)+(cok*c)+(dok*d)+(eok*e1)+(fok*f)+(gok*g)+(hok*h))/count
        ok=1
    return {'e':e,'ok':ok} 
def sumoffive(meangmt2,i,j):  
    count=0
    ok=0
    abcdeok=np.zeros((5,2)) #a row 0, b row 1 etc. Value in col 0, multiplier in col 1
    if meangmt2[i,j-1]>0:
        count=count+1
        abcdeok[0,0]=meangmt2[i,j-1]
        abcdeok[0,1]=1
    if meangmt2[i+1,j-1]>0:
        count=count+1
        abcdeok[1,0]=meangmt2[i+1,j-1]
        abcdeok[1,1]=1              
    if meangmt2[i+1,j]>0:
        count=count+1
        abcdeok[2,0]=meangmt2[i+1,j]
        abcdeok[2,1]=1                   
    if meangmt2[i+1,j+1]>0:
        count=count+1
        abcdeok[3,0]=meangmt2[i+1,j+1]
        abcdeok[3,1]=1
    if meangmt2[i,j+1]>0:
        count=count+1
        abcdeok[4,0]=meangmt2[i,j+1]
        abcdeok[4,1]=1
    if count>3:
        e=((abcdeok[0,0]*abcdeok[0,1])+(abcdeok[1,0]*abcdeok[1,1])+(abcdeok[2,0]*abcdeok[2,1])+(abcdeok[3,0]*abcdeok[3,1])+(abcdeok[4,0]*abcdeok[4,1]))/count      
    return {'e':e,'ok':ok} 
def deadpixelalg1(size,okpixel2,meangmt2):
    if size==8:      
        ##Taking in an 8 x 8 array. Different techniques to average pixels, primarily from nearest neighbours.
        print('Average of nearest neighbours (4 in the centre, 3 on the edge, 2 on the corner). Only works if the summing pixels are not dead too')
        for i in range (0,8):
            for j in range (0,8):
                if okpixel2[i,j]==0:    #could replace with a find locations of dead pixels
                    if i>0 and i<7 and j>0 and j<7:     #CENTRE OF MODULE
#                        a=meangmt2[i,j-1]
#                        b=meangmt2[i,j+1]
#                        c=meangmt2[i+1,j]
#                        d=meangmt2[i-1,j]
#                        if a>0 and b>0 and c>0 and d>0:
#                            meangmt2[i,j]=(a+b+c+d)/4 
                        sum4=sumoffour(meangmt2,i,j,size)
                        ok=sum4['ok']
                        if ok==1:
                            meangmt2[i,j]=sum4['e']
                    elif i==0:
                        if j>0 and j<7:                 #TOP OF MODULE
                            a=meangmt2[i,j-1]
                            b=meangmt2[i,j+1]
                            c=meangmt2[i+1,j]
                            if a>0 and b>0 and c>0:
                                meangmt2[i,j]=(a+b+c)/3                            
                        if j==0:                        #TOP LEFT CORNER
                            a=meangmt2[1,0]
                            b=meangmt2[0,1]
                            if a>0 and b>0 and c>0:
                                meangmt2[0,0]=(a+b)/2
                        if j==7:                        #TOP RIGHT CORNER
                            a=meangmt2[0,6]
                            b=meangmt2[1,7]
                            if a>0 and b>0 and c>0:
                                meangmt2[0,7]=(a+b)/2                    
                    elif i==7:                            #BOTTOM LEFT CORNER
                        if j==0:
                            a=meangmt2[6,0]
                            b=meangmt2[7,1]
                            if a>0 and b>0:
                                meangmt2[7,0]=(a+b)/2
                        if j==7:                        #BOTTOM RIGHT CORNER
                            a=meangmt2[7,6]
                            b=meangmt2[6,7]
                            if a>0 and b>0:
                                meangmt2[7,7]=(a+b)/2  
                        if j>0 and j<7:                 #BOTTOM OF MODULE
                            a=meangmt2[i,j-1]
                            b=meangmt2[i,j+1]
                            c=meangmt2[i-1,j]
                            if a>0 and b>0 and c>0:
                                meangmt2[i,j]=(a+b+c)/3
                    elif j==0 and i>0 and i<7:          #RIGHT OF MODULE
                        a=meangmt2[i-1,j]
                        b=meangmt2[i,j+1]
                        c=meangmt2[i+1,j]
                        if a>0 and b>0 and c>0:
                            meangmt2[i,j]=(a+b+c)/3                       
                    elif j==7 and i>0 and i<7:          #LEFT OF MODULE
                        a=meangmt2[i-1,j]
                        b=meangmt2[i,j-1]
                        c=meangmt2[i+1,j]
                        if a>0 and b>0 and c>0:
                            meangmt2[i,j]=(a+b+c)/3     
    if size==48:
        #print ('coming soon')
        xyoffset=[0,8,16,24,32,40]
        errmat=np.zeros((6,6))
        errmat[0,0]=1
        errmat[0,5]=1
        errmat[5,0]=1
        errmat[5,5]=1
        bcs=np.zeros((6,6,9)) # define boundary conditions
        bcs[:,:,0] = [[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1]]
        bcs[:,:,1] = [[0,1,1,1,1,0],[1,0,0,0,0,1],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        bcs[:,:,2] = [[0,1,0,0,0,0],[1,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        bcs[:,:,3] = [[0,0,0,0,1,0],[0,0,0,0,0,1],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        bcs[:,:,4] = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[1,0,0,0,0,0],[0,1,0,0,0,0]]
        bcs[:,:,5] = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,1],[0,0,0,0,1,0]]
        bcs[:,:,6] = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[1,0,0,0,0,1],[0,1,1,1,1,0]]
        bcs[:,:,7] = [[0,0,0,0,1,0],[0,0,0,0,0,1],[0,0,0,0,0,1],[0,0,0,0,0,1],[0,0,0,0,0,1],[0,0,0,0,1,0]]
        bcs[:,:,8] = [[0,1,0,0,0,0],[1,0,0,0,0,0],[1,0,0,0,0,0],[1,0,0,0,0,0],[1,0,0,0,0,0],[0,1,0,0,0,0]]
        #print('Average of nearest neighbours (4 in the centre, 3 on the edge, 2 on the corner). Only works if the summing pixels are not dead too')
        for xo in range (0,6):
            for yo in range (0,6):
                xoff=xyoffset[xo]
                yoff=xyoffset[yo]
                #go to individual tile
                if errmat[xo,yo]==0:
                    ##Taking in a full camera array. Different techniques to average pixels, primarily from nearest neighbours.
                    for i in range (xoff+0,xoff+8):
                        for j in range (yoff+0,yoff+8):
                            if okpixel2[i,j]==0:    #could replace with a find locations of dead pixels
                                print (i, j, bcs[xo,yo,:], xoff, yoff)
                                ok=0
                                if i==xoff+0:
                                    print ('top')
                                    if bcs[xo,yo,1]==1 and j>yoff+0 and j<yoff+7:                 #TOP OF MODULE
                                        #print('Top of Module')
                                        a=meangmt2[i,j-1]
                                        b=meangmt2[i,j+1]
                                        c=meangmt2[i+1,j]
                                        if a!=0 and b!=0 and c!=0:
                                            meangmt2[i,j]=(a+b+c)/3
                                            ok=1
                                    elif bcs[xo,yo,2]==1:#j==yoff+0 and bcs[xo,yo,2]==1:                        #TOP LEFT CORNER
                                        #print('Top Left of Module', i, j)
                                        a=meangmt2[xoff+1,yoff+0]
                                        b=meangmt2[xoff+0,yoff+1]
                                        if a!=0 and b!=0:
                                            meangmt2[i,j]=(a+b)/2
                                            ok=1
                                    elif bcs[xo,yo,3]==1: # j==yoff+7 and bcs[xo,yo,3]==1:                        #TOP RIGHT CORNER
                                        a=meangmt2[xoff+0,yoff+6]
                                        b=meangmt2[xoff+1,yoff+7]
                                        if a!=0 and b!=0:
                                            meangmt2[i,j]=(a+b)/2
                                            ok=1
                                    else:# i>0 and i<7 and j>0 and j<7 and bcs[xo,yo,0]==1:     #CENTRE OF MODULE
                                        #print('Centre of Module', i, j)
                                        sum4=sumoffour(meangmt2,i,j,size)
                                        ok=sum4['ok']
                                        if ok==1:
                                            meangmt2[i,j]=sum4['e']
                                elif i>xoff+0 and i<xoff+7:                       #IN THE MIDDLE
                                    #print('right')
                                    if j==yoff+7 and i>xoff+0 and i<xoff+7  and bcs[xo,yo,7]==1 and ok==0:          #RIGHT OF MODULE
                                        a=meangmt2[i-1,j]
                                        b=meangmt2[i,j-1]
                                        c=meangmt2[i+1,j]
                                        if a>0 and b>0 and c>0:
                                            meangmt2[i,j]=(a+b+c)/3
                                            ok==1                                        
                                    elif j==yoff+0 and i>xoff+0 and i<xoff+7  and bcs[xo,yo,8]==1 and ok==0:          #LEFT OF MODULE
                                        a=meangmt2[i-1,j]
                                        b=meangmt2[i,j+1]
                                        c=meangmt2[i+1,j]
                                        if a>0 and b>0 and c>0:
                                            meangmt2[i,j]=(a+b+c)/3
                                            ok==1
                                    else:# i>0 and i<7 and j>0 and j<7 and bcs[xo,yo,0]==1:     #CENTRE OF MODULE
                                        sum4=sumoffour(meangmt2,i,j,size)
                                        ok=sum4['ok']
                                        if ok==1:
                                            meangmt2[i,j]=sum4['e']
                                elif i==xoff+7:                                   #BOTTOM       
                                    if j==yoff+0 and bcs[xo,yo,4]==1:       #BOTTOM LEFT CORNER
                                        #print('Bottom Left of Module')
                                        a=meangmt2[xoff+6,yoff+0]
                                        b=meangmt2[xoff+7,yoff+1]
                                        if a!=0 and b!=0:
                                            meangmt2[i,j]=(a+b)/2
                                    elif j==yoff+7 and bcs[xo,yo,5]==1:                        #BOTTOM RIGHT CORNER
                                        #print('Bottom Right of Module')
                                        a=meangmt2[xoff+7,yoff+6]
                                        b=meangmt2[xoff+6,yoff+7]
                                        if a!=0 and b!=0:
                                            meangmt2[i,j]=(a+b)/2  
                                    elif j>yoff+0 and j<yoff+7 and bcs[xo,yo,6]==1:                 #BOTTOM OF MODULE
                                        #print('Bottom of Module')
                                        a=meangmt2[i,j-1]
                                        b=meangmt2[i,j+1]
                                        c=meangmt2[i-1,j]
                                        if a!=0 and b!=0 and c!=0:
                                            meangmt2[i,j]=(a+b+c)/3
                                    else:# i>0 and i<7 and j>0 and j<7 and bcs[xo,yo,0]==1:     #CENTRE OF MODULE
                                        #print('Centre of Module', i, j)
                                        sum4=sumoffour(meangmt2,i,j,size)
                                        ok=sum4['ok']
                                        if ok==1:
                                            meangmt2[i,j]=sum4['e']                                         
                                elif i-1>-1 and j-1>-1 and i+1<48 and j+1<48:# i>0 and i<7 and j>0 and j<7 and bcs[xo,yo,0]==1:     #CENTRE OF MODULE
                                    #print('Centre of Module', i, j)
                                    sum4=sumoffour(meangmt2,i,j,size)
                                    ok=sum4['ok']
                                    if ok==1:
                                        meangmt2[i,j]=sum4['e'] 
    return meangmt2
def deadpixelalg2(size,okpixel2,meangmt2):
    if size==8:
        for i in range (0,8):
            for j in range (0,8):
                if okpixel2[i,j]==0:
                    if i==0 and j>0 and j<7:
                        #print('Along the top edge, not the corner. All samples around a dead pixel that are not also dead are summed and averaged')
                        count=0
                        abcdeok=np.zeros((5,2)) #a row 0, b row 1 etc. Value in col 0, multiplier in col 1
                        if meangmt2[i,j-1]>0:
                            count=count+1
                            abcdeok[0,0]=meangmt2[i,j-1]
                            abcdeok[0,1]=1
                        if meangmt2[i+1,j-1]>0:
                            count=count+1
                            abcdeok[1,0]=meangmt2[i+1,j-1]
                            abcdeok[1,1]=1              
                        if meangmt2[i+1,j]>0:
                            count=count+1
                            abcdeok[2,0]=meangmt2[i+1,j]
                            abcdeok[2,1]=1                   
                        if meangmt2[i+1,j+1]>0:
                            count=count+1
                            abcdeok[3,0]=meangmt2[i+1,j+1]
                            abcdeok[3,1]=1
                        if meangmt2[i,j+1]>0:
                            count=count+1
                            abcdeok[4,0]=meangmt2[i,j+1]
                            abcdeok[4,1]=1
                        if count>3:
                            meangmt2[i,j]=((abcdeok[0,0]*abcdeok[0,1])+(abcdeok[1,0]*abcdeok[1,1])+(abcdeok[2,0]*abcdeok[2,1])+(abcdeok[3,0]*abcdeok[3,1])+(abcdeok[4,0]*abcdeok[4,1]))/count
                        else:
                           print('No solution (yet) on ', i, ',', j)                     
                    if i>0 and i<7 and j>0 and j<7:
                        a=meangmt2[i,j-1]
                        b=meangmt2[i,j+1]
                        if b==0:
                            b=0.5*(meangmt2[i-1,j+1]+meangmt2[i+1,j+1])
                            if meangmt2[i-1,j+1]==0 or meangmt2[i+1,j+1]==0:
                                b=0
                        c=meangmt2[i+1,j]
                        if c==0:
                            c=0.5*(meangmt2[i+1,j-1]+meangmt2[i+1,j+1])
                            if meangmt2[i+1,j-1]==0 or meangmt2[i+1,j+1]==0:
                                c=0
                        d=meangmt2[i-1,j]
                        if a>0 and b>0 and c>0 and d>0:
                            meangmt2[i,j]=(a+b+c+d)/4
                        else:
                            sum8=sumofeight(meangmt2,i,j,size)
                            ok=sum8['ok']
                            if ok==1:
                                meangmt2[i,j]=sum8['e']  
                            else:
                                print('No solution (yet) on ', i, ',', j)                                        
                    if i>0 and i<7 and j==0:
                        b=meangmt2[i,j+1]
                        if b==0:
                            b=0.5*(meangmt2[i-1,j+1]+meangmt2[i+1,j+1])
                            if meangmt2[i-1,j+1]==0 or meangmt2[i+1,j+1]==0:
                                b=0
                        c=meangmt2[i,j-1]
                        if c==0:
                            c=0
                        d=meangmt2[i,j+1]
                        if d==0:
                            d=0.5*(meangmt2[i,j+2]+meangmt2[i+1,j+1])
                            if meangmt2[i,j+2]==0 or meangmt2[i+1,j+1]==0:
                                b=0                    
                        if b>0 and c>0 and d>0:
                            meangmt2[i,j]=(b+c+d)/3                              
                        else:
                            count=0
                            abcdeok=np.zeros((5,2)) #a row 0, b row 1 etc. Value in col 0, multiplier in col 1
                            if meangmt2[i-1,j]>0:
                                count=count+1
                                abcdeok[0,0]=meangmt2[i-1,j]
                                abcdeok[0,1]=1
                            if meangmt2[i-1,j+1]>0:
                                count=count+1
                                abcdeok[1,0]=meangmt2[i-1,j+1]
                                abcdeok[1,1]=1                                
                            if meangmt2[i,j+1]>0:
                                count=count+1
                                abcdeok[2,0]=meangmt2[i,j+1]
                                abcdeok[2,1]=1                   
                            if meangmt2[i+1,j+1]>0:
                                count=count+1
                                abcdeok[3,0]=meangmt2[i+1,j+1]
                                abcdeok[3,1]=1
                            if meangmt2[i+1,j]>0:
                                count=count+1
                                abcdeok[4,0]=meangmt2[i+1,j]
                                abcdeok[4,1]=1
                            if count>3:
                                meangmt2[i,j]=((abcdeok[0,0]*abcdeok[0,1])+(abcdeok[1,0]*abcdeok[1,1])+(abcdeok[2,0]*abcdeok[2,1])+(abcdeok[3,0]*abcdeok[3,1])+(abcdeok[4,0]*abcdeok[4,1]))/count
                            else:
                                print('No solution (yet) on ', i, ',', j)  
                    if i>0 and i<7 and j==7:
                        a=meangmt2[i,j-1]
                        b=meangmt2[i-1,j]
                        if b==0:
                            b=0
                        c=meangmt2[i+1,j]
                        if c==0:
                            c=0
                        if a>0 and b>0 and c>0:
                            meangmt2[i,j]=(a+b+c)/3       
                        else:
                            count=0
                            abcdeok=np.zeros((5,2)) #a row 0, b row 1 etc. Value in col 0, multiplier in col 1
                            if meangmt2[i-1,j]>0:
                                count=count+1
                                abcdeok[0,0]=meangmt2[i-1,j]
                                abcdeok[0,1]=1
                            if meangmt2[i-1,j-1]>0:
                                count=count+1
                                abcdeok[1,0]=meangmt2[i-1,j-1]
                                abcdeok[1,1]=1                                
                            if meangmt2[i,j-1]>0:
                                count=count+1
                                abcdeok[2,0]=meangmt2[i,j-1]
                                abcdeok[2,1]=1                   
                            if meangmt2[i+1,j-1]>0:
                                count=count+1
                                abcdeok[3,0]=meangmt2[i+1,j-1]
                                abcdeok[3,1]=1
                            if meangmt2[i+1,j]>0:
                                count=count+1
                                abcdeok[4,0]=meangmt2[i+1,j]
                                abcdeok[4,1]=1
                            if count>3:
                                meangmt2[i,j]=((abcdeok[0,0]*abcdeok[0,1])+(abcdeok[1,0]*abcdeok[1,1])+(abcdeok[2,0]*abcdeok[2,1])+(abcdeok[3,0]*abcdeok[3,1])+(abcdeok[4,0]*abcdeok[4,1]))/count
                            else:
                                print('No solution (yet) on ', i, ',', j) 
                    if i==7 and j>0 and j<7:
                        a=meangmt2[i,j-1]
                        b=meangmt2[i,j+1]
                        c=meangmt2[i-1,j]
                        if a>0 and b>0 and c>0:
                            meangmt2[i,j]=(a+b+c)/3   
                        else:
                            count=0
                            abcdeok=np.zeros((5,2)) #a row 0, b row 1 etc. Value in col 0, multiplier in col 1
                            if meangmt2[i,j-1]>0:
                                count=count+1
                                abcdeok[0,0]=meangmt2[i,j-1]
                                abcdeok[0,1]=1
                            if meangmt2[i-1,j-1]>0:
                                count=count+1
                                abcdeok[1,0]=meangmt2[i,j+1]
                                abcdeok[1,1]=1                                
                            if meangmt2[i,j-1]>0:
                                count=count+1
                                abcdeok[2,0]=meangmt2[i-1,j+1]
                                abcdeok[2,1]=1                   
                            if meangmt2[i+1,j-1]>0:
                                count=count+1
                                abcdeok[3,0]=meangmt2[i-1,j]
                                abcdeok[3,1]=1
                            if meangmt2[i+1,j]>0:
                                count=count+1
                                abcdeok[4,0]=meangmt2[i-1,j-1]
                                abcdeok[4,1]=1
                            if count>3:
                                meangmt2[i,j]=((abcdeok[0,0]*abcdeok[0,1])+(abcdeok[1,0]*abcdeok[1,1])+(abcdeok[2,0]*abcdeok[2,1])+(abcdeok[3,0]*abcdeok[3,1])+(abcdeok[4,0]*abcdeok[4,1]))/count
                            else:
                                print('No solution (yet) on ', i, ',', j) 
    if size ==40:
        sum8=sumofeight(meangmt2,i,j,size)
        ok=sum8['ok']
        if ok==1:
            meangmt2[i,j]=sum8['e']  
        else:
            print('No solution (yet) on ', i, ',', j) 
    return meangmt2
def checkdeadp(meangmt2,size,okpixel2):
    okpixeltot=0
    if size ==8:
        for i in range (0,8):
            for j in range (0,8):
                if meangmt2[i,j]>0:
                    okpixeltot=okpixeltot+1
                    okpixel2[i,j]=1
        print(okpixeltot, 'of 64 pixels are sorted.')
    if size ==48:
        for i in range (0,48):
            for j in range (0,48):
                if meangmt2[i,j]!=0:
                    okpixeltot=okpixeltot+1
                    okpixel2[i,j]=1
        print(okpixeltot, 'of 2048 pixels are sorted.')
    return {'okpixel2':okpixel2,'okpixeltot':okpixeltot}