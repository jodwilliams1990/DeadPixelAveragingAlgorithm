import sys
sys.path.append('../')
sys.path.append('../../')
import numpy as np
import DPAABE

test=0
readin=1 
ieve=round(np.random.rand()*2047)
#while ieve<2048:    
if test==1:
    #READ IN AND PREP TEST DATA
    testreadina=DPAABE.testreadin()
    data=testreadina['data']
    okpixel2=testreadina['okpixel2'] 
    size=testreadina['size']
if readin==1:
    #READ IN AND PREP REAL DATA
    datareadina=DPAABE.datareadin(ieve)
    data=datareadina['data']
    okpixel2=datareadina['okpixel2']    
    size=datareadina['size'] 
    lencharge=datareadina['lencharge'] 
meangmt2=1*data

#Dead Pixel Averaging Algorithm
okpixelactual=okpixel2
okpixeltot=1
runtwice=1
runtwicea=1
while runtwicea<3 and okpixeltot<lencharge:
    while runtwice<3 and okpixeltot<lencharge:
        meangmt2=DPAABE.deadpixelalg1(size,okpixel2,meangmt2)
        dpcheck=DPAABE.checkdeadp(meangmt2,size,okpixel2)
        okpixeltot=dpcheck['okpixeltot']
        if okpixeltot<lencharge:
            okpixel2=dpcheck['okpixel2']
        runtwice=runtwice+1
    if okpixeltot<size:
        meangmt2=DPAABE.deadpixelalg2(size,okpixel2,meangmt2)
        dpcheck=DPAABE.checkdeadp(meangmt2,size,okpixel2)
        okpixeltot=dpcheck['okpixeltot']
        if okpixeltot<64:
            okpixel2=dpcheck['okpixel2']
    runtwicea=runtwicea+1
    #if okpixeltot<2048:
    #    print ('ieve is', ieve)
    #    break
    #else:
    #    ieve=ieve+1
if size==64:
    print('Coming Soon')