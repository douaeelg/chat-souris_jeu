import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Paramètres du jeu
largeur_fenetre = 800
hauteur_fenetre = 800
taille_case = 80

# Assurez-vous que la taille de la case est un multiple de la hauteur de la fenêtre
assert hauteur_fenetre % taille_case == 0, "La taille de la case doit être un multiple de la hauteur de la fenêtre"

# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)
rouge = (255, 0, 0)
vert = (0, 255, 0)

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre + 100))  # Hauteur supplémentaire pour les boutons
pygame.display.set_caption("Chat et Souris")

# Chargement des images et redimensionnement
image_chat = pygame.image.load("cat.png")
image_souris = pygame.image.load("mouse.png")
image_chat = pygame.transform.scale(image_chat, (taille_case, taille_case))
image_souris = pygame.transform.scale(image_souris, (taille_case, taille_case))

# Fonction pour afficher le tableau avec les boutons
def afficher_tableau(chat, souris, message_erreur=None, nombre_de_pas=None):
    fenetre.fill(blanc)

    for i in range(hauteur_fenetre // taille_case):
        for j in range(largeur_fenetre // taille_case):
            if i == 0 or i == hauteur_fenetre // taille_case - 1 or j == 0 or j == largeur_fenetre // taille_case - 1:
                pygame.draw.rect(fenetre, noir, (j * taille_case, i * taille_case, taille_case, taille_case))
            elif (i - 1, j - 1) == chat:
                fenetre.blit(image_chat, (j * taille_case, i * taille_case))
            elif (i - 1, j - 1) == souris:
                fenetre.blit(image_souris, (j * taille_case, i * taille_case))
            else:
                pygame.draw.rect(fenetre, blanc, (j * taille_case, i * taille_case, taille_case, taille_case), 1)

    if message_erreur:
        police = pygame.font.Font(None, 36)
        texte_erreur = police.render(message_erreur, True, rouge)
        fenetre.blit(texte_erreur, (largeur_fenetre // 4, hauteur_fenetre // 20))  # Ajuster la position du message

    # Afficher le message "Tu as attrapé la souris en (nombre) de pas" en bas de la fenêtre en vert
    if nombre_de_pas is not None:
        police_message = pygame.font.Font(None, 36)
        message = f"Tu as attrapé la souris en {nombre_de_pas} pas!"
        texte_message = police_message.render(message, True, vert)
        fenetre.blit(texte_message, (largeur_fenetre // 4, hauteur_fenetre + 60))  # Ajuster la position du message

    # Ajout des boutons
    pygame.draw.rect(fenetre, noir, (0, hauteur_fenetre, largeur_fenetre // 2, 100))  # Bouton Réinitialiser
    pygame.draw.rect(fenetre, noir, (largeur_fenetre // 2, hauteur_fenetre, largeur_fenetre // 2, 100))  # Bouton Fermer

    police_bouton = pygame.font.Font(None, 36)
    texte_reset = police_bouton.render("Réinitialiser", True, blanc)
    texte_close = police_bouton.render("Fermer", True, blanc)

    fenetre.blit(texte_reset, (largeur_fenetre // 8, hauteur_fenetre + 20))
    fenetre.blit(texte_close, (largeur_fenetre * 5 // 8, hauteur_fenetre + 20))

    pygame.display.flip()

# Position initiale du chat
position_chat = ((hauteur_fenetre // taille_case) - 3, 1)

# Génération aléatoire de la position initiale de la souris à l'intérieur du tableau
position_souris = (random.randint(1, (hauteur_fenetre // taille_case) - 3), random.randint(1, (largeur_fenetre // taille_case) - 3))

# Gestion du temps pour le message d'erreur
temps_message_erreur = 0

# Initialisation des variables
nombre_de_pas = 0
souris_attrapee = False

# Boucle principale du jeu
clock = pygame.time.Clock()
max_pas = 25
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if position_chat[0] > 0:  # Vérifier que la coordonnée y est positive
                    position_chat = (position_chat[0] - 1, position_chat[1])
                else:
                    temps_message_erreur = pygame.time.get_ticks() + 10000  # Afficher le message pendant 10 secondes
            elif event.key == pygame.K_DOWN:
                if position_chat[0] < (hauteur_fenetre // taille_case) - 3:  # Ajuster la limite inférieure
                    position_chat = (position_chat[0] + 1, position_chat[1])
                else:
                    temps_message_erreur = pygame.time.get_ticks() + 10000
            elif event.key == pygame.K_LEFT:
                if position_chat[1] > 0:  # Vérifier que la coordonnée x est positive
                    position_chat = (position_chat[0], position_chat[1] - 1)
                else:
                    temps_message_erreur = pygame.time.get_ticks() + 10000
            elif event.key == pygame.K_RIGHT:
                if position_chat[1] < (largeur_fenetre // taille_case) - 3:  # Ajuster la limite de droite
                    position_chat = (position_chat[0], position_chat[1] + 1)
                else:
                    temps_message_erreur = pygame.time.get_ticks() + 10000
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if y > hauteur_fenetre and y < hauteur_fenetre + 100:
                if x < largeur_fenetre // 2:
                    # Clic sur le bouton Réinitialiser
                    position_chat = ((hauteur_fenetre // taille_case) - 3, 1)
                    position_souris = (random.randint(1, (hauteur_fenetre // taille_case) - 3), random.randint(1, (largeur_fenetre // taille_case) - 3))
                    temps_message_erreur = 0  # Réinitialiser le message d'erreur
                    nombre_de_pas = 0  # Réinitialiser le nombre de pas
                    souris_attrapee = False  # Réinitialiser l'indicateur de souris attrapée
                else:
                    # Clic sur le bouton Fermer
                    running = False

    # Vérifier si le chat a atteint la souris
    if position_chat == position_souris:
        print("Le chat a attrapé la souris!")
        souris_attrapee = True  # Mettre à jour l'indicateur de souris attrapée

    # Incrémenter le nombre de pas à chaque itération de la boucle
    nombre_de_pas += 1

    # Afficher le tableau avec le message d'erreur si le temps n'est pas écoulé
    if temps_message_erreur > pygame.time.get_ticks():
        afficher_tableau(position_chat, position_souris, "Zone inaccessible!")

    # Sinon, afficher le tableau normalement
    else:
        afficher_tableau(position_chat, position_souris, nombre_de_pas=nombre_de_pas)

    pygame.time.delay(500)
    clock.tick(2)

    # Vérifier si la souris a été attrapée et afficher le message approprié
    if souris_attrapee:
        afficher_tableau(position_chat, position_souris, nombre_de_pas=nombre_de_pas)

# Fermer Pygame
pygame.quit()
sys.exit()
