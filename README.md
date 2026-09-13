# 7Manager

API backend de 7Manager, construite avec [FastAPI](https://fastapi.tiangolo.com/) et [Supabase](https://supabase.com/) (base de données PostgreSQL + authentification).

## Stack

- **FastAPI** — framework API
- **Supabase** — base de données et authentification (inscription / connexion)
- **Pydantic** — validation des données
- **Uvicorn** — serveur ASGI

## Structure du projet

```
7manager/
├── main.py                 # Point d'entrée FastAPI
├── requirements.txt
├── .env                     # Variables d'environnement (non versionné)
└── app/
    ├── core/
    │   └── database.py      # Client Supabase
    ├── auth/                # Inscription / connexion des utilisateurs
    │   ├── router.py
    │   ├── service.py
    │   └── models.py
    └── postes/               # Gestion des postes
        ├── router.py
        ├── service.py
        └── models.py
```

## Installation

1. Cloner le dépôt et se placer dans le dossier :
   ```bash
   git clone https://github.com/kenanTurhan/7Manager.git
   cd 7Manager
   ```

2. Créer et activer un environnement virtuel :
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Créer un fichier `.env` à la racine du projet avec les variables suivantes :
   ```
   SUPABASE_URL=<url_du_projet_supabase>
   SUPABASE_KEY=<clé_publique_supabase>
   SUPABASE_SECRET=<clé_secrète_supabase>
   ```

## Lancer le projet

```bash
uvicorn main:app --reload
```

L'API est ensuite disponible sur `http://127.0.0.1:8000`, avec la documentation interactive sur `http://127.0.0.1:8000/docs`.

## Endpoints principaux

### Auth (`/api/auth`)

| Méthode | Route | Description |
|---|---|---|
| POST | `/inscription` | Créer un compte utilisateur |
| POST | `/connexion` | Se connecter et obtenir un token d'accès |

### Postes (`/api/postes`)

| Méthode | Route | Description |
|---|---|---|
| POST | `/ajouter_poste` | Ajouter un poste |
| DELETE | `/retirer_poste` | Retirer un poste |
| PATCH | `/actualiser_poste` | Modifier un poste existant |
