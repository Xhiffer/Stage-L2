# -*- coding: utf-8 -*-
"""
Created on Tue May 28 16:31:06 2019

@author: Villebon Charpak
"""

from PIL import Image#, ImageDraw
import sqlite3
#from time import time
import numpy as np
from skimage import io, color
#from skimage.viewer import ImageViewer


def gradim(lx, ly, gradMap, pixelMap):
    """
    prendre l'image en teinte de gris pour est la transphorme en image gradient
    
    Arguments :
        lx, ly = taille de l'image 
        gradMap = tupple des valeurs des pixels de l'image vierge 
                    sous forme luma
        pixelMap = tupple des valeurs des pixels de l'image que l'on observe 
                    sous forme luma
    Sortie :
        gradMap = tupple des valeurs des pixels de l'image sous forme 
                    luma mets en valeur les contraste de gris
    """
    for x in range(lx):
        for y in range(ly):
            if x == lx - 1 :
                gradMap[x, y] = (gradMap[x - 1, y],)
            elif y == ly - 1 :
                gradMap[x, y] = (gradMap[x, y - 1],)
            else :
                pixgrad = round(np.sqrt((pixelMap[x, y] -
                          pixelMap[x, y + 1])**2 + 
                          (pixelMap[x, y] - pixelMap[x + 1, y])**2))
                gradMap[x, y] = (int(pixgrad),)
    return gradMap

def rgb2labIMG():
    """
    prend l'image RGB, la transphorme en lab et crée une image avec 
    la valeur de Chromas 
    Arguments :
        path + picname = le fichier de l'image 
    Sortie : 
        liste de la valeur de chroma pixel par pixel
    """
    saturation = []
    rgb = io.imread(path + picname)
    lab = color.rgb2lab(rgb)
    for x in range(lx):
        saturationy = []
        for y in range(ly):
            C = np.sqrt(lab[y][x][1]**2 + lab[y][x][2]**2)
            saturationy.append(C)
        saturation.append(saturationy)
    return saturation

def Loadimg() :
    """
    ouvre l'image que l'ont vas observé 
    Arguments:
        path + picname : destination du ficher de l'image
    Sortie :
        im = image convertie en luma
        imload = tupples qui garde en information les valeurs 
                des pixels de l'image im 
        pm = image blance avec la taille de l'image im
        pmload = tupples qui garde en information les valeurs 
                des pixels de l'image pm
        lx = taille x de l'image im
        ly = taille y de l'image im
    """
    im = Image.open(path + picname)
    im = im.convert('L')
    imload = im.load()
    lx, ly = im.size
    pm = Image.new('L', (lx, ly), color = 'white')
    gradMap = pm.load()
    return im, imload, pm, gradMap, lx, ly



def MIformule(yi,xi,masse):
    """
    formule du moment d'inertie 
    Arguments :
        yi = axe y de notre point observé
        xi = axe x de notre point observé
        masse = liste des masse de chaque pixel de notre image 
    """
    SMI =0
    for x in range(0, lx):
            for y in range(ly):
                try :
                    SMI += (masse[x, y] * ((( - ly / 2 + y) -
                        ( - ly / 2 + yi))**2 + (( - lx / 2 + xi) -
                        ( - lx / 2 + x))**2))
                except TypeError: 
                    SMI += (masse[x][y] * ((( - ly / 2 + y) -
                            ( - ly / 2 + yi))**2 + (( - lx / 2 + xi) -
                            ( - lx / 2 + x))**2))
    return SMI



def INITmomentinertie(masse) :
    """
    prend 5 point sur notre image (chaque angle et le point du centre)
    et calcule leurs moment d'inertie 
    Arguments : 
        masse = tupple des masses de chaque pixel de notre image
    Sortie :
        flatpix = tupple [[moment d'inertie, positionX, positionY],...] 
                de nos 5 points
    """
    
    
    flatpix = []
    for xi, yi in zip ([0, lx, 0, lx, lx / 2], [0, ly, ly, 0, ly / 2]):
        SMI = MIformule(yi, xi, masse)
        flatpix.append([SMI, xi, yi])
    return flatpix

def CSquare(flatpix, masse):
    """
    fonction recurcive qui fait un carré avec le centre du carré précédent et 
    le point avec la valeur de moment d'inertie la plus faible des 4 points
    du carrée précédent jusqu'a que le centre du carré précédent et 
    le point le plus failble du carré précédent n'ont plus de pixel d'écart
    Arguments : 
        flatpix = tupple [[moment d'inertie, positionX, positionY],...] 
                de nos 5 points
        masse = tupple des masses de chaque pixel de notre image
    Sortie :
        tupple = [moment d'inertie, positionX, positionY] du centre de 
                 gravité de l'image
    """
    cdimg = flatpix[-1]
    flatpix = sorted(flatpix[:-1], key=lambda tup: tup[0])
    minMI = flatpix[0]
    
    flatpix = [minMI] + [cdimg]
    for xi, yi in zip ([minMI[1], cdimg[1], 
                        (cdimg[1] + (minMI[1] - cdimg[1]) / 2)],
                        [cdimg[2], minMI[2], 
                         (cdimg[2] + (minMI[2] - cdimg[2]) / 2)]):
        SMI = MIformule(yi, xi, masse)
        flatpix.append([SMI, xi, yi])
    if round(flatpix[-1][1]) == round(flatpix[0][1]) :
        return  flatpix[-1]
    return CSquare(flatpix, masse)


if __name__ == "__main__":
        #======
    counttimes = 200
    path = 'C:/Users/Villebon/Desktop/AVA_dataset/images/images/'
    conn = sqlite3.connect('AVA.db')
    c = conn.cursor()
    f = open("C:/Users/Villebon/Desktop/idAVA6.txt", "r")
    curentid = f.read()
    curentid = int(curentid)
    f.close()
    c.execute("""SELECT id FROM AVA WHERE ID >? 
              AND CDGGRAYtoCDimg IS NULL LIMIT ?""",
               [curentid, counttimes])
    a = c.fetchall()
    for i in a:#range(curentid, curentid +100):
        picname = str(i[0]) + '.jpg'
        try :
            im, imload, pm, gradMap, lx, ly = Loadimg()
            #saturation test
            try :
                saturation = rgb2labIMG() #problème si pas rgb ?
                flatpix = INITmomentinertie(255 * saturation)
                cdgSAT = CSquare(flatpix, 255 * saturation)
                cdgSAT2 = ((abs(cdgSAT[1] - lx / 2) + abs(cdgSAT[2] - ly / 2))/ 
                           (abs(lx - lx / 2) + abs(ly - ly / 2)))
                cdgSAT2 = round(cdgSAT2, 4)
                c.execute("UPDATE AVA SET CDGSATtoCDimg = {} WHERE id = {}".
                          format(cdgSAT2, i[0]))
                c.execute("UPDATE AVA SET CDGSaturation = ? WHERE id = ?",
                          [str(cdgSAT), i[0]])
            except ValueError:
                """
                si l'image est noir est blanc, peut pas calculé la saturation
                """
                print("picture black and white" , i[0])
            #grad test 
            gradMap = gradim(lx, ly, gradMap, imload)
            flatpix = INITmomentinertie(gradMap)
            cdgGRAD = CSquare(flatpix, gradMap)
            cdgGRAD2 = ((abs(cdgGRAD[1] - lx / 2) + abs(cdgGRAD[2] - ly / 2))/ 
                        (abs(lx - lx / 2) + abs(ly - ly / 2)))
            #gray test
            flatpix = INITmomentinertie(imload)
            cdgGRAY = CSquare(flatpix, imload)
            cdgGRAY2 = ((abs(cdgGRAY[1] - lx / 2) + abs(cdgGRAY[2] - ly / 2)) / 
            (abs(lx - lx / 2) + abs(ly - ly / 2)))
            c.execute("UPDATE AVA SET imgexist = {} WHERE id = {}"
                      .format(1, i[0]))
            cdgGRAY2 = round(cdgGRAY2, 4)
            cdgGRAD2 = round(cdgGRAD2, 4)
            c.execute("UPDATE AVA SET CDGGRAYtoCDimg = {} WHERE id = {}"
                      .format(cdgGRAY2, i[0]))
            c.execute("UPDATE AVA SET CDGGRADtoCDimg = {} WHERE id = {}"
                      .format(cdgGRAD2, i[0]))
            c.execute("UPDATE AVA SET CDGGray = ? WHERE id = ?",
                      [str(cdgGRAY), i[0]])
            c.execute("UPDATE AVA SET CDGGradient = ? WHERE id = ?", 
                      [str(cdgGRAD), i[0]])
        except FileNotFoundError:
            """
            Si l'image n'est pas dans ma base de donnée d'image de mon pc,passe
            """
            c.execute("UPDATE AVA SET imgexist = ? WHERE id = ?", [0,i[0]])
            print("picture" , i[0])
    f = open("C:/Users/Villebon/Desktop/idAVA6.txt", "w")
    f.write(str(a[~0][0]))
    f.close()
    conn.commit()
    conn.close()

    