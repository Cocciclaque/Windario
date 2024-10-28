# Windario 

### Qu'est-ce que c'est ?

<p> Windario est un puzzle platformer développé sous PyGame originallement supposé utiliser un fond transparent et des mécaniques de "fenêtres" déplaçables comme élément de gameplay principal, d'où son nom, Window Mario.

Après beaucoup de code et de réflexion, ces idées ont été mises de côté pour à la place implémenter un système de "copié collé" en reprenant mon système de fenêtre, où le joueur peut copier des éléments existants du terrain, les coller à d'autres endroits pour arriver à la fin du niveau. </p>

### Comment exécuter ?

<p> Bien que le jeu ne soit pas disponible à l'heure actuelle car 90% de mon code source ne me sera disponible que demain matin, le jeu est exécutable en exécutant python.exe sur le fichier main.py, en le faisant depuis le dossier du jeu. 

Exemple : 
```
$ cd C:\Users\kilia\OneDrive\Documents\PYTHON\Games\windario>
$ python.exe main.py
```
(remplacer python.exe par votre emplacement de python si python n'est pas ajouté à la variable PATH)
Aucune librairie (à part pygame) n'est à installer, tout a été développé à la main. </p>

### Fonctionnalités et comment jouer 

<p> Arrivé sur le menu, simplement sélectionner "Play game" pour lancer le premier niveau. <hr>
Le joueur peut se déplacer en utilisant Q et D pour aller respectivement de gauche à droite, et la barre espace pour sauter. <br>
Le but du jeu est simplement d'atteindre le drapeau à chaque niveau.</p>

##### Mécanique spéciale :
<p> On remarque en partie un texture indiquant un nombre de "copié collé" disponible. <br>
En appuyant sur la touche "r", la logique du jeu s'arrête et nous pouvons sélectionner un rectangle en cliquant d'abord sur le bord haut-gauche puis le bord bas-droite, ce qui crée une "fenêtre" (une sous-surface pygame). <br>
Cela nous permet de déplacer un élement du terrain ailleurs, sans les ennemis et l'arrivée pour nous servir de formes préfaites pour créer nos propres platformes et arriver à la fin du niveau. <br>
On peut annuler la copie en faisant un clic-droit en mode copie. </p>

##### Comment battre les ennemis ? :
<p> Etant un jeu de puzzle, j'ai préféré abordé une logique plus orientée sur la créativité du joueur et en enlevant les éléments superflus. Le joueur n'a pas de vies, ni de score. Certains powerups permettant de récupérer une nouvelle opportunité de copie sont disponibles et nous permettent d'achever notre but différemment. <br>
Les ennemis sont immortels, et flottent, pour deux raisons : <br>
- La prémière est que j'ai simplement préféré rendre les ennemis des choses à éviter à des choses à combattre. <br>
- La deuxième est que j'avais simplement d'autres fonctionnalités sur lesquelles me concentrer, donc j'ai du rayer ceci en profit d'autres éléments. (j'avais un peu la flemme soyons honnête). </p>

### Comment fermer le jeu ?

<p> On peut à tout moment fermer le jeu en appuyant sur ECHAP ou simplement en quittant les nombreux boutons "Quit game" disséminés à travers les nombreux menus (lors de la mort, de la victoire, etc). </p>