"""
            SAE1.02 PACMAN IUT'O
         BUT1 Informatique 2023-2024

        Module plateau.py
        Ce module contient l'implémentation de la structure de données
        qui gère le plateau jeu aussi qu'un certain nombre de fonctions
        permettant d'observer le plateau et d'aider l'IA à prendre des décisions
"""
import const
import case
import random



def get_nb_lignes(plateau):
    """retourne le nombre de lignes du plateau

    Args:
        plateau (dict): le plateau considéré

    Returns:
        int: le nombre de lignes du plateau
    """
    return plateau['nb_lignes']


def get_nb_colonnes(plateau):
    """retourne le nombre de colonnes du plateau

    Args:
        plateau (dict): le plateau considéré

    Returns:
        int: le nombre de colonnes du plateau
    """
    return plateau['nb_colonnes']


def pos_ouest(plateau, pos):
    """retourne la position de la case à l'ouest de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    west_pos = pos[1] - 1
    if west_pos < 0:
        west_pos = get_nb_colonnes(plateau) - 1
        
    return pos[0], west_pos


def pos_est(plateau, pos):
    """retourne la position de la case à l'est de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    east_pos = pos[1] + 1
    if east_pos >= get_nb_colonnes(plateau):
        east_pos = 0

    return pos[0], east_pos

def pos_nord(plateau, pos):
    """retourne la position de la case au nord de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    north_pos = pos[0] - 1
    if north_pos < 0:
        north_pos = get_nb_lignes(plateau) - 1

    return north_pos, pos[1]


def pos_sud(plateau, pos):
    """retourne la position de la case au sud de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    south_pos = pos[0] + 1
    if south_pos >= get_nb_lignes(plateau):
        south_pos = 0

    return south_pos, pos[1]


def pos_arrivee(plateau,pos,direction):
    """ calcule la position d'arrivée si on part de pos et qu'on va dans
    la direction indiquée en tenant compte que le plateau est un tore
    si la direction n'existe pas la fonction retourne None
    Args:
        plateau (dict): Le plateau considéré
        pos (tuple): une paire d'entiers qui donne la position de départ
        direction (str): un des caractère NSEO donnant la direction du déplacement

    Returns:
        None|tuple: None ou une paire d'entiers indiquant la position d'arrivée
    """
    next_pos = None
    if direction == 'O':
        next_pos = pos_ouest(plateau, pos)
    elif direction == 'E':
        next_pos = pos_est(plateau, pos)
    elif direction == 'N':
        next_pos = pos_nord(plateau, pos)
    elif direction == 'S':
        next_pos = pos_sud(plateau, pos)

    return next_pos

def get_case(plateau, pos):
    """retourne la case qui se trouve à la position pos du plateau

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        dict: La case qui se situe à la position pos du plateau
    """
    return plateau['cases'][pos[0]][pos[1]]


def get_objet(plateau, pos):
    """retourne l'objet qui se trouve à la position pos du plateau

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        str: le caractère symbolisant l'objet
    """
    return case.get_objet(get_case(plateau, pos))


def poser_pacman(plateau, pacman, pos):
    """pose un pacman en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        pacman (str): la lettre représentant le pacman
        pos (tuple): une paire (lig,col) de deux int
    """
    case.poser_pacman(get_case(plateau, pos), pacman)


def poser_fantome(plateau, fantome, pos):
    """pose un fantome en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        fantome (str): la lettre représentant le fantome
        pos (tuple): une paire (lig,col) de deux int
    """
    case.poser_fantome(get_case(plateau, pos), fantome)


def poser_objet(plateau, objet, pos):
    """Pose un objet en position pos sur le plateau. Si cette case contenait déjà
        un objet ce dernier disparait

    Args:
        plateau (dict): le plateau considéré
        objet (int): un entier représentant l'objet. const.AUCUN indique aucun objet
        pos (tuple): une paire (lig,col) de deux int
    """
    plateau['cases'][pos[0]][pos[1]] = objet


def Plateau(plan):
    """Créer un plateau en respectant le plan donné en paramètre.
        Le plan est une chaine de caractères contenant
            '#' (mur)
            ' ' (couloir non peint)
            une lettre majuscule (un couloir peint par le joueur représenté par la lettre)

    Args:
        plan (str): le plan sous la forme d'une chaine de caractères

    Returns:
        dict: Le plateau correspondant au plan
    """
    tp = plan.split('\n')
    for i in range(len(tp)):
        if ';' in tp[i]:
            tp[i] = tp[i].split(';')
    tp = tuple(tp)

    def positions(nb_entite, ind_entite):
        dico = {}
        for i in range(ind_entite, ind_entite + nb_entite, 1):
            dico[tp[i][0]] = int(tp[i][1]), int(tp[i][2])
        
        return dico
    
    nb_lignes, nb_colonnes = int(tp[0][0]), int(tp[0][1])
    nb_joueurs = int(tp[nb_lignes + 1])
    nb_fantomes = int(tp[nb_lignes + nb_joueurs + 2])
    joueurs = positions(nb_joueurs, nb_lignes + 2)
    fantomes = positions(nb_fantomes, nb_lignes + nb_joueurs + 3)
    cases = []

    for y in range(nb_lignes):
        cases.append([])

        for elem in tp[y + 1]:
            if elem == const.AUCUN:
                cases[y].append(case.Case())

            elif elem in const.LES_OBJETS:
                cases[y].append(case.Case(objet=elem))

            else:
                cases[y].append(case.Case(mur=True))

    res = {'nb_lignes': nb_lignes,
            'nb_colonnes': nb_colonnes,
            'nb_joueurs': nb_joueurs,
            'nb_fantomes': nb_fantomes,
            'cases': cases,
            'joueurs': joueurs,
            'fantomes': fantomes}

    for pacman in joueurs:
        poser_pacman(res, pacman, joueurs[pacman])

    for fantom in fantomes:
        poser_fantome(res, fantom, fantomes[fantom])

    return res


def set_case(plateau, pos, une_case):
    """remplace la case qui se trouve en position pos du plateau par une_case

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int
        une_case (dict): la nouvelle case
    """
    plateau['cases'][pos[0]][pos[1]] = une_case


def enlever_pacman(plateau, pacman, pos):
    """enlève un joueur qui se trouve en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        pacman (str): la lettre représentant le joueur
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        bool: True si l'opération s'est bien déroulée, False sinon
    """
    return case.prendre_pacman(get_case(plateau, pos), pacman)


def enlever_fantome(plateau, fantome, pos):
    """enlève un fantome qui se trouve en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        fantome (str): la lettre représentant le fantome
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        bool: True si l'opération s'est bien déroulée, False sinon
    """
    return case.prendre_fantome(get_case(plateau, pos), fantome)


def prendre_objet(plateau, pos):
    """Prend l'objet qui se trouve en position pos du plateau et retourne l'entier
        représentant cet objet. const.AUCUN indique qu'aucun objet se trouve sur case

    Args:
        plateau (dict): Le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        int: l'entier représentant l'objet qui se trouvait sur la case.
        const.AUCUN indique aucun objet
    """
    return case.prendre_objet(get_case(plateau, pos))

        
def deplacer_pacman(plateau, pacman, pos, direction, passemuraille=False):
    """Déplace dans la direction indiquée un joueur se trouvant en position pos
        sur le plateau si c'est possible

    Args:
        plateau (dict): Le plateau considéré
        pacman (str): La lettre identifiant le pacman à déplacer
        pos (tuple): une paire (lig,col) d'int
        direction (str): une lettre parmie NSEO indiquant la direction du déplacement
        passemuraille (bool): un booléen indiquant si le pacman est passemuraille ou non

    Returns:
        (int,int): une paire (lig,col) indiquant la position d'arrivée du pacman 
                   (None si le pacman n'a pas pu se déplacer)
    """
    next_pos = pos_arrivee(plateau, pos, direction)

    if passemuraille or not case.est_mur(get_case(plateau, next_pos)):
        enlever_pacman(plateau, pacman, pos)
        poser_pacman(plateau, pacman, next_pos)
        plateau['joueurs'][pacman] = next_pos
        return next_pos


def deplacer_fantome(plateau, fantome, pos, direction):
    """Déplace dans la direction indiquée un fantome se trouvant en position pos
        sur le plateau

    Args:
        plateau (dict): Le plateau considéré
        fantome (str): La lettre identifiant le fantome à déplacer
        pos (tuple): une paire (lig,col) d'int
        direction (str): une lettre parmie NSEO indiquant la direction du déplacement

    Returns:
        (int,int): une paire (lig,col) indiquant la position d'arrivée du fantome
                   None si le joueur n'a pas pu se déplacer
    """
    next_pos = pos_arrivee(plateau, pos, direction)

    if not case.est_mur(get_case(plateau, next_pos)):
        enlever_fantome(plateau, fantome, pos)
        poser_fantome(plateau, fantome, next_pos)
        plateau['fantomes'][fantome] = next_pos
        return next_pos

def case_vide(plateau):
    """choisi aléatoirement sur le plateau une case qui n'est pas un mur et qui
       ne contient ni pacman ni fantome ni objet

    Args:
        plateau (dict): le plateau

    Returns:
        (int,int): la position choisie
    """
    pass


def directions_possibles(plateau,pos,passemuraille=False):
    """ retourne les directions vers où il est possible de se déplacer à partir
        de la position pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): un couple d'entiers (ligne,colonne) indiquant la position de départ
        passemuraille (bool): indique si on s'autorise à passer au travers des murs
    
    Returns:
        str: une chaine de caractères indiquant les directions possibles
              à partir de pos
    """
    pass
#---------------------------------------------------------#


def analyse_plateau(plateau, pos, direction, distance_max):
    """calcul les distances entre la position pos, les différents objets et
        joueurs du plateau si on commence par partir dans la direction indiquée
        en se limitant à la distance max. Si il n'est pas possible d'aller dans la
        direction indiquée à partir de pos, la fonction doit retourner None

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers indiquant la postion de calcul des distances
        distance_max (int): un entier indiquant la distance limite de la recherche
    Returns:
        dict: un dictionnaire de listes. 
                Les clés du dictionnaire sont 'objets', 'pacmans' et 'fantomes'
                Les valeurs du dictionnaire sont des listes de paires de la forme
                    (dist,ident) où dist est la distance de l'objet, du pacman ou du fantome
                                    et ident est l'identifiant de l'objet, du pacman ou du fantome
            S'il n'est pas possible d'aller dans la direction indiquée à partir de pos
            la fonction retourne None
    """ 
    res = {}
    cpt = 0
    if distance_max<=0:
        return None
    while cpt != distance_max:
        if direction is 'N':
            pos = pos_nord(plateau,pos)
            if get_objet(plateau,pos) != None:
                res['objets']=[pos,get_objet(plateau,pos)]
            if get_case(plateau,pos)['pacmans_presents'] != None:
                res['pacmans']=[pos,get_case(plateau,pos)['pacmans_presents']]
            if get_case(plateau,pos)['fantomes_presents'] != None:
                res['fantomes']=[pos,get_case(plateau,pos)['fantomes_presents']]
        elif direction is 'S':
            pos = pos_sud(plateau,pos)
            if get_objet(plateau,pos) != None:
                res['objets']=[pos,get_objet(plateau,pos)]
            if get_case(plateau,pos)['pacmans_presents'] != None:
                res['pacmans']=[pos,get_case(plateau,pos)['pacmans_presents']]
            if get_case(plateau,pos)['fantomes_presents'] != None:
                res['fantomes']=[pos,get_case(plateau,pos)['fantomes_presents']]
        elif direction is 'E':
            pos = pos_est(plateau,pos)
            if get_objet(plateau,pos) != None:
                res['objets']=[pos,get_objet(plateau,pos)]
            if get_case(plateau,pos)['pacmans_presents'] != None:
                res['pacmans']=[pos,get_case(plateau,pos)['pacmans_presents']]
            if get_case(plateau,pos)['fantomes_presents'] != None:
                res['fantomes']=[pos,get_case(plateau,pos)['fantomes_presents']]
        elif direction is 'O':
            pos = pos_ouest(plateau,pos)
            if get_objet(plateau,pos) != None:
                res['objets']=[pos,get_objet(plateau,pos)]
            if get_case(plateau,pos)['pacmans_presents'] != None:
                res['pacmans']=[pos,get_case(plateau,pos)['pacmans_presents']]
            if get_case(plateau,pos)['fantomes_presents'] != None:
                res['fantomes']=[pos,get_case(plateau,pos)['fantomes_presents']]
        cpt += 1
    return res

def prochaine_intersection(plateau,pos,direction):
    """calcule la distance de la prochaine intersection
        si on s'engage dans la direction indiquée

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position de départ
        direction (str): la direction choisie

    Returns:
        int: un entier indiquant la distance à la prochaine intersection
             -1 si la direction mène à un cul de sac.
    """
    deplacement = True
    cpt = -1
    while deplacement:
        for direct in directions_possibles(plateau,pos,passemuraille=False):
            if direct == direction:
                if direction is 'N':
                    pos = pos_nord(plateau,pos)
                    cpt+=1
                elif direction is 'S':
                    pos = pos_sud(plateau,pos)
                    cpt+=1
                elif direction is 'E':
                    pos = pos_est(plateau,pos)
                    cpt+=1
                elif direction is 'O':
                    pos = pos_ouest(plateau,pos)
                    cpt+=1
        if direction not in directions_possibles(plateau,pos,passemuraille=False):
            deplacement = False
    return cpt
# A NE PAS DEMANDER
def plateau_2_str(plateau):
        res = str(get_nb_lignes(plateau))+";"+str(get_nb_colonnes(plateau))+"\n"
        pacmans = []
        fantomes = []
        for lig in range(get_nb_lignes(plateau)):
            ligne = ""
            for col in range(get_nb_colonnes(plateau)):
                la_case = get_case(plateau,(lig, col))
                if case.est_mur(la_case):
                    ligne += "#"
                    les_pacmans = case.get_pacmans(la_case)
                    for pac in les_pacmans:
                        pacmans.append((pac, lig, col))
                else:
                    obj = case.get_objet(la_case)
                    les_pacmans = case.get_pacmans(la_case)
                    les_fantomes= case.get_fantomes(la_case)
                    ligne += str(obj)
                    for pac in les_pacmans:
                        pacmans.append((pac, lig, col))
                    for fantome in les_fantomes:
                        fantomes.append((fantome,lig,col))
            res += ligne+"\n"
        res += str(len(pacmans))+'\n'
        for pac, lig, col in pacmans:
            res += str(pac)+";"+str(lig)+";"+str(col)+"\n"
        res += str(len(fantomes))+"\n"
        for fantome, lig, col in fantomes:
            res += str(fantome)+";"+str(lig)+";"+str(col)+"\n"
        return res
