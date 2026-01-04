# Projet_soutenance_devis
# Nathan Devis - Système de Gestion de Devis

## 🚀 Description
Application web développée avec Django permettant aux utilisateurs de créer, gérer et exporter des devis professionnels aux formats PDF et Word.

## ✨ Fonctionnalités
- Gestion des clients et des produits.
- Calcul automatisé du HT, de la TVA (19.25%) et du TTC.
- Génération de documents PDF (via WeasyPrint).
- Génération de documents Word (via Docxtpl).
- Historique des devis par utilisateur avec numérotation séquentielle.

## 🛠️ Installation
1. Cloner le repository :
   `git@github.com:Nathan8dev/Projet_soutenance_devis.git`
2. Créer un environnement virtuel :
   `python -m venv Env`
3. Activer l'environnement :
   `source Env/bin/activate` (Linux/Mac) ou `Env\Scripts\activate` (Windows)
4. Installer les dépendances :
   `pip install -r requirements.txt`
5. Lancer les migrations :
   `python manage.py migrate`
6. Démarrer le serveur :
   `python manage.py runserver`
