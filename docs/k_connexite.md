# Exercices Corrigés - k-Connexité

Voici les corrections pour la série d'exercices sur la k-connexité.

## Exercice 1 : Chemins disjoints entre ensembles

**Question :** Soit G un graphe k-connexe, et soient X et Y deux sous-ensembles de sommets de taille k. Montrez que G possède k chemins disjoints reliant X à Y.

**Preuve :**
On utilise le **Théorème de Menger**.
Imaginez qu'on ajoute deux nouveaux sommets fictifs au graphe :
*   Une "super-source" S reliée à tous les sommets de X.
*   Un "super-puits" T relié à tous les sommets de Y.

Puisque le graphe original est k-connexe, il faut supprimer au moins k sommets pour le déconnecter.
Cela implique qu'il est impossible de séparer S de T en supprimant moins de k sommets (car X et Y sont de taille k et sont "solidement" attachés au reste du graphe).
D'après le théorème de Menger, le nombre minimum de sommets à supprimer pour couper le chemin entre S et T est égal au nombre maximum de chemins disjoints entre S et T.
Donc, il existe k chemins disjoints entre S et T. En retirant S et T, on obtient k chemins disjoints entre X et Y.

---

## Exercice 2 : 2-connexité et Degré minimum

**1. Un graphe G est 2-connexe si et seulement si il existe deux arbres couvrants disjoints.**

**Réponse : FAUX.**
Contre-exemple : Un cycle simple avec n sommets (C_n).
*   C'est un graphe 2-connexe (il faut couper 2 sommets pour le séparer).
*   Il possède n arêtes.
*   Un arbre couvrant a besoin de n-1 arêtes.
*   Deux arbres couvrants disjoints auraient besoin de 2(n-1) arêtes.
*   Pour n > 2, on a 2n - 2 > n. Il n'y a pas assez d'arêtes dans le cycle pour faire deux arbres.

**2. Si G est k-connexe alors le degré minimum delta(G) >= k.**

**Réponse : VRAI.**
Supposons qu'il existe un sommet v avec un degré strictement inférieur à k (par exemple k-1 voisins).
Si on supprime ces k-1 voisins, le sommet v se retrouve totalement isolé du reste du graphe.
On a donc réussi à déconnecter le graphe en supprimant moins de k sommets (k-1).
Cela contredit le fait que le graphe est k-connexe.
Donc, tous les sommets doivent avoir au moins k voisins.

---

## Exercice 3 : k-arête-connexe vs k-connexe

**Définitions :**
*   **k-connexe** : Il faut supprimer au moins k sommets pour déconnecter le graphe.
*   **k-arête-connexe** : Il faut supprimer au moins k arêtes pour déconnecter le graphe.

**1. Si G est k-arête-connexe, est-ce qu'il est k-connexe ?**

**Réponse : NON.**
Il est généralement plus facile de casser un graphe en supprimant des sommets (qui emportent toutes leurs arêtes avec eux) qu'en supprimant des arêtes une par une.
Exemple du "Nœud Papillon" (deux triangles reliés par un seul sommet central).
*   Si on supprime le sommet central, le graphe est coupé. Il n'est donc pas 2-connexe (1-connexe seulement).
*   Pourtant, pour le couper en supprimant des arêtes, il faut en enlever au moins 2. Il est donc 2-arête-connexe.
La connexité par arêtes ne garantit pas la connexité par sommets.

**2. Réciproque : Si G est k-connexe, est-il k-arête-connexe ?**

**Réponse : OUI.**
La connexité par sommets est une propriété plus forte.
On a l'inégalité classique : (connexité sommets) <= (connexité arêtes) <= (degré minimum).
Si la connexité sommets est k, alors la connexité arêtes est au moins k.

---

## Exercice 4 : Cycle passant par x et y

**Question :** Soit G un graphe 2-connexe. Montrez que pour toute paire de sommets x, y il existe un cycle qui les contient.

**Preuve :**
Puisque G est 2-connexe, d'après le théorème de Menger, il existe au moins **2 chemins disjoints** (qui ne partagent aucun sommet à part le début et la fin) entre x et y.
Appelons ces chemins P1 et P2.
*   P1 va de x à y.
*   P2 va de x à y (par un autre chemin).
Si on part de x, qu'on suit P1 jusqu'à y, et qu'on revient à x par P2 (en sens inverse), on forme une boucle fermée sans croisement.
Cette boucle est un cycle qui contient x et y.

---

## Exercice 5 : Chemins arcs-disjoints et Flot Maximum

**Question :** Modéliser la recherche du nombre maximum de chemins arcs-disjoints entre x et y comme un problème de flot.

**Modélisation :**
1.  Prendre le graphe orienté D.
2.  Assigner une **capacité de 1** à chaque arc.
3.  Considérer x comme la Source et y comme le Puits.
4.  Calculer le **Flot Maximum** de x à y.

**Justification :**
Comme chaque arc a une capacité de 1, le flot ne peut passer qu'une seule fois par chaque arc.
La valeur du flot maximum correspondra donc exactement au nombre de chemins que l'on peut emprunter simultanément sans réutiliser les mêmes arcs.

---

## Exercice 6 : Chemins sommets-disjoints et Flots

**Question :** Même question mais pour les chemins sommets-disjoints (qui ne partagent aucun sommet).

**Modélisation :**
Le problème est que le flot standard limite les arêtes, pas les sommets. Il faut transformer le graphe pour limiter le passage par les sommets.
**Technique du "Dédoublement de Sommets" (Vertex Splitting) :**
1.  Pour chaque sommet v du graphe, on le remplace par deux sommets : v_entrée et v_sortie.
2.  On ajoute un arc (v_entrée -> v_sortie) avec une **capacité de 1**. (C'est cet arc qui limite le passage par le sommet à 1 seule fois).
3.  Pour chaque arc original (u -> v), on crée un arc (u_sortie -> v_entrée) avec capacité infinie (ou 1).
4.  Calculer le Flot Max entre x_sortie et y_entrée.

**Application au graphe non orienté :**
Pour un graphe non orienté, on remplace d'abord chaque arête non orientée {u, v} par deux arcs orientés (u -> v) et (v -> u).
Ensuite, on applique la même technique de dédoublement de sommets décrite ci-dessus.
Cela permet de trouver le nombre maximum de chemins indépendants entre deux points, ce qui est très utile pour mesurer la robustesse d'un réseau.
