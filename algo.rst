============
 Algorithme
============

Au coeur de notre algo, une fonction élémentaire: pour un point (x,y),
elle cherchera le plus grand carré avec ce point comme sommet haut
gauche.

Un premier algo, brutal, pourra itérer cette recherche sur tous les
points du plateau, avec bien sur un coût important. Il pourra être
utilisé pour les tests fonctionnels, pour tester des implems plus
subtiles.

Un raffinement consistera à profiter de cette recherche pour marquer
des points, situés à l'intérieur du carré trouvé, d'où il est inutile
de lancer de nouvelles recherches. J'ai également l'espoir de chainer
les appels de cette fonction de façon optimale, pour minimiser le
nombre d'appels.

La recherche pourra être incrémentale ou dichotomique, on commencera
par de l'incrémental.

Passer un carré de taille n à n+1, c'est ajouter une bande en bas, une
bande à droite, et un point en diagonale... s'ils sont sans obstacle.
Chercher la bande à droite est optimisable en "couchant" le plateau,
comme on fait pour de la multiplication de matrices: la bande sera
alors une slice, plus facile à extraire.

le ou les carrés trouvés sont stockés sous la forme: ((x,y), taille):
- coordonnées x, y du coin supérieur gauche
- taille du carré.

:date: 2021-02-18

Pas eu le temps de finasser:
- algo "brutal", mais traite des plateaux 500x500 en - de 20s, pas
  idiot.
- tu et tf complets, automatiques.
- pas de mesure du taux de couverture.
- pas de docker.
- seul élément d'optimisation: le plateau couché.
- optimisations possibles:

  - recherche carré dichotomique.
  - au cours de la découverte de carré, marquer les coins (supérieurs
    droits) d'où il est inutile de chercher, car ils ne peuvent pas
    ramener de carré plus grand.
