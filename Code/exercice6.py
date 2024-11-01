import cv2


def pixelise (image, reduction):

    copie = image.copy ()
    hauteur = copie.shape[0]
    largeur = copie.shape[1]
    
    hauteurReduite = hauteur // reduction
    largeurReduite = largeur // reduction
    modele = [[[None, None, None] for _ in range (largeurReduite)] for _ in range (hauteurReduite)]
    
    for ligneReduite in range (hauteurReduite):
        for colonneReduite in range (largeurReduite):
            pixel = modele[ligneReduite][colonneReduite]
            
            for couleur in range (3):
            
                compte = reduction ** 2
                somme = 0
                for ligne in range (ligneReduite * reduction, (ligneReduite + 1) * reduction):
                    for colonne in range (colonneReduite * reduction, (colonneReduite + 1) * reduction):
                        somme += image[ligne][colonne][couleur]
                        
                moyenne = somme // compte
                pixel[couleur] = moyenne
    
    for ligne in range (hauteur):
        for colonne in range (largeur):
            pixel = copie[ligne][colonne]
            
            for couleur in range (3):
                pixel[couleur] = modele[ligne // reduction][colonne // reduction][couleur]
            
    return copie
