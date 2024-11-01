import cv2
from numpy import *


def binaire (image, seuil):

    copie = image.copy ()
    hauteur = copie.shape[0]
    largeur = copie.shape[1]
    
    for ligne in range (hauteur):
        for colonne in range (largeur):
            pixel = copie[ligne][colonne]
            
            for couleur in range (3):
                if pixel[couleur] < seuil:
                    pixel[couleur] = 0
                else:
                    pixel[couleur] = 255
                    
    return copie
    

def estBlanc (pixel):

    for couleur in pixel:
        if couleur == 0:
            return False
            
    return True


def estNoir (pixel):

    for couleur in pixel:
        if couleur != 0:
            return False
            
    return True


def erosion (image, structurant):

    copie = image.copy ()
    hauteur = copie.shape[0]
    largeur = copie.shape[1]
    
    amplitudeHorizontale = (len (structurant) - 1) // 2
    pariteHorizontale = len (structurant) % 2
    amplitudeVerticale = (len (structurant[0]) - 1) // 2
    pariteVerticale = len (structurant) % 2
    centre = structurant[amplitudeHorizontale][amplitudeVerticale]
    
    for ligne in range (hauteur):
        for colonne in range (largeur):
            pixel = copie[ligne][colonne]
            erode = False
            
            for ligneStructurante in range (-amplitudeHorizontale, amplitudeHorizontale + pariteHorizontale):
                for colonneStructurante in range (-amplitudeVerticale, amplitudeVerticale + pariteVerticale):

                    condition = structurant[ligneStructurante + amplitudeHorizontale][colonneStructurante + amplitudeVerticale]
                    condition = condition and 0 <= ligneStructurante + ligne < hauteur
                    condition = condition and 0 <= colonneStructurante + colonne < largeur
                    condition = condition and estBlanc (image[ligne + ligneStructurante][colonne + colonneStructurante])
                    if condition:

                        # Érosion du pixel
                        for couleur in range (3):
                            pixel[couleur] = 255
                        
                        erode = True
                        break
                if erode:
                    break
                    
    return copie


def dilatation (image, structurant):

    copie = image.copy ()
    hauteur = copie.shape[0]
    largeur = copie.shape[1]
    
    amplitudeHorizontale = (len (structurant) - 1) // 2
    pariteHorizontale = len (structurant) % 2
    amplitudeVerticale = (len (structurant[0]) - 1) // 2
    pariteVerticale = len (structurant) % 2
    centre = structurant[amplitudeHorizontale][amplitudeVerticale]
    
    for ligne in range (hauteur):
        for colonne in range (largeur):
            pixel = copie[ligne][colonne]
            erode = False
            
            for ligneStructurante in range (-amplitudeHorizontale, amplitudeHorizontale + pariteHorizontale):
                for colonneStructurante in range (-amplitudeVerticale, amplitudeVerticale + pariteVerticale):

                    condition = structurant[ligneStructurante + amplitudeHorizontale][colonneStructurante + amplitudeVerticale]
                    condition = condition and 0 <= ligneStructurante + ligne < hauteur
                    condition = condition and 0 <= colonneStructurante + colonne < largeur
                    condition = condition and estNoir (image[ligne + ligneStructurante][colonne + colonneStructurante])
                    if condition:

                        # Dilatation du pixel
                        for couleur in range (3):
                            pixel[couleur] = 0
                        
                        erode = True
                        break
                if erode:
                    break
                    
    return copie


def soustraction (positive, negative):

    hauteur = max (positive.shape[0], negative.shape[0])
    largeur = max (positive.shape[1], negative.shape[1])
    copie = [[array ([0, 0, 0]) for _ in range (largeur)] for _ in range (hauteur)]
    
    for ligne in range (hauteur):
        for colonne in range (largeur):
            pixel = copie[ligne][colonne]
            
            positifExiste = ligne < positive.shape[0] and colonne < positive.shape[1]
            negatifExiste = ligne < negative.shape[0] and colonne < negative.shape[1]
            
            # Les coordonnées sont dans les limites des 2 images
            if positifExiste and negatifExiste:
                positif = positive[ligne][colonne]
                negatif = negative[ligne][colonne]
                for couleur in range (3):
                    pixel[couleur] = positif[couleur] - negatif[couleur]
            
            # Les coordonnées sortent de l'image négative
            elif positifExiste:
                positif = positive[ligne][colonne]
                for couleur in range (3):
                    pixel[couleur] = positif[couleur]
            
            # Les coordonnées sortent de l'image positive
            else:
                negatif = negative[ligne][colonne]
                for couleur in range (3):
                    pixel[couleur] = -negatif[couleur]
                    
            for couleur in range (3):
                pixel[couleur] = abs (pixel[couleur])
                
    return copie


def contoursPropres (image, structurant):

    propreErodee = erosion (erosion (dilatation (image, structurant), structurant), structurant)
    propreDilatee = dilatation (dilatation (image, structurant), structurant)
    
    return soustraction (propreErodee, propreDilatee)
