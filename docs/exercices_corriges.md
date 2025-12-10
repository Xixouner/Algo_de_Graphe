# Exercices Corrigés - Arbres Couvrants

Voici les corrections détaillées pour les exercices demandés.

## Exercice 2 : Borne supérieure sur le nombre d'arbres couvrants

**Question :** Donnez une borne supérieure sur le nombre d'arbres couvrants qu'un graphe à n sommets peut avoir.

**Réponse :**
La borne supérieure est donnée par la **formule de Cayley**.
Pour un graphe complet K_n (où toutes les paires de sommets sont reliées), le nombre d'arbres couvrants est exactement :
**n puissance (n-2)**

Puisque tout graphe à n sommets est un sous-graphe du graphe complet K_n, il ne peut pas avoir plus d'arbres couvrants que K_n.
Donc, le nombre d'arbres couvrants est au maximum n^(n-2).

---

## Exercice 3 : Poids négatifs et Maximum

**1. Si les valuations des arêtes sont toutes négatives. Est-ce que le problème est plus difficile que le cas où les arêtes sont de poids positifs ?**

**Réponse : Non.**
Les algorithmes de Kruskal et Prim fonctionnent par **comparaison** de poids (trouver le minimum, trier).
*   Si on ajoute une constante C à toutes les arêtes pour les rendre positives, l'ordre des arêtes ne change pas (si w1 < w2, alors w1 + C < w2 + C).
*   L'arbre qui minimise la somme des poids reste le même.
*   La complexité reste donc identique.

**2. Si l'on souhaite trouver l'arbre couvrant de poids maximum. Est-ce que le problème devient difficile ?**

**Réponse : Non.**
Le problème est symétrique. Pour trouver un Arbre Couvrant de Poids **Maximum** :
*   Soit on multiplie tous les poids par -1 et on cherche le Minimum.
*   Soit on modifie Kruskal pour trier les arêtes par ordre **décroissant**.
*   Soit on modifie Prim pour choisir l'arête de poids **maximum** à chaque étape.
La complexité reste la même.

---

## Exercice 4 : Propriété de l'arête de poids minimum

**Question :** Soit G = (V, E, w) un graphe non-orienté valué. Montrez que l'arête e de poids minimum appartient toujours à un Arbre couvrant de poids minimum.

**Preuve (par l'absurde ou par la propriété de coupe) :**
Soit e = (u, v) l'arête de poids minimum unique du graphe.
Supposons qu'il existe un Arbre Couvrant Minimum T qui ne contient pas e.
1.  Si on ajoute e à T, cela crée nécessairement un cycle (car T est un arbre couvrant, il connecte déjà u et v par un chemin).
2.  Ce cycle contient l'arête e et au moins une autre arête e' qui traverse la même coupe que e (c'est-à-dire une autre arête sur le chemin entre u et v dans T).
3.  Comme e est l'arête de poids minimum de tout le graphe, son poids w(e) est strictement inférieur à w(e').
4.  Si on retire e' et qu'on garde e, on obtient un nouvel arbre T' qui est toujours couvrant.
5.  Le poids total de T' est Poids(T') = Poids(T) - w(e') + w(e).
6.  Puisque w(e) < w(e'), alors Poids(T') < Poids(T).
7.  Ceci contredit le fait que T était un Arbre Couvrant *Minimum*.

**Conclusion :** L'arête de poids minimum doit faire partie de l'ACM (si elle est unique). Si plusieurs arêtes ont le même poids minimum, au moins l'une d'entre elles appartient à un ACM.

---

## Exercice 5 : Condition de connexité

**Question :** Montrez que G = (V, E) est un graphe connexe si et seulement si la frontière de tout sous-ensemble de sommets n'est pas vide.

**Explication :** La frontière d'un ensemble X (notée parfois d(X)) est l'ensemble des arêtes qui relient un sommet dans X à un sommet hors de X.

**Preuve :**
*   **Sens direct (=>) :** Si G est connexe.
    Prenez n'importe quel groupe de sommets X (qui n'est ni vide, ni tout le graphe). Puisque le graphe est connexe, il est possible d'aller de n'importe quel sommet de X vers n'importe quel sommet hors de X. Il doit donc forcément y avoir une "route" (une arête) qui sort de X. Donc la frontière de X n'est pas vide.

*   **Sens réciproque (<=) :** Si la frontière n'est jamais vide.
    Supposons par l'absurde que G n'est pas connexe.
    Alors G est coupé en plusieurs morceaux isolés (composantes connexes). Prenons un de ces morceaux, appelons-le C1.
    Si on regarde l'ensemble X = C1, comme c'est un morceau isolé, aucune arête ne le relie au reste du graphe.
    Donc la frontière de C1 est vide.
    Ceci contredit l'hypothèse de départ ("la frontière n'est jamais vide"). Donc G est forcément connexe.

---

## Exercice 6 : Unicité de la liste des poids

**Question :** Soit L la liste triée des poids des arêtes d'un ACM T. Soit T' un autre ACM. Est-ce que la liste triée L' des poids de T' est égale à L ?

**Réponse : VRAI.**

**Théorème :** Pour un graphe donné, tous les arbres couvrants minimums ont exactement la même suite de poids d'arêtes.

**Intuition :**
Même si la *structure* de l'arbre (quelles arêtes sont choisies) peut changer si plusieurs arêtes ont le même poids, la *quantité* d'arêtes de chaque poids nécessaire pour connecter le graphe est fixe.
Par exemple, si on a besoin de 2 arêtes de poids 1 et 1 arête de poids 2 pour connecter tout le monde au moindre coût, tous les ACM auront cette composition, même s'ils ne choisissent pas les mêmes arêtes de poids 1.
