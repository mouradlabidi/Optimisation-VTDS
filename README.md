# Optimisation des Paramètres de la Politique de Vacances à Deux Seuils (VTDS)

Ce projet vise à optimiser les paramètres de la politique de vacances à deux seuils (VTDS) pour réduire la consommation d'énergie des capteurs tout en minimisant le délai d'attente dans les réseaux de capteurs sans fil (WSN). Il inclut une interface graphique permettant d'évaluer les performances de différentes configurations de paramètres et d'optimiser ces paramètres en utilisant plusieurs algorithmes de résolution.

#Fonctionnalités
- Évaluation des paramètres : Calcule le délai d'attente et l'énergie consommée par un capteur avec une configuration donnée.
- Optimisation des paramètres : Implémente plusieurs méthodes d'optimisation pour trouver la meilleure configuration des paramètres VTDS, notamment :
    1. Recherche exhaustive
    2. Recuit simulé
    3. Recherche Tabou
    4. Optimisation par essaim de particules (PSO)

#Installation
1. Clonez le repository sur votre machine locale :
   git clone https://github.com/mouradlabidi/PFE-Optimisation-VTDS.git
2. Naviguez dans le répertoire du projet :
   cd PFE-Optimisation-VTDS
3. Installez les dépendances nécessaires (par exemple, pour Python, si applicable) :
   pip install -r requirements.txt

#Utilisation
1. Exécutez l'application pour lancer l'interface graphique :
    python App.py
3. Utilisez l'interface pour :
   . Tester différentes combinaisons de paramètres et voir les résultats (délai d'attente, énergie consommée)
   . Optimiser les paramètres en sélectionnant l'algorithme souhaité.

#Technologies Utilisées
  1. Langage : Python
  2. Framework : tkinter pour l'interface graphique
  3. Algorithmes d'optimisation : Recuit simulé, Recherche Tabou, PSO

#Contribuer
- Les contributions sont les bienvenues ! Si vous avez des idées pour améliorer ce projet, n'hésitez pas à soumettre une pull request ou à ouvrir une issue.
