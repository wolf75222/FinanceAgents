# Bilan Extractor

Un outil pour extraire automatiquement les variables financières des bilans comptables.

## Fonctionnalités

- Lecture de fichiers au format PDF
- Conversion vers Markdown via Docling
- Extraction des variables financières via LLM (Ollama + Gemma 3B)
- Extraction de différents types de valeurs (brut, net, amortissement)
- Extraction de valeurs pour des années spécifiques
- Configuration flexible des variables à extraire via JSON
- Sortie au format JSON

## Variables extraites

Par défaut, les variables financières suivantes sont extraites :

- Actif total
- Passif total
- Capitaux propres
- Résultat net
- Chiffre d'affaires
- Dettes

Mais l'outil peut désormais extraire n'importe quelle variable financière définie dans le fichier de configuration `bilan_extractor/config/variables.json`, y compris des variables spécifiques avec des codes comptables comme :

- 2154220 MAT IND SUBV BIOCLAD 2012
- 2818300 AMORT/MAT BUREAU ET INFORM
- Et bien d'autres...

Pour chaque variable, l'outil peut extraire différents types de valeurs :
- Valeur brute (avant amortissements et provisions)
- Valeur nette (après amortissements et provisions)
- Valeur des amortissements et provisions

L'outil peut également extraire les valeurs pour une année spécifique.

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
- `--year` : Année spécifique pour laquelle extraire les valeurs (ex: 2023)
- `--value-type` : Type de valeur à extraire (choix: brut, net, amortissement)
- `--verbose` : Activer la sortie détaillée

Exemples:
```bash
# Extraire toutes les variables avec toutes les valeurs disponibles
python -m bilan_extractor.main chemin_vers_fichier.pdf

# Extraire uniquement les valeurs nettes pour l'année 2023
python -m bilan_extractor.main chemin_vers_fichier.pdf --year 2023 --value-type net

# Extraire uniquement les valeurs brutes et sauvegarder le résultat
python -m bilan_extractor.main chemin_vers_fichier.pdf --value-type brut --output resultats.json
```

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

3. **Bilan Extractor Year and Value Type** : Configuration pour extraire des valeurs spécifiques
   - Chemin du fichier PDF : `C:\Users\romai\Documents\test.pdf`
   - Année : `2023` (extrait uniquement les valeurs pour cette année)
   - Type de valeur : `net` (extrait uniquement les valeurs nettes)
   - Sortie JSON : sauvegardée dans le dossier `output` du projet

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

#### Format de sortie précédent (pour compatibilité)

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

#### Nouveau format de sortie (avec types de valeurs et années)

```json
{
  "actif_total": {
    "name": "actif_total",
    "values": [
      {
        "value": 542000,
        "value_type": "brut",
        "year": 2023
      },
      {
        "value": 520000,
        "value_type": "net",
        "year": 2023
      }
    ]
  },
  "passif_total": {
    "name": "passif_total",
    "values": [
      {
        "value": 478000,
        "value_type": "net",
        "year": 2023
      }
    ]
  },
  "2154220_mat_ind_subv_bioclad_2012": {
    "name": "2154220_mat_ind_subv_bioclad_2012",
    "code": "2154220",
    "values": [
      {
        "value": 50000,
        "value_type": "brut",
        "year": 2023
      },
      {
        "value": 20000,
        "value_type": "amortissement",
        "year": 2023
      },
      {
        "value": 30000,
        "value_type": "net",
        "year": 2023
      }
    ]
  }
}
```

## Structure du projet

```
bilan_extractor/
│
├── main.py                    # Point d'entrée principal
│
├── config/
│   ├── settings.py            # Configuration générale
│   └── variables.json         # Configuration des variables à extraire
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

## Configuration des variables à extraire

L'outil utilise un fichier de configuration JSON pour définir les variables à extraire. Ce fichier se trouve à l'emplacement `bilan_extractor/config/variables.json`.

### Structure du fichier de configuration

```
{
  "default_variables": [
    {
      "name": "actif_total",
      "aliases": ["actiftotal", "actif total", "total actif", "total de l'actif"],
      "description": "Total des actifs"
    },
    {
      "name": "passif_total",
      "aliases": ["passiftotal", "passif total", "total passif", "total du passif"],
      "description": "Total des passifs"
    }
  ],
  "additional_variables": [
    {
      "name": "2154220_mat_ind_subv_bioclad_2012",
      "code": "2154220",
      "aliases": ["MAT IND SUBV BIOCLAD 2012", "2154220 MAT IND SUBV BIOCLAD 2012"],
      "description": "Matériel industriel subventionné BIOCLAD 2012"
    },
    {
      "name": "2818300_amort_mat_bureau_inform",
      "code": "2818300",
      "aliases": ["AMORT/MAT BUREAU ET INFORM", "2818300 AMORT/MAT BUREAU ET INFORM"],
      "description": "Amortissements sur matériel de bureau et informatique"
    }
  ]
}
```

> **Note**: Vous pouvez ajouter autant de variables que nécessaire dans les sections `default_variables` et `additional_variables`.

### Champs disponibles

Pour chaque variable :
- `name` (obligatoire) : Identifiant unique de la variable (utilisé dans la sortie JSON)
- `aliases` (recommandé) : Liste des noms alternatifs qui peuvent apparaître dans le bilan
- `code` (optionnel) : Code comptable associé à la variable
- `description` (optionnel) : Description de la variable

### Comment ajouter une nouvelle variable

Pour ajouter une nouvelle variable à extraire :

1. Ouvrez le fichier `bilan_extractor/config/variables.json`
2. Ajoutez une nouvelle entrée dans la section `additional_variables`
3. Définissez au minimum le champ `name` et idéalement les champs `aliases` pour améliorer la détection
4. Sauvegardez le fichier

Exemple d'ajout d'une nouvelle variable :
```json
{
  "name": "immobilisations_corporelles",
  "aliases": ["immobilisations corporelles", "total immobilisations corporelles"],
  "description": "Total des immobilisations corporelles"
}
```

## Extensions possibles

- Visualisation des ratios (liquidité, solvabilité, etc.)
- Détection automatique de la structure du bilan (par année, par entité)
- Traitement de plusieurs fichiers à la suite
- Interface utilisateur avec Textualize

## Licence

MIT