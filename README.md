# Module de Calcul et de Simulation d'Emprunts et de Prêts

Ce projet implémente un simulateur d'emprunts et de prêts avec calcul des annuités et génération d'un tableau d'amortissement.

## 🧭 Objectifs
- Fournir une interface (frontend) pour saisir les paramètres d'un emprunt/prêt.
- Calculer : montant des remboursements, durée (si manquante), et génération du tableau d'amortissement.
- Fournir une API backend pour effectuer les calculs.

## 🗃️ Structure du projet
- `backend/` : API en Python + Flask
- `frontend/` : interface web en HTML/CSS/JavaScript

## 🚀 Exécution (local)
### Prérequis
- Python 3.10+ installé
- (Optionnel) Git pour versionner le projet

### 1) Initialiser Git (sur votre machine)
```sh
cd loan-simulator
git init
git add .
git commit -m "Initial project"
```

### 2) Installer les dépendances
```sh
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
```

### 3) Lancer le backend
```sh
cd backend
python app.py
```

### 4) Ouvrir le frontend
Ouvrez `frontend/index.html` dans votre navigateur (double-clic), puis utilisez le formulaire.

> 💡 Si vous souhaitez lancer le frontend via un serveur local (recommandé pour éviter les restrictions CORS), vous pouvez exécuter :
> ```sh
> python -m http.server --directory frontend 8000
> ```
> Puis ouvrez http://localhost:8000

## 🧾 Ajouter ce projet à votre CV
Mentionnez-le comme un projet personnel / de démonstration avec les points suivants :
- Implémentation d'un calculateur de prêt (annuité, amortissement)
- Génération d'un tableau d'amortissement détaillé
- API REST avec Flask (Python)
- Frontend HTML/CSS/JavaScript (formulaire + affichage de résultats)

## 📚 À améliorer / prochaines étapes
- Ajout de tests unitaires (pytest)
- Authentification (connexion utilisateur)
- Export du tableau d'amortissement en PDF/Excel
- Graphiques (matplotlib / chart.js)
