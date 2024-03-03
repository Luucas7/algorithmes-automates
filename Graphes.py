import re
import copy


# ~~~~~~Utilitaire 
def valeurEstDansIterableEmbriquee(iterable, val):
    for element in iterable:
        if type(element) in (list, tuple, set):
            if valeurEstDansIterableEmbriquee(element, val):
                return True
        else:
            if element == val:
                return True
    return False

def UneMemeOccurence(ite1, ite2):
    #Vérifie si une valeur apparait dans deux itérables    
    isIte1AnIterable = type(ite1) in (list, tuple, set)
    isIte2AnIterable = type(ite2) in (list, tuple, set)
    # Deux itérables
    if isIte1AnIterable and isIte2AnIterable:
        for element in ite1:
            if valeurEstDansIterableEmbriquee(ite2, element):
                return True
        for element in ite2:
            if valeurEstDansIterableEmbriquee(ite1, element):
                return True
        return False
    elif isIte1AnIterable and not isIte2AnIterable:
        return valeurEstDansIterableEmbriquee(ite1, ite2)
    elif not isIte1AnIterable and isIte2AnIterable:
        return valeurEstDansIterableEmbriquee(ite2, ite1)
    #Aucun n'est un itérable
    else:
        return ite1 == ite2

def extraireValeurOuPas(iterateur):
    #Extrait les seules valeurs des itérateurs de longueur 1 au cas ou nécessaire
    if type(iterateur) in (list,tuple,set):
        #On prend la seule valeur présente
        if len(iterateur) == 1:
            return iterateur[0]
        #Sinon on renvoie le paramètre
        else:
            return tuple(iterateur)
    else:
        return iterateur
    
# ~~~~~~1.1 MOTS
def pref(mot):
    return [mot[0:i] for i in range(len(mot) + 1)]


def suf(mot):
    return [mot[i:] for i in range(len(mot) + 1)]


def fact(mot):
    return [''] + [mot[i:j] for i in range(len(mot) + 1) for j in range(i + 1, len(mot) + 1)]


def miroir(mot):
    return mot[::-1]


# ~~~~~~1.2 LANGAGES
def concatene(l1, l2):
    return sorted(list(set([i + j for i in l1 for j in l2])))


def puis(l, n):
    resultat = l
    for i in range(n - 1):
        resultat = [i + j for i in resultat for j in l]
    return sorted(list(set(resultat)))


# ~~~1.2.3
# car cela calculerait à l'infini
#

def tousmots(l, n):
    liste = [""]
    for i in range(n):
        liste += puis(l, i)
    return sorted(list(set(liste)))


# ~~~~~~1.3 AUTOMATES
def defauto():
    print("\n<--->")
    alphabet = input("Entrez les lettres de l'alphabet en les séparant par des virgules :\n\n")
    alphabet = re.sub(r'[\n ]','',alphabet).split(",")
    
    etats = input("Entrez le nombre d'états de l'automate :\n\n")
    etats = int(re.sub(r'[\n ,.]', '', etats))
    etats = list(range(1, etats + 1))

    transitions = []
    nbTransitions = int(input("Entrez le nombre de transitions :\n\n"))
    for i in range(nbTransitions):
        transition = input(
            f"Entrez la transition numéro n°{i} en séparant les états et l'étiquette par des virgules (exemple : 1,a,2) :\n\n")
        transition = re.sub(r'[\n ]', '', transition).split(",")

        transitions.append(transition)

    initiaux = input("Entrez les états initiaux en les séparant par des virgules :\n\n")
    initiaux = re.sub(r'[\n ]', '', initiaux).split(",")

    finaux = input("Entrez les états finaux en les séparant par des virgules :\n\n")
    finaux = re.sub(r'[\n ]', '', finaux).split(",")

    return {
        "alphabet": alphabet,
        "etats": etats,
        "transitions": transitions,
        "I": initiaux,
        "F": finaux
    }


def lirelettre(T, E, a):
    atteignables = []

    for transition in T:
        # Si la transition est de la forme (e1, a, e2) avec e1 dans E et a égal à la lettre a
        if type(E) == int and transition[0] == E and transition[1] == a:
            atteignables.append(transition[2])
        elif type(E) == list and transition[0] in E and transition[1] == a:
            atteignables.append(transition[2])
    return list(set(atteignables))


def liremot(T, E, m):
    if len(m) == 0:
        # Cas d'arrêt : on a fini de lire le mot
        return E
    else:
        # Récursion : on lit la première lettre du mot et on passe à la suite
        debut = m[0]
        fin = m[1:]
        atteints = lirelettre(T, E, debut)
        return liremot(T, atteints, fin)


def accepte(auto, m):
    # si le résultat = [], alors le mot n'est pas accepté
    return len(liremot(auto['transitions'], auto['I'], m)) > 0


def langage_accept(auto, n):
    lst = []
    for mot in (tousmots(auto['alphabet'], n)):
        if accepte(auto, mot):
            lst.append(mot)
    return lst


# ~~~1.3.6
# Les langages peuvent être d'une taille infinie
#

# ~~~~~~~~~~~~ 2 DETERMINISATION

def deterministe(auto):
    doublons = set()
    for i in auto["transitions"]:
        etat_transi = tuple(i[:2])
        # On vérifie si l'état n'a pas déjà d'étiquette
        if etat_transi in doublons:
            return False
        doublons.add(etat_transi)
    return True

def determinise(auto):
    if deterministe(auto):
        return copy.deepcopy(auto)
    newAuto = {
        "alphabet": list(auto["alphabet"]),
        "etats": [auto["I"]],
        "transitions": [],
        "I": [auto["I"]],
        "F": []
    }

    etatsAVisiter = [auto["I"]]

    while len(etatsAVisiter) > 0:
        etatActuel = etatsAVisiter[0]
        etatsAVisiter.remove(etatActuel)

        for lettre in auto["alphabet"]:
            atteints = lirelettre(auto["transitions"], etatActuel, lettre)

            # Aucune étiquette vers un état
            if atteints == []:
                continue

            # Ajout du nouvel état dans le nouvel automate
            if atteints not in newAuto["etats"]:
                newAuto["etats"].append(atteints)
                etatsAVisiter.append(atteints)

                # Si le nouvel état est final
                for etat in auto["F"]:
                    if valeurEstDansIterableEmbriquee(etatsAVisiter, etat) and atteints not in newAuto["F"]:
                        newAuto["F"].append(atteints)

            newAuto["transitions"].append([etatActuel, lettre, atteints])

    return newAuto


def remplacement(liste,map,newAuto):
    for etat in liste:
            if type(etat) in (list,set,tuple):
                oldEtat = extraireValeurOuPas(etat)
            else:
                oldEtat = etat
            newAuto.append(map[oldEtat])

def renommage(auto):
    newAuto = {
        "alphabet": auto["alphabet"],
        "etats": [],
        "transitions": [],
        "I": [],
        "F": []
    }
    OldNameToNew = {}

    # On associe à chaque état un nouveau nom
    for i, etat in enumerate(auto["etats"]):
        oldEtat = extraireValeurOuPas(etat)
        OldNameToNew[oldEtat] = i

    remplacement(auto['etats'],OldNameToNew,newAuto['etats'])
    remplacement(auto['F'],OldNameToNew,newAuto['F'])
    remplacement(auto['I'],OldNameToNew,newAuto['I'])

    for transition in auto["transitions"]:
        transition[0] = extraireValeurOuPas(transition[0])
        transition[1] = extraireValeurOuPas(transition[1])
        transition[2] = extraireValeurOuPas(transition[2])
        newAuto["transitions"].append([OldNameToNew[(transition[0])], transition[1], OldNameToNew[(transition[2])]])

    return newAuto


# ~~~~~~~~~~~~ 3 COMPLEMENTATION

def complet(auto):
    # Cela va vérifier que chaque état possède une transition pour chaque symbole de l'alphabet
    for etat in auto["etats"]:
        for symb in auto["alphabet"]:
            if not any(transition[0] == etat and transition[1] == symb for transition in auto["transitions"]):
                return False
    # Si toutes les transitions sont définies, l'automate est complet
    return True

def complete(auto):
    if complet(auto):
        return copy.deepcopy(auto)

    # Copie de l'automate original
    auto_complet = copy.deepcopy(auto)

    # Ajout de l'état puits
    puits = len(auto_complet['etats'])
    auto_complet['etats'].append(puits)

    # Ajout des transitions manquantes vers l'état puits
    for etat in auto_complet['etats']:
        for symb in auto_complet['alphabet']:
            if not any([transition[1] == symb and transition[0] == etat
                        for transition in auto_complet['transitions']]):
                auto_complet['transitions'].append([etat, symb, puits])

    return auto_complet

def complement(auto):
    auto = renommage((complete(determinise(auto))))  # complétion de l'automate
    etats_finaux = auto["F"]
    etats_non_finaux = [i for i in auto["etats"] if i not in etats_finaux]

    # échange des états finaux et non-finaux
    auto["F"] = etats_non_finaux
    auto["etats"] = etats_non_finaux + etats_finaux

    return auto

# ~~~~~~~~~~~~ 4 AUTOMATES PRODUIT

def inter(auto1, auto2):
    auto1 = determinise(auto1)
    auto2 = determinise(auto2)
    newAuto = produit(auto1,auto2)
    # Tous les états produit avec les deux états finaux
    newAuto['F'] =  [etat for etat in newAuto["etats"] if etat[0] in auto1['F'] and etat[1] in auto2['F']]    
    return newAuto

def difference(auto1, auto2):
    auto1 = complete(determinise(auto1))
    auto2 = complete(determinise(auto2))
    newAuto = produit(auto1,auto2) 
    # Tous les états produit avec l'état 1 final et pas l'état 2
    newAuto['F'] = [etat for etat in newAuto["etats"] if etat[0] in auto1['F'] and etat[1] not in auto2['F']]    
    return newAuto

def produit(auto1, auto2):
    a = extraireValeurOuPas(auto1['I'])
    b = extraireValeurOuPas(auto2['I'])
    newAuto = {
            "alphabet": list(auto1["alphabet"]),
            "etats": [(a, b)],
            "transitions": [],
            "I": [(a, b)]}
    
    etatsActuels = [(a,b)]
    # Tant qu'il y a des états à regarder
    while len(etatsActuels) > 0:
            etat1, etat2 = etatsActuels[0]
            etatsActuels.remove((etat1, etat2))
            for lettre in auto1['alphabet']:
                a = lirelettre(auto1['transitions'], etat1, lettre)
                b = lirelettre(auto2['transitions'], etat2, lettre)

                #Si on va nul part dans un des chemins (automate pas complet)
                if a == [] or b == []:
                    continue

                else:
                    a = extraireValeurOuPas(a)
                    b = extraireValeurOuPas(b)
                    newAuto["transitions"].append([(etat1, etat2), lettre, (a, b)])

                    #On ajoute le nouvel état produit
                    if (a, b) not in newAuto["etats"]:
                        newAuto["etats"].append((a, b))
                        #On regardera récursivement le nouvel état
                        etatsActuels.append((a, b))
    return newAuto

# ~~~~~~~~~~~~ 5 Propriétés de fermeture

def prefixe(auto):
    auto = copy.deepcopy(auto)
    # On accepte tous les préfixes, donc on peut s'arrêter avant
    auto['F'] = auto["etats"]
    return auto

def suffixe(auto):
    auto = copy.deepcopy(auto) 
    # On accepte tous les suffixes, donc on peut commencer de n'importe où
    auto['I'] = auto["etats"]
    return auto

def facteur(auto):
    auto = copy.deepcopy(auto)
    # facteur(auto) = suffixe(auto) + prefixe(auto)
    auto['I'] = auto["etats"]
    auto['F'] = auto["etats"]
    return auto

def miroirAutomate(auto):
    newAuto = copy.deepcopy(auto) 
    #On inverse chaque transition 
    newAuto["transitions"] = [transition[::-1] for transition in auto["transitions"]]
    newAuto['I'] = auto['F']
    newAuto['F'] = auto['I']
    return newAuto

# ~~~~~~~~~~~~ 6 Minimisation

def minimise(auto):
    auto = copy.deepcopy(auto)
    if (not complet(auto)):
        auto = complete(auto)
    if (not deterministe(auto)):
        auto = determinise(auto)
        
    classes = []
    nvClasses = []
    #On crée les classes d'équivalences du début, en séparant les états finaux et non-finaux
    classes.append(auto["F"])
    classes.append([i for i in auto["etats"] if i not in auto["F"]])

    nvClassesFinal = classes

    tableTransitions = {}
    for etat in auto['etats']:
        tableTransitions[etat] = dict()
        for lettre in auto['alphabet']:
            etatVisite = lirelettre(auto['transitions'],etat,lettre)
            etatVisite = extraireValeurOuPas(etatVisite)
            tableTransitions[etat][lettre] = etatVisite
    print(tableTransitions)
    
    while 1:
        for classe in classes:
            #Si une classe a un état
            if len(classe) == 1:
                continue
            #On calcule chaque sous classe d'une classe pour les ajouter après
            nvClasses += sousClassesSuivantes(nvClassesFinal,classe,tableTransitions,auto)
        #Des que l'équivalence est atteinte
        if nvClassesFinal == nvClasses:
            break
        nvClassesFinal = nvClasses
        nvClasses = []
    print(nvClassesFinal)
    return CreerAutomateMinimise(nvClassesFinal,tableTransitions,auto)

def sousClassesSuivantes(classes,classe,transitions,auto):
    newClasses = []
    dejaAjoutes = set()
    for etat in classe:
        #On prend chaque état
        if etat in dejaAjoutes:
            continue
        newSousClasse = [etat]
        #On regarde chaque autre état
        for autreEtat in classe:
            if etat==autreEtat or autreEtat in dejaAjoutes:
                continue
            #Si ils doivent être de la même classe
            if memeSousClasse(classes,etat,autreEtat,transitions,auto):
                newSousClasse.append(autreEtat)
                dejaAjoutes.add(autreEtat)
        newClasses.append(newSousClasse)
        dejaAjoutes.add(etat)
    return newClasses

def memeSousClasse(classes,etat,autreEtat,transitions,auto):
    for lettre in auto["alphabet"]:

        versEtatA = transitions[etat][lettre]
        versEtatB = transitions[autreEtat][lettre]

        #Si il y a des différences de finalité
        if (not( (versEtatA not in auto['F'] and versEtatB not in auto['F']) or (versEtatA in auto['F'] and versEtatB in auto['F']))):
            return False

        #Si il y a des états de différentes classes pour une même lettre lue.
        if ObtenirClasseDepuisEtat(versEtatA,classes) != ObtenirClasseDepuisEtat(versEtatB,classes):
            return False
    return True

def ObtenirClasseDepuisEtat(etat,classes):
    for classe in classes:
        if etat in classe:
            return classe

def CreerAutomateMinimise(nvClassesFinal,tableTransitions,auto):

    newAuto = {
        'I' : [],
        'transitions' : [],
        'alphabet' : auto['alphabet'],
        'F' : [],
        'etats' : nvClassesFinal
    }

    for classe in nvClassesFinal :
        for lettre in auto['alphabet']:
            #On va vers une autre classe en lisant une lettre
            newAuto['transitions'].append([classe,lettre,ObtenirClasseDepuisEtat(tableTransitions[classe[0]][lettre],nvClassesFinal)])
        #On ajoute les états finaux    
        if UneMemeOccurence(classe,auto['F']):
            newAuto['F'].append(classe)
        
        if UneMemeOccurence(classe,auto['I']):
            newAuto['I'].append(classe)
    return newAuto

def main():
    auto = {
        "alphabet": ['a', 'b'],
        "etats": [1, 2, 3, 4],
        "transitions": [[1, 'a', 2], [2, 'a', 2], [2, 'b', 3], [3, 'a', 4]],
        "I": [1], "F": [4]}

    print('\n---------- 1.1 Mots ----------\n')
    print(pref("coucou"))
    print(suf('coucou'))
    print(fact('coucou'))
    print(miroir('coucou'))

    print('\n---------- 1.2 Langages ----------\n')

    L1 = ['aa', 'ab', 'ba', 'bb']
    L2 = ['a', 'b', '']
    print(concatene(L1, L2))

    L1 = ['aa', 'ab', 'ba', 'bb']
    print(puis(L1, 2))

    print(tousmots(['a', 'b'], 3))

    print('\n---------- 1.2 Automates ----------\n')
    print(lirelettre(auto["transitions"], auto["etats"], 'a'))

    print(liremot(auto["transitions"], auto["etats"], 'aba'))

    print(accepte(auto, 'aaba'))

    print(langage_accept(auto, 3))

    auto0 = {"alphabet": ['a', 'b'], "etats": [0, 1, 2, 3],
             "transitions": [[0, 'a', 1], [1, 'a', 1], [1, 'b', 2], [2, 'a', 3]], "I": [0], "F": [3]}
    auto1 = {"alphabet": ['a', 'b'], "etats": [0, 1],
             "transitions": [[0, 'a', 0], [0, 'b', 1], [1, 'b', 1], [1, 'a', 1]], "I": [0], "F": [1]}
    auto2 = {"alphabet": ['a', 'b'], "etats": [0, 1],
             "transitions": [[0, 'a', 0], [0, 'a', 1], [1, 'b', 1], [1, 'a', 1]], "I": [0], "F": [1]}
    print('\n---------- 2 Déterminisation ----------\n')
    print(deterministe(auto0))
    print(renommage(determinise(auto2)))

    auto3 ={"alphabet":['a','b'],"etats": [0,1,2,],
            "transitions":[[0,'a',1],[0,'a',0],[1,'b',2],[1,'b',1]], "I":[0],"F":[2]}
    
    auto4 = {"alphabet": ['a', 'b'], "etats": [0, 1, 2, ],
             "transitions": [[0, 'a', 1], [1, 'b', 2], [2, 'b', 2], [2, 'a', 2]], "I": [0], "F": [2]}
    auto5 = {"alphabet": ['a', 'b'], "etats": [0, 1, 2],
             "transitions": [[0, 'a', 0], [0, 'b', 1], [1, 'a', 1], [1, 'b', 2], [2, 'a', 2], [2, 'b', 0]],
             "I": [0], "F": [0, 1]}

    print('\n---------- 3 Complémentation ----------\n')
    print(complet(auto0))
    print(complet(auto1))
    print(complete(auto0))
    print(complement(auto3))

    print('\n---------- 4 Automate produit ----------\n')
    print(renommage(inter(auto4, auto5)))
    print(renommage(difference(auto4, auto5)))

    print('\n---------- 5 Propriétés de fermeture ----------\n')
    automateFermeture = {"alphabet":['a','b'], "etats":[1,2,3,4,5],
                         "transitions":[[1,'a',1],[1,'a',2],[2,'a',5],[2,'b',3],[3,'b',3],[3,'a',4],[5,'b',5]],
                         "I":[1], "F":[4,5]}

    print(prefixe(automateFermeture))
    print(suffixe(automateFermeture))
    print(facteur(automateFermeture))
    print(miroirAutomate(automateFermeture))

    print('\n---------- 6 Minimisation ----------\n')
    auto6 ={"alphabet":['a','b'],"etats": [0,1,2,3,4,5],
    "transitions":[[0,'a',4],[0,'b',3],[1,'a',5],[1,'b',5],[2,'a',5],[2,'b',2],[3,'a',1],[3,'b',0],
    [4,'a',1],[4,'b',2],[5,'a',2],[5,'b',5]],
    "I":[0],"F":[0,1,2,5]}
    
    print(renommage(minimise(auto6)))

    auto6 ={"alphabet":['a','b'],"etats": [1,2,3,4],
    "transitions":[[1,'a',1],[1,'b',1],[1,'a',2],[2,'a',3],[3,'a',4],[4,'b',4],[4,'a',4]],
    "I":[1,3],"F":[2,4]}

    print(determinise(auto6))
    
    autoa ={"alphabet":['a','b'],"etats": [0,1,2],
    "transitions":[[0,'a',1],[1,'a',2],[2,'a',0]],
    "I":[0],"F":[0]}

    autob ={"alphabet":['a','b'],"etats": [3,4],
    "transitions":[[3,'a',4],[4,'a',3]],
    "I":[3],"F":[4]}

    print((difference(autoa,autob)))



if __name__ == '__main__':
    main()