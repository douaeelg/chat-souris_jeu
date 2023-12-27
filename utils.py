import random

def afficher_tableau(chat, souris):
    for i in range(12):
        for j in range(12):
            if i == 0 or i == 11 or j == 0 or j == 11:
                print("# ", end="")
            elif (i-1, j-1) == chat:
                print("C ", end="")
            elif (i-1, j-1) == souris:
                print("S ", end="")
            else:
                print(". ", end="")
        print()

def generer_position_souris():
    return random.randint(1, 10), random.randint(1, 10)

def distance(position1, position2):
    return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])

def deplacer_chat(chat, souris):
    if chat[0] < souris[0]:
        chat = (chat[0] + 1, chat[1])
    elif chat[0] > souris[0]:
        chat = (chat[0] - 1, chat[1])
    elif chat[1] < souris[1]:
        chat = (chat[0], chat[1] + 1)
    elif chat[1] > souris[1]:
        chat = (chat[0], chat[1] - 1)
    return chat