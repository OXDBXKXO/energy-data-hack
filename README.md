# Energy Data Hack

Ce dossier contient tous les dossiers et fichiers relatifs à notre contribution
au hackathon Energy Data Hack, réalisé par le ministère des armées.

# Dépendances

L'installation des dépendances est donnée par la commande :
> pip install -r requirements.txt

# Vue d'ensemble

## Le dossier docs

Le dossier 'docs' contient toutes la documentation du projet. Cette
documentation a été générée grâce à doxypypy.

## La bibliothèque 'keysolver'

Le dossier 'keysolver' est le dossier de la bibliothèque, il contient le
fichier 'solve.py', contenant la fonction 'solve' permettant de trouver
les touches contenues dans un fichier.

Le dossier 'keysolver' est, d'autre part, découpé en trois dossiers :
* Le dossier 'ai' contient les fichiers relatifs à l'IA permettant de
trouver quelles touches ont été pressées.
* Le dossier 'io' contient des fichiers permettant des manipulations d'entrée
et sortie.
* Le dossier 'post_treatment' contient les fichiers relatifs au post traitement
du résultat de l'IA

Un ficher notebook 'main.ipynb' est à disposition à la racine, il s'agit d'un
exemple d'utilisation minimale de la bibliothèque. Si nécessaire, il est
possible d'appeler individuellement les fonctions que la fonction 'solve'
appelle.

## Le dossier 'word_guesser'
