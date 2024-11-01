import cv2


def transforme (taille, indice):

    destination = (indice - 1) // 2
    if indice % 2 == 0:
        destination += taille // 2 + 1
        
    return destination


def photomaton (image):

    copie = image.copy ()
    hauteur = copie.shape[0]
    largeur = copie.shape[1]
    
    for ligne in range (hauteur):
        for colonne in range (largeur):
            pixel = image[ligne][colonne][:]
            copie[transforme (hauteur, ligne)][transforme (largeur, colonne)] = pixel
            
    return copie
