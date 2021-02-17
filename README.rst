===============
 Test Bon coin
===============

:date: 2021-02-17

Tentative de réponse au test qui m'a été soumis ce jour.
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
