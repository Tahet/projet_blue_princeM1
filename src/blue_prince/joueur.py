# Gestion du joueur, de l'inventaire etc.
class Joueur:
    def __init__(self):
        self.pas = 70
        self.or_ = 0
        self.gemmes = 2
        self.clefs = 0
        #self.des = 0
        self.position = [2, 8]  # Position initiale [colonne, ligne]

    # Gestion des pas
    def ajouter_pas(self, nombre):
        self.pas += nombre
    def utiliser_pas(self):
        if self.pas <= 0:
            return False
        self.pas -= 1
        return True

    # Gestion de l'or
    def ajouter_or(self, montant):
        self.or_ += montant

    def utiliser_or(self, montant):
        if montant > self.or_:
            return False
        self.or_ -= montant
        return True
    
    # Gestion des gemmes
    def ajouter_gemmes(self, nb):
        self.gemmes += nb
        
    def utiliser_gemmes(self, nb):
        if nb > self.gemmes:
            return False
        self.gemmes -= nb
        return True

    def deplacer(self, direction): 
        if (direction == "gauche" and self.position[0] > 0):
            self.position[0] -= 1
            return True

        if (direction == "droite" and self.position[0] < 4):
            self.position[0] += 1
            return True

    
        if (direction == "haut" and self.position[1] > 0):
            self.position[1] -= 1
            return True

        if (direction == "bas" and self.position[1] < 8):
            self.position[1] += 1
            return True
        
        return False