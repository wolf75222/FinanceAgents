# Bilan Extractor

Un outil pour extraire automatiquement les variables financières des bilans comptables.

## Fonctionnalités

- Lecture de fichiers au format PDF
- Conversion vers Markdown via Docling
- Extraction des variables financières via LLM (Ollama + Gemma 3B)
- Sortie au format JSON

## Variables extraites

- Actif total
- Passif total
- Capitaux propres
- Résultat net
- Chiffre d'affaires
- Dettes

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/votre-utilisateur/bilan-extractor.git
cd bilan-extractor

# Installer les dépendances
pip install -r requirements.txt

# Installer Ollama (si ce n'est pas déjà fait)
# Voir https://ollama.ai/download

# Télécharger le modèle Gemma 3
ollama pull gemma3
```

## Utilisation

### Ligne de commande

```bash
python -m bilan_extractor.main chemin_vers_fichier.pdf
```

Options disponibles:
- `--model` : Modèle Ollama à utiliser (par défaut: gemma3)
- `--output` : Chemin pour sauvegarder la sortie JSON
- `--markdown` : Chemin pour sauvegarder le Markdown intermédiaire
- `--verbose` : Activer la sortie détaillée

### Variables d'environnement

L'application prend en charge les variables d'environnement suivantes :

- `DISABLE_DOCLING` : Désactive l'utilisation de docling et force l'utilisation de PyPDF2 pour l'extraction de texte (valeurs acceptées : "1", "true", "yes")
- `DISABLE_SSL_VERIFICATION` : Désactive la vérification des certificats SSL lors des requêtes HTTPS effectuées par docling (valeurs acceptées : "1", "true", "yes"). Utile en cas d'erreurs SSL, mais déconseillé en production pour des raisons de sécurité.
- `OLLAMA_MODEL` : Définit le modèle Ollama par défaut (par défaut : "gemma3")
- `OLLAMA_HOST` : Définit l'hôte Ollama (par défaut : "http://localhost:11434")

### PyCharm

Des configurations de lancement PyCharm sont incluses dans le projet pour faciliter l'exécution de l'application :

1. **Bilan Extractor PDF** : Configuration simple pour lancer l'application avec un fichier PDF
   - Chemin du fichier PDF : `C:\Users\romai\Documents\test.pdf` (à modifier selon vos besoins)

2. **Bilan Extractor With Options** : Configuration avancée avec options supplémentaires
   - Chemin du fichier PDF : `C:\Users\romai\Documents\test.pdf`
   - Modèle : `gemma:3b`
   - Sortie JSON : sauvegardée dans le dossier `output` du projet
   - Mode verbose activé

Pour utiliser ces configurations :
1. Ouvrez le projet dans PyCharm
2. Sélectionnez la configuration souhaitée dans le menu déroulant en haut à droite
3. Cliquez sur le bouton de lecture (triangle vert)

Pour modifier une configuration :
1. Cliquez sur le menu déroulant des configurations
2. Sélectionnez "Edit Configurations..."
3. Modifiez les paramètres selon vos besoins (notamment le chemin du fichier PDF)

> **Important** : Si vous rencontrez l'erreur "Please select a valid Python interpreter", vous devez configurer un interpréteur Python valide :
> 1. Dans PyCharm, allez dans File > Settings > Project: FinanceAgents > Python Interpreter
> 2. Cliquez sur l'icône d'engrenage (⚙️) puis "Add..."
> 3. Sélectionnez un interpréteur Python existant ou créez un environnement virtuel
> 4. Cliquez sur "OK" pour appliquer les changements

### Exemple de sortie

```json
{
  "actif_total": 542000,
  "passif_total": 478000,
  "capitaux_propres": 64000,
  "résultat_net": 8200,
  "chiffre_affaires": 235000,
  "dettes": 415000
}
```

## Structure du projet

```
bilan_extractor/
│
├── main.py                    # Point d'entrée principal
│
├── config/
│   └── settings.py            # Configuration générale
│
├── core/                      # Cœur métier
│   ├── converter.py           # Conversion PDF → Markdown
│   ├── loader.py              # Chargement des fichiers
│   ├── extractor.py           # Appels au LLM (Ollama)
│   └── parser.py              # Nettoyage & parsing JSON
│
├── services/                  # Services externes
│   ├── ollama_client.py       # Wrapper Ollama
│   └── docling_wrapper.py     # Wrapper docling avec DocumentConverter
│
├── models/                    # Définition des modèles de données
│   └── variables.py           # Dataclass pour les variables financières
│
├── utils/
│   └── logger.py              # Gestion du logging
│
└── tests/                     # Tests unitaires
```

## Extensions possibles

- Visualisation des ratios (liquidité, solvabilité, etc.)
- Détection automatique de la structure du bilan (par année, par entité)
- Traitement de plusieurs fichiers à la suite
- Interface utilisateur avec Textualize

## Licence

MIT