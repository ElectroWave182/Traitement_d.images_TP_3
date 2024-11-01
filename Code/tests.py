import cv2
from pathlib import Path
from matplotlib import pyplot

from exercice1 import *
from exercice3 import *
from exercice6 import *


def main ():
    
    
    # Initialisation
    
    nbLignes = 5
    nbColonnes = 9
    compteur = 1


    # Read images

    cheminImages = str (Path (__file__).resolve ().parent) + "/images/"
    
    bouc1 = cv2.imread (cheminImages + "morph_1.pgm")
    humain = cv2.imread (cheminImages + "morph_2.pgm")
    bouc2 = cv2.imread (cheminImages + "morph_3.pgm")
    
    lieu1 = cv2.imread (cheminImages + "source.jpg")
    lieu2 = cv2.imread (cheminImages + "source2.jpeg")
    lieu3 = cv2.imread (cheminImages + "source3.jpg")
    charlie1 = cv2.imread (cheminImages + "template.jpg")
    charlie2 = cv2.imread (cheminImages + "template2.jpeg")
    charlie3 = cv2.imread (cheminImages + "template3.jpg")
    
    lena = cv2.imread (cheminImages + "lena.jpg")
    
    chessboard = cv2.imread (cheminImages + "chessboard.png")
    
    
    # Treat them
    
    boucBinaire127 = binaire (bouc1, 127)
    boucBinaire200 = binaire (bouc1, 200)
    structurantGros = list ()
    structurantGros.append ([False, False, False, True,  False, False])
    structurantGros.append ([False, False, True,  True,  True,  False])
    structurantGros.append ([True,  True,  True,  True,  True,  True ])
    structurantGros.append ([False, False, True,  True,  True,  False])
    structurantGros.append ([False, False, False, True,  False, False])
    boucErodeBcp = erosion (boucBinaire200, structurantGros)
    boucDilateBcp = dilatation (boucBinaire200, structurantGros)
    structurantPetit = list ()
    structurantPetit.append ([False, True,  False])
    structurantPetit.append ([True,  True,  True ])
    structurantPetit.append ([False, True,  False])
    boucErodePeu = erosion (boucBinaire200, structurantPetit)
    boucDilatePeu = dilatation (boucBinaire200, structurantPetit)
    boucOuvert = dilatation (boucErodePeu, structurantGros)
    boucContours = soustraction (boucErodePeu, boucDilatePeu)
    boucPropre = contoursPropres (boucBinaire200, structurantPetit)
    boucDecape = contoursPropres (boucBinaire200, structurantGros)
    
    trouve1 = cv2.matchTemplate (lieu1, charlie1, cv2.TM_CCORR_NORMED)
    trouve2 = cv2.matchTemplate (lieu2, charlie2, cv2.TM_CCORR_NORMED)
    trouve3 = cv2.matchTemplate (lieu3, charlie3, cv2.TM_CCORR_NORMED)
    
    bouc1Mosaique = photomaton (bouc1)
    humainMosaique = photomaton (humain)
    bouc2Mosaique = photomaton (bouc2)
    
    lenaGradient = cv2.Sobel (src = lena, ddepth = -1, dx = 1, dy = 0, ksize = 5)
    
    # Nuances de gris
    lenaCompatible = cv2.cvtColor (lena, cv2.COLOR_BGR2GRAY)
    lenaCompatible = float32 (lenaCompatible)
    lenaCorners = cv2.cornerHarris (lenaCompatible, 2, 5, 0.07)
    chessboardCompatible = cv2.cvtColor (chessboard, cv2.COLOR_BGR2GRAY)
    chessboardCompatible = float32 (chessboardCompatible)
    print (chessboardCompatible)
    chessboardCorners = cv2.cornerHarris (chessboardCompatible, 2, 5, 0.07)
    
    lenaPixelisee = pixelise (lena, 10)
    
    
    # Show result
    
    pyplot.subplot (nbLignes, nbColonnes, compteur)
    pyplot.imshow (cv2.cvtColor (bouc1, cv2.COLOR_BGR2RGB))
    pyplot.title ("1.1) Base")
    compteur += 1
    
    pyplot.subplot (nbLignes, nbColonnes, compteur)
    pyplot.imshow (boucBinaire127, cmap = "gray")
    pyplot.title ("1.1) Seuil à 127")
    compteur += 1
    
    pyplot.subplot (nbLignes, nbColonnes, compteur)
    pyplot.imshow (boucBinaire200, cmap = "gray")
    pyplot.title ("1.1) Seuil à 200")
    compteur += 1
    
    pyplot.subplot (nbLignes, nbColonnes, compteur)
    pyplot.imshow (boucErodeBcp, cmap = "gray")
    pyplot.title ("1.2) Croix 5x6")
    compteur += 1
    
    pyplot.subplot (nbLignes, nbColonnes, compteur)
    pyplot.imshow (boucErodePeu, cmap = "gray")
    pyplot.title ("1.2) Croix 3x3")
    compteur += 1
    
    pyplot.subplot (nbLignes, nbColonnes, compteur)
    pyplot.imshow (boucOuvert, cmap = "gray")
    pyplot.title ("1.3)")
    compteur += 1
    
    pyplot.subplot (nbLignes, nbColonnes, compteur)
    pyplot.imshow (boucContours, cmap = "gray")
    pyplot.title ("1.4)")
    compteur += 1
    
    pyplot.subplot (nbLignes, nbColonnes, compteur)
    pyplot.imshow (boucPropre, cmap = "gray")
    pyplot.title ("1.5) Croix 3x3")
    compteur += 1
    
    pyplot.subplot (nbLignes, nbColonnes, compteur)
    pyplot.imshow (boucDecape, cmap = "gray")
    pyplot.title ("1.5) Croix 5x6")
    compteur += 1
    
    pyplot.subplot (nbLignes, nbColonnes, compteur)
    pyplot.imshow (cv2.cvtColor (trouve1, cv2.COLOR_BGR2RGB))
    pyplot.title ("2) Montagnes")
    compteur += 1
    
    pyplot.subplot (nbLignes, nbColonnes, compteur)
    pyplot.imshow (cv2.cvtColor (trouve2, cv2.COLOR_BGR2RGB))
    pyplot.title ("2) Iles")
    compteur += 1
    
    pyplot.subplot (nbLignes, nbColonnes, compteur)
    pyplot.imshow (cv2.cvtColor (trouve3, cv2.COLOR_BGR2RGB))
    pyplot.title ("2) Plage")
    compteur += 1
    
    pyplot.subplot (nbLignes, nbColonnes, compteur)
    pyplot.imshow (cv2.cvtColor (bouc1Mosaique, cv2.COLOR_BGR2RGB))
    pyplot.title ("3.2) 1er bouc")
    compteur += 1
    
    pyplot.subplot (nbLignes, nbColonnes, compteur)
    pyplot.imshow (cv2.cvtColor (humainMosaique, cv2.COLOR_BGR2RGB))
    pyplot.title ("3.2) Humain")
    compteur += 1
    
    pyplot.subplot (nbLignes, nbColonnes, compteur)
    pyplot.imshow (cv2.cvtColor (bouc2Mosaique, cv2.COLOR_BGR2RGB))
    pyplot.title ("3.2) 2e bouc")
    compteur += 1
    
    pyplot.subplot (nbLignes, nbColonnes, compteur)
    pyplot.imshow (cv2.cvtColor (lenaGradient, cv2.COLOR_BGR2RGB))
    pyplot.title ("4)")
    compteur += 1
    
    pyplot.subplot (nbLignes, nbColonnes, compteur)
    pyplot.imshow (cv2.cvtColor (lenaCorners, cv2.COLOR_BGR2RGB))
    pyplot.title ("5.1) Lena")
    compteur += 1
    
    pyplot.subplot (nbLignes, nbColonnes, compteur)
    pyplot.imshow (cv2.cvtColor (chessboardCorners, cv2.COLOR_BGR2RGB))
    pyplot.title ("5.1) Chessboard")
    compteur += 1
    
    pyplot.subplot (nbLignes, nbColonnes, compteur)
    pyplot.imshow (cv2.cvtColor (lenaPixelisee, cv2.COLOR_BGR2RGB))
    pyplot.title ("6.1)")
    compteur += 1
    
    
    pyplot.show ()


main ()
