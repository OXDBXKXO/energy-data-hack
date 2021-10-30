# Hackaton Energy Data Hack

Ce dépôt contient tous les dossiers et fichiers relatifs à notre contribution
au hackathon Energy Data Hack, organisé par le Ministère des Armées.

# Dépendances

L'installation des dépendances est réalisée par la commande :
> pip install -r requirements.txt

Il est possible de télécharger le modèle d'IA pré-généré depuis
la section "Releases" de ce dépôt.

# Vue d'ensemble

## Le dossier docs

Le dossier 'docs' contient toutes la documentation du projet. Cette
documentation a été générée grâce à doxypypy.

## La bibliothèque 'keysolver'

Le dossier 'keysolver' contient le fichier 'solve.py', dont la fonction 
'solve' permet de retrouver les touches contenues dans un fichier.

Le dossier 'keysolver' est, d'autre part, découpé en trois dossiers :
* Le dossier 'ai' contient les fichiers relatifs à l'IA permettant de
retrouver quelles touches ont été pressées.
* Le dossier 'io' contient des fichiers permettant des manipulations d'entrée
et sortie.
* Le dossier 'post_treatment' contient les fichiers relatifs au post-traitement
du résultat de l'IA

Un ficher notebook 'main.ipynb' est à disposition à la racine, il s'agit d'un
exemple d'utilisation minimale de la bibliothèque.

## Le dossier 'word_guesser'

Le dossier 'word_guesser' contient toute la logique relative à la recherche des
identifiants à partir du résultat brut de 'keysolver'. Nous avons choisi l'approche
de l'attaque par dictionnaire personnalisé. Dans le cas d'une attaque réelle, un attaquant
cherchera à personnaliser son attaque en créant un dictionnaire relatif à sa cible. Nous
avons donc créé l'outil 'custom_wordlist_gen.py' qui permet de créer un dictionnaire à partir d'une
liste de mots prédéfinis. Dans notre cas cette liste contient des mots comme "hackaton",
"energy", "data" ou "2021". Nous avons ensuite créé l'outil 'wordlist_levenshtein.py'
qui permet de renvoyer les mots avec la plus faible distance de Levenshtein par rapport à un
mot ou d'une liste de mots. Dans notre cas, nous utilisons en entrée la liste de tous
les mots possibles renvoyée par 'keysolver'.
