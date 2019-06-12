# -*- coding: utf-8 -*-
"""
Created on Wed May 29 16:23:06 2019

@author: Villebon Charpak
"""

import sqlite3
import matplotlib.pyplot as plt
#import matplotlib.mlab as mlab

conn = sqlite3.connect('AVA.db')
c = conn.cursor()
c.execute("""SELECT id, AVGBeautyScore, CDGGRAYtoCDimg, CDGGRADtoCDimg, CDGSATtoCDimg
          FROM AVA  WHERE CDGGRADtoCDimg NOT NULL AND CDGSATtoCDimg NOT NULL""")
l = c.fetchall()
flatpix = sorted(l, key=lambda tup: tup[1])
beautymin =  flatpix[0]
beautymax =flatpix[-1]


flatpix = sorted(l, key=lambda tup: tup[2])
lmax2 = flatpix[-1]
lmin2 = flatpix[0]
for i in l:
    plt.scatter(i[1],i[2])
plt.axis([ beautymin[1]-0.5, beautymax[1]+0.5,lmin2[2]-0.05, lmax2[2]+0.05])
plt.ylabel('cdg of gray')
plt.xlabel('beauty score')
plt.savefig('C:/Users/Villebon/Desktop/Graphes-AVA/gray-beauty.jpg')
plt.show()
plt.close()

listb = [0]*40
for i in l :
    listb[int((round(i[1]*2)/2)*2*2)] +=i[2]
    listb[int((round(i[1]*2)/2)*2*2+1)] += 1
for i in range(0,len(listb),2):
    

    try:
        listb[i] = listb[i]/listb[i+1]
        plt.plot((i)/4,listb[i], 'ro')
    except ZeroDivisionError:
        pass
plt.ylabel('cdg of gray')
plt.xlabel('beauty score rounded to 0,5')
plt.axvline(x=4.5,color='red',linestyle = '--')
plt.axvline(x=6.5,color='red',linestyle = '--')
plt.savefig('C:/Users/Villebon/Desktop/Graphes-AVA/avg-gray-beauty.jpg')
plt.show()
plt.close()






flatpix = sorted(l, key=lambda tup: tup[3])
lmax2 = flatpix[-1]
lmin2 = flatpix[0]
for i in l:
    plt.scatter(i[1],i[3])
plt.axis([ beautymin[1]-0.5, beautymax[1]+0.5,lmin2[3]-0.05, lmax2[3]+0.05])
plt.ylabel('cdg of gradient')
plt.xlabel('beauty score')
plt.savefig('C:/Users/Villebon/Desktop/Graphes-AVA/grad-beauty.jpg')
plt.show()
plt.close()
listb = [0]*40
for i in l :
    listb[int((round(i[1]*2)/2)*2*2)] +=i[3]
    listb[int((round(i[1]*2)/2)*2*2+1)] += 1
for i in range(0,len(listb),2):
    

    try:
        listb[i] = listb[i]/listb[i+1]
        plt.plot((i)/4,listb[i], 'ro')
    except ZeroDivisionError:
        pass
plt.ylabel('cdg of gradient')
plt.xlabel('beauty score rounded to 0,5')
plt.axvline(x=4.5,color='red',linestyle = '--')
plt.axvline(x=6.5,color='red',linestyle = '--')
plt.savefig('C:/Users/Villebon/Desktop/Graphes-AVA/avg-grad-beauty.jpg')
plt.show()
plt.close()









flatpix = sorted(l, key=lambda tup: tup[4])
lmax2 = flatpix[-1]
lmin2 = flatpix[0]
for i in l:
    plt.scatter(i[1],i[4])
plt.axis([ beautymin[1]-0.5, beautymax[1]+0.5,lmin2[4]-0.05, lmax2[4]+0.05])
plt.ylabel('cdg of Saturation')
plt.xlabel('beauty score')
plt.savefig('C:/Users/Villebon/Desktop/Graphes-AVA/sat-beauty.jpg')
plt.show()
plt.close()

listb = [0]*40
for i in l :
    listb[int((round(i[1]*2)/2)*2*2)] +=i[4]
    listb[int((round(i[1]*2)/2)*2*2+1)] += 1
for i in range(0,len(listb),2):
    

    try:
        listb[i] = listb[i]/listb[i+1]
        plt.plot((i)/4,listb[i], 'ro')
    except ZeroDivisionError:
        pass
plt.ylabel('cdg of Saturation')
plt.xlabel('beauty score rounded to 0,5')
plt.axvline(x=4.5,color='red',linestyle = '--')
plt.axvline(x=6.5,color='red',linestyle = '--')
plt.savefig('C:/Users/Villebon/Desktop/Graphes-AVA/avg-sat-beauty.jpg')
plt.show()
plt.close()

his = []
listb = listb[1:]
for num,i in enumerate(listb[::2]):
    print(i)
    plt.hist([num]*i,range = (5,16),color='red', alpha=0.5)
plt.ylabel('number of pictures')
plt.xlabel('beauty score')
plt.savefig('C:/Users/Villebon/Desktop/Graphes-AVA/num-pic-beauty.jpg')
plt.show()
plt.close()
