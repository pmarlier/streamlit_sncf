

# Generate documentation with Sphinx and AutoAPI

> [!NOTE]
> With AutoAPI, docstrings and the project's module structure are automatically identified.

## Generate the documentation

From the project root directory:

```powershell
.\docs\make.bat html
```

The HTML pages are generated in `docs/_build/html`:
- `index.html`: home page
- `autoapi/index.html`: API documentation

## If modules have been deleted or renamed

Clean and then regenerate the documentation:

```powershell
.\docs\make.bat clean
.\docs\make.bat html
```

## Explanation of the configuration files

### `make.bat`

- `SOURCEDIR=.` indicates that the Sphinx root directory is the `docs` folder.
- `BUILDDIR=_build` generates the output in `docs/_build`.

### `conf.py`

The `../src` directory is added to `sys.path` to make the code importable:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
```

The `autoapi.extension` and `sphinx.ext.napoleon` extensions are enabled:

```python
extensions = ["autoapi.extension", "sphinx.ext.napoleon"]
autoapi_dirs = ["../src"]
autoapi_type = "python"
```

- **AutoAPI** automatically scans the entire `src/` directory and generates documentation pages from the docstrings.
- **Napoleon** handles the docstring format.

### `index.rst`

AutoAPI automatically adds its index page (`autoapi/index`) to the `toctree`.