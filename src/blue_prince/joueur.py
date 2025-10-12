# Gestion du joueur, de l'inventaire etc.
class Joueur:
    def __init__(self):
        self.pas = 70
        self.or_ = 0
        self.gemmes = 2
        self.cles = 0
        self.des = 0
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
        """
        Tente de déplacer le joueur dans une direction.
        Retourne True si le mouvement est possible (dans les limites), False sinon.
        Ne modifie la position que si le mouvement est valide.
        """
        temp_pos = list(self.position)
        moved = False

        if direction == "gauche" and self.position[0] > 0:
            temp_pos[0] -= 1
            moved = True
        elif direction == "droite" and self.position[0] < 4: # 5 colonnes (0-4)
            temp_pos[0] += 1
            moved = True
        elif direction == "haut" and self.position[1] > 0:
            temp_pos[1] -= 1
            moved = True
        elif direction == "bas" and self.position[1] < 8: # 9 lignes (0-8)
            temp_pos[1] += 1
            moved = True
        
        if moved:
            self.position = temp_pos
            return True
        
        return False