# Exercices Corrigés - Plus Courts Chemins

Voici les corrections pour la série d'exercices sur les plus courts chemins.

## Exercice 1 : Dijkstra et Cycles Négatifs

**Question :** Dans un graphe pondéré, en présence de cycles négatifs, exhibez un exemple où l'algorithme de Dijkstra ne trouve pas le plus court chemin.

**Réponse :**
L'algorithme de Dijkstra suppose que lorsqu'on "valide" un sommet (qu'on le sort de la file d'attente), on a définitivement trouvé son plus court chemin. Cette hypothèse est fausse si des arêtes ont des poids négatifs, et encore plus s'il y a des cycles négatifs.

**Exemple d'exécution (Graphe sans poids négatifs) :**
<video controls width="100%" autoplay loop muted>
  <source src="../img/dijkstra.webm" type="video/webm">
  <source src="../img/dijkstra.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

**Exemple simple (Arête négative) :**
*   Sommets : A, B, C
*   Arêtes :
    *   A -> B (coût 2)
    *   A -> C (coût 5)
    *   B -> C (coût -10)

**Déroulement de Dijkstra (partant de A) :**
1.  On visite A. Voisins : B (2), C (5).
2.  Le plus proche est B (2). On valide B.
3.  On regarde les voisins de B : C est accessible avec un coût total de 2 + (-10) = -8.
    *   *Problème* : Si Dijkstra a déjà validé C (dans un graphe plus complexe) ou s'il ne met pas à jour correctement les priorités, il échoue.
    *   Mais le vrai problème des **cycles négatifs** est que le chemin peut devenir infiniment petit (ex: A -> B -> A avec coût total -1). Dijkstra ne détecte pas cela et peut tourner en boucle ou donner un résultat faux.

---

## Exercice 2 : Produit des poids

**Question :** On veut trouver le chemin qui minimise le **produit** des poids (tous >= 1). Comment faire ?

**Réponse :**
On utilise les **logarithmes**.
On sait que : log(a * b) = log(a) + log(b).
Minimiser un produit revient à minimiser la somme des logarithmes.

**Algorithme :**
1.  Transformer le graphe : remplacer chaque poids w par son logarithme : w' = log(w).
2.  Comme w >= 1, alors log(w) >= 0. Tous les nouveaux poids sont positifs.
3.  Appliquer l'algorithme de **Dijkstra** classique sur ce nouveau graphe.
4.  Le chemin trouvé sera celui qui minimise la somme des log, et donc le produit des poids initiaux.

---

## Exercice 3 : Chemin le plus fiable (Probabilités)

**Question :** Les poids sont des probabilités (entre 0 et 1). On veut maximiser la probabilité d'arrivée (produit des probabilités sur le chemin).

**Réponse :**
C'est similaire à l'exercice précédent, mais on veut **maximiser** un produit de nombres entre 0 et 1.
On sait que log(p) est négatif (car p <= 1).
Pour se ramener à un problème de plus court chemin (minimisation de somme positive), on utilise : **-log(p)**.

**Algorithme :**
1.  Transformer le graphe : remplacer chaque probabilité p par w' = -log(p).
2.  Comme p <= 1, log(p) <= 0, donc -log(p) >= 0. Les nouveaux poids sont positifs.
3.  Chercher le chemin qui **minimise** la somme des w' (ce qui revient à maximiser le produit des p).
4.  Utiliser **Dijkstra**.

---

## Exercice 4 : Plus long chemin et cycles négatifs

**Question :** Montrez que si nous savons résoudre le problème du plus court chemin en présence de cycle de longueur négative, alors nous savons résoudre le problème du plus long chemin.

**Réponse :**
Le problème du "Plus Long Chemin" dans un graphe G est équivalent au problème du "Plus Court Chemin" dans un graphe G' où tous les poids sont inversés (multipliés par -1).

**Réduction :**
1.  Construire G' identique à G, mais pour chaque arête de poids w, on lui donne le poids -w.
2.  Chercher le plus court chemin dans G'.
    *   Si on trouve un chemin de longueur L dans G', cela correspond à un chemin de longueur -L dans G.
    *   Minimiser (-L) revient à Maximiser L.
3.  **Attention** : Si G a des cycles positifs, G' aura des cycles négatifs.
    *   C'est pourquoi on a besoin d'un algorithme capable de gérer les cycles négatifs (comme supposé dans l'énoncé).

---

## Exercice 5 : Complexité de Dijkstra

**Question :** Est-ce que l'algorithme de Dijkstra (avec tas de Fibonacci) peut s'exécuter en temps inférieur à o(m + n log n) ?

**Réponse : Non (dans le cas général).**
La complexité O(m + n log n) est considérée comme optimale pour les algorithmes basés sur la comparaison dans des graphes généraux.
*   Le terme "n log n" vient de la nécessité de trier les sommets par distance (similaire au tri d'une liste).
*   On sait que trier n éléments par comparaison prend au minimum O(n log n).
*   Si on pouvait faire Dijkstra beaucoup plus vite, on pourrait l'utiliser pour trier des nombres plus vite que la limite théorique, ce qui est impossible (avec des comparaisons uniquement).
