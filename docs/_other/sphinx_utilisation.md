# Utilisation de Sphinx avec AutoAPI

> [!NOTE]
> Avec AutoAPI, les docstrings et la structuration du projet avec les modules est identifiée automatiquement.

## Lancer la génération de la doc

Depuis la racine du projet :

```powershell
uv run docs\make.bat html
```

Les pages HTML sont générées dans `docs/_build/html` :
- `index.html` : page d'accueil
- `autoapi/index.html` : documentation de l'API

## Si des modules ont été supprimés ou renommés

Clean puis regénérer la doc :

```powershell
.\docs\make.bat clean
.\docs\make.bat html
```

## Explication des fichiers de configuration :

### `make.bat`

- `SOURCEDIR=.` indique que la racine Sphinx est le dossier `docs`.
- `BUILDDIR=_build` génère le résultat dans `docs/_build`.

### `conf.py`

Le dossier `../src` est ajouté au `sys.path` pour rendre le code importable :

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
```

Les extensions `autoapi.extension` et `sphinx.ext.napoleon` sont activées :

```python
extensions = ["autoapi.extension", "sphinx.ext.napoleon"]
autoapi_dirs = ["../src"]
autoapi_type = "python"
```

- **AutoAPI** scanne automatiquement tout le dossier `src/` et génère les
  pages de documentation à partir des docstrings.
- **Napoleon** gère le format des docstrings.

### `index.rst`

AutoAPI ajoute automatiquement sa page d'index (`autoapi/index`) au `toctree`.