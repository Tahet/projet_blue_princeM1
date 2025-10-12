import os
import pygame

class Piece:
    def __init__(self, directions, nom, cles_nes=[], icon_img=None):
        self.directions = directions  # Liste des directions possibles (ex: ["haut", "bas", "gauche", "droite"])
        self.visitee = False  # Indique si la pièce a été visitée
        self.objets = []  # Liste des objets présents dans la pièce
        self.icon_img = icon_img
        self.nom = nom
        self.cles_nes = cles_nes

    def ajouter_objet(self, objet):
        self.objets.append(objet)

    def retirer_objet(self, objet):
        if objet in self.objets:
            self.objets.remove(objet)

    def acheter_objet(self, objet, joueur):
        if objet in self.objets:
            if joueur.utiliser_or(objet.prix):
                self.retirer_objet(objet)
                return True
        return False

def charger_pieces_blue_prince(cell_w, cell_h, Piece):
    """
    Charge toutes les images de pièces, les redimensionne et crée des objets Piece.
    Les pièces qui nécessitent une clé pour certaines directions doivent spécifier
    cette liste dans le dictionnaire de données.
    """
    
    # 1. Définir les données des pièces
    pieces_data = [
        {"file": "Entrance_Hall.webp", "name": "Entrance Hall", "connexions": ["N", "E", "W"]},
        {"file": "Antechamber.webp", "name": "Antechamber", "connexions": ["N", "E", "S", "W"], "cles_nes": ["N", "E", "S", "W"]},
        {"file": "Bedroom.webp", "name": "Bedroom", "connexions": ["N", "E", "S", "W"]},
        {"file": "Closet.webp", "name": "Closet", "connexions": ["S"]},
        {"file": "Commissary.webp", "name": "Commissary", "connexions": ["N", "E", "S"]},
        {"file": "Corridor.webp", "name": "Corridor", "connexions": ["N", "S"]},
        {"file": "Den.webp", "name": "Den", "connexions": ["N", "E", "S", "W"]},
        {"file": "East_Wing_Hall.webp", "name": "East Wing Hall", "connexions": ["N", "E", "S", "W"]},
        {"file": "Locksmith.webp", "name": "Locksmith", "connexions": ["S", "W"]},
        {"file": "Master_Bedroom.webp", "name": "Master Bedroom", "connexions": ["N", "E", "S", "W"]},
        {"file": "Passageway.webp", "name": "Passageway", "connexions": ["N", "E", "S", "W"]},
        {"file": "Rumpus_Room.webp", "name": "Rumpus Room", "connexions": ["N", "E", "S", "W"]},
        {"file": "Vault.webp", "name": "Vault", "connexions": ["E", "S", "W"]},
        {"file": "Weight_Room.webp", "name": "Weight Room", "connexions": ["N", "E", "S", "W"]},
    ]

    salles_chargees = []
    base_dir = os.path.join(os.path.dirname(__file__), "data")

    for data in pieces_data:
        img_path = os.path.join(base_dir, data["file"])
        
        try:
            icon_img = pygame.image.load(img_path).convert_alpha()
            icon_img = pygame.transform.scale(icon_img, (cell_w, cell_h))
            
            # Récupérer cles_nes, ou utiliser une liste vide si la clé n'est pas spécifiée
            cles_necessaires = data.get("cles_nes", [])
            
            # 3. Créer l'objet Piece avec les 4 arguments positionnels
            nouvelle_piece = Piece(
                data["connexions"],
                data["name"],
                cles_necessaires, 
                icon_img          
            )
            salles_chargees.append(nouvelle_piece)
            
        except pygame.error as e:
            print(f"Erreur de chargement pour {data['file']} : {e}")

    return salles_chargees