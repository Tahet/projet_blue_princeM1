PROJET POO BLUE PRINCE M1
=====================

DESCRIPTION
-----------
Ce projet implémente une version simplifiée vu du haut du jeu Blue Prince connu.

PRÉREQUIS
---------
- Python 3.12.10
- pygame

INSTALLATION
------------
1. Cloner le dépôt
2. Installer les dépendances : pip install -r requirements.txt

UTILISATION
-----------
Il suffit d'exécuter le fichier main.py
python main.py

Les contrôles sont :
ZQSD pour choisir le mouvement, ESPACE pour confirmer
Pour tirer une pièce ; Z/S puis ESPACE pour confirmer
Si vous avez un dé, il est possible de relancer le tirage avec F

RÈGLES DU JEU
-------------
Objectif : Atteindre l'Antechamber avant d'épuiser vos pas.
- Placez des pièces pour créer un chemin
- Collectez des objets 
- Les portes sont verrouillées selon la progression 
- Certaines pièces ont des effets garantis (Bedroom +2 pas, Vault +40 or, etc.)
- Gérez vos ressources : gemmes pour placer des pièces rares, clés pour les portes

STRATEGIE DE JEU
-------------
Une bonne stratégie pour atteindre l'Antechamber sans perdre est de maximiser l'espace
dans le manoir et de remplir au plus toutes les salles non découvertes.
Pour avoir de grandes chances de gagner, il est important d'avoir beaucoup d'or
pour acheter des clés dans la pièce "Locksmith" ou dans la cuisine pour restaurer
un peu les pas.


STRUCTURE DU PROJET
-------------------
projet_blue_princeM1/src/blue_prince
├── main.py     
├── controles.py
├── fenetre.py
├── joueur.py
├── objets.py
├── pieces.py
├── rarete.py
├── victoire.py
├── README.txt       
└── data/
    └── (images utilisées pour le jeu)

AUTEURS
------
Thibault Cullet
Taaha Hafeji
Israa Tlili

DATE
----
09/11/2025
