# 📚 Documentation Files

This project uses **MkDocs** with Material theme to generate comprehensive documentation hosted on GitHub Pages.

## Documentation Structure

All documentation is organised in the `docs/` folder:

docs/ MkDocs documentation directory, and README.md

```
│   CHANGELOG.md
│   DOCUMENTATION.md
│   FILE_MANIFEST.md
│   QUICKSTART.md
│   README.md
│   SUPPORT.md
│   SYSTEM_ARCHITECTURE.md
│
├───1_home
│       10_ts.md
│       11_prod.md
│       3_setup.md
│       4_api.md
│       5_env.md
│       6_docker.md
│       7_log.md
│       8_model.md
│       9_performance.md
│       INDEX.md
│
└───4_setup
        10_documentation_files.md
        11_next_steps.md
        12_troubleshooting.md
        13_support.md
        14_notes.md
        1_created.md
        2_quickstart.md
        3_architecture.md
        4_features.md
        5_api_endpoints.md
        6_different_models.md
        7_testing.md
        8_environment_variables.md
        9_dev_vs_prod.md
        index.md
        SETUP_COMPLETE.md
```

## Key Scripts

| File | Purpose |
|------|---------|
| [select_model.py](https://github.com/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation/blob/main/select_model.py) | Model selection tool |
| [test_api.py](https://github.com/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation/blob/main/test_api.py) | API test suite |

## MkDocs

Install mkdocs:

```bash
pip install mkdocs
```

### Local Development

Preview documentation locally at <http://127.0.0.1:8000/>:

```bash
python -m mkdocs serve 
```

### Build for Production

To build MkDocs:

```bash
python -m mkdocs build
```

### Deploy to GitHub Pages

Deploy built documentation to GitHub Pages.

```bash
python -m mkdocs gh-deploy
```

***Note**: Ensure all changes are committed before deploying. The `gh-deploy` command pushes to the `gh-pages` branch.*

### View online

Live Documentation <https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/>