===============
 Test Bon coin
===============

:date: 2021-02-17

Réponse au test qui m'a été soumis ce jour.

specs contient le document de spécif initial, et les "recommandations".
scripts contient les scripts de traitement:

- map_gen.py, le générateur de fichiers d'entrée.
- find_square, le script solution

Le test est d'une difficulté conséquente, je choisis de fournir la
réponse la plus simple possible, en particulier:

- rester au niveau pur python: pas de web service, pas de dockerfile,
  pas de github action. 
- Les optimisations possibles sont suggérées (cf docstrings), pas
  implémentées: une première implem avec un bon taux de couverture,
  qu'il faudrait logiquement faire suivre pas une passe
  d'optimisation.

J'ai fini par implémenter:

- un docker: mais j'ai voulu conserver un interface CLI, et comment
  envoyer un fichier via ssh à une appli dockerisée? Pour que ça reste
  une appli simple:

  - transmettre le fichier en pipe.
  - accepter l'argument "-", signifiant "lis le contenu sur stdin.

- un test via github actions: le test ignore le docker, et invoque
  directement pytest, enchainant tu et tf (peu orthodoxe)

Le docker est testé grossièrement, localement, par ``tests/ti/sample_test``


:note: Un test fonctionnel plus complet serait possible, qui lance
       l'algo non pas sur des plateaux générés aléatoirement, mais
       avec des obstacles permettant de connaitre, par raisonnement,
       la bonne réponse, et de vérifier cette réponse.

