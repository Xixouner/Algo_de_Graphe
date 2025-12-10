# Exercices Corrigés - Coloration

Voici les corrections pour la série d'exercices sur la coloration de graphes.

## Exercice 1 : Relation entre Chi et Omega

**Question :** Laquelle de ces affirmations est vraie ?
*   Chi <= Omega
*   Omega <= Chi

**Réponse : Omega <= Chi est VRAIE.**

*   **Omega (w)** est la taille de la plus grande clique (un groupe de sommets tous reliés entre eux).
*   **Chi (x)** est le nombre chromatique (nombre minimum de couleurs pour colorier le graphe).

**Explication :**
Dans une clique de taille k, chaque sommet est relié à tous les autres. Il est donc impossible de donner la même couleur à deux sommets de la clique. Il faut donc obligatoirement **au moins k couleurs** différentes juste pour colorier cette clique.
Par conséquent, le nombre total de couleurs nécessaires pour le graphe entier (Chi) est forcément supérieur ou égal à la taille de la plus grande clique (Omega).

---

## Exercice 2 : Algorithme Glouton sur Kn,n moins un couplage

**Graphe :** G est un graphe biparti complet Kn,n (deux ensembles A et B de n sommets) auquel on a retiré un couplage parfait (on a enlevé les arêtes (a1, b1), (a2, b2)... (an, bn)).
Cela signifie que a_i est relié à tous les b_j sauf b_i.

**1. Permutation pour 2 couleurs (Minimum)**
Puisque le graphe est biparti (les arêtes ne vont que de A vers B), il est 2-coloriable.
*   **Ordre :** D'abord tous les sommets de A, puis tous les sommets de B.
    *   a1, a2, ..., an, b1, b2, ..., bn
*   **Exécution :**
    *   Tous les a_i prennent la couleur 1 (ils ne sont pas reliés entre eux).
    *   Tous les b_i prennent la couleur 2 (ils sont reliés aux a_i, donc pas couleur 1, mais pas reliés entre eux).
*   **Total :** 2 couleurs.

**2. Permutation pour un nombre maximum de couleurs**
On veut piéger l'algorithme glouton.
*   **Ordre :** a1, b1, a2, b2, ..., an, bn.
*   **Exécution :**
    *   **a1** : Couleur 1.
    *   **b1** : N'est PAS relié à a1 (arête retirée). Prend la couleur 1.
    *   **a2** : Relié à b1 (couleur 1). Prend la couleur 2.
    *   **b2** : Relié à a1 (couleur 1). N'est PAS relié à a2. Prend la couleur 2.
    *   **a3** : Relié à b1 (1) et b2 (2). Prend la couleur 3.
    *   **b3** : Relié à a1 (1) et a2 (2). Prend la couleur 3.
    *   ...
    *   **an, bn** : Reliés à tous les b_j et a_j précédents (couleurs 1 à n-1). Prennent la couleur n.
*   **Total :** n couleurs seront utilisées.

---

## Exercice 3 : Sommet d'articulation

**Question :** Soit v un sommet d'articulation séparant le graphe en deux blocs G1 et G2. Montrez que Chi(G) = max(Chi(G1), Chi(G2)).

**Preuve :**
1.  **Borne inférieure :** G contient G1 et G2 comme sous-graphes. Donc il faut au moins autant de couleurs que pour G1 et autant que pour G2. Donc Chi(G) >= max(Chi(G1), Chi(G2)).
2.  **Borne supérieure (Construction) :**
    *   Coloriez G1 avec k1 = Chi(G1) couleurs. Le sommet v reçoit une couleur c1.
    *   Coloriez G2 avec k2 = Chi(G2) couleurs. Le sommet v reçoit une couleur c2.
    *   Supposons k1 >= k2. On a k1 couleurs disponibles.
    *   Dans le coloriage de G2, on peut permuter les couleurs (échanger les noms des couleurs) pour faire en sorte que v reçoive la couleur c1 (la même que dans G1).
    *   Maintenant, les deux coloriages sont compatibles au niveau du sommet v (le seul point commun).
    *   On fusionne les deux coloriages. Le nombre total de couleurs utilisé est max(k1, k2).

---

## Exercice 4 : Graphes k-dégénérés

**Définition :** Un graphe est k-dégénéré si on peut le réduire à vide en supprimant successivement des sommets de degré <= k.

**1. Équivalence**
Un graphe est k-dégénéré SI ET SEULEMENT SI tout sous-graphe contient au moins un sommet de degré <= k.
*   Si on peut supprimer successivement, à chaque étape le sommet supprimé avait degré <= k dans le graphe restant (qui est un sous-graphe).
*   Inversement, si tout sous-graphe a un sommet de degré faible, on peut toujours en trouver un à supprimer pour continuer la réduction.

**2. Graphes 1-dégénérés**
Ce sont les graphes qui contiennent toujours un sommet de degré 0 ou 1.
Si on supprime ces sommets récursivement, on finit par tout supprimer.
Cela correspond aux **Forêts** (graphes sans cycles).
*   Un cycle a tous ses sommets de degré 2. Donc un graphe avec un cycle n'est pas 1-dégénéré (le cycle restera bloqué).

**3. k-dégénéré => (k+1)-coloriable**
Utilisons l'algorithme glouton avec un ordre intelligent.
*   **Ordre :** L'inverse de l'ordre de suppression. On commence par le dernier sommet supprimé, on remonte jusqu'au premier.
*   Soit v un sommet dans cet ordre. Quand c'est son tour d'être colorié, il a un certain nombre de voisins déjà coloriés.
*   Ces voisins sont ceux qui étaient *après* lui dans l'ordre de suppression (donc présents dans le graphe au moment où v a été supprimé).
*   Par définition de la k-dégénérescence, v avait au plus k voisins dans ce graphe résiduel.
*   Donc v a au plus k voisins déjà coloriés.
*   Parmi k+1 couleurs disponibles, il en reste forcément au moins une libre pour v.
*   Donc le graphe est (k+1)-coloriable.

---

## Exercice 5 : Théorème de Vizing

**Question :** Montrez le théorème de Vizing : Chi' <= Delta + 1.

**Définitions :**
*   **Chi' (x')** : Indice chromatique (nombre de couleurs pour colorier les ARÊTES).
*   **Delta** : Degré maximum du graphe.

**Énoncé :**
Le nombre de couleurs nécessaires pour colorier les arêtes d'un graphe est soit égal au degré maximum (Delta), soit égal à Delta + 1.
*   On a évidemment Chi' >= Delta (car un sommet de degré Delta a Delta arêtes incidentes qui doivent toutes avoir des couleurs différentes).
*   Vizing a prouvé que l'on n'a jamais besoin de plus de Delta + 1 couleurs.

**Note :** La preuve complète est complexe et dépasse généralement le cadre d'un simple exercice, mais le résultat est fondamental à connaître.
Pour les graphes bipartis, on a toujours Chi' = Delta.
Pour les graphes généraux, c'est soit Delta (Classe 1), soit Delta + 1 (Classe 2).
