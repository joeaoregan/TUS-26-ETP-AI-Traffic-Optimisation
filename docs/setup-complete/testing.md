# 🧪 Testing

## Test With Included Client
```bash
python test_api.py
```

Tests include:

- Health checks
- Basic functionality
- Custom observation predictions
- Load testing (5 requests)
- Model information retrieval

## Manual Test

```bash
# Test auto-generated action
curl http://localhost:8080/api/traffic/action

# Test custom observations
curl -X POST http://localhost:8080/api/traffic/action \
  -H "Content-Type: application/json" \
  -d '{"observations": [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]}'

# Check API health
curl http://localhost:8080/api/traffic/health

# Check Python model
curl http://localhost:8000/health
```

## Documenation Testing

Before deploying documentation changes to GitHub Pages, verify the MkDocs build and local preview.

### 1. Build Documentation

Generate the static site to catch any errors:

```bash
python -m mkdocs build
```

This creates a site/ directory with the compiled HTML. 

Check for:

- [x] No build errors or warnings in the console
- [x] All links resolve correctly
- [x] Code blocks render properly
- [x] Images load correctly

### 2. Preview Locally

Serve documentation locally and visually inspect all pages:

```bash
python -m mkdocs serve
```

Navigate to http://127.0.0.1:8000/ and test:

- [x] Navigation menu loads correctly
- [x] All internal links work
- [x] Search functionality (if enabled)
- [x] Code examples display properly
- [x] Tables render correctly
- [x] Mobile responsiveness (resize browser window)

### 3. Check for Common Issues

Before deploying, verify:

- [x] No broken links (external or internal)
- [x] File paths are relative (not absolute)
- [x] Image paths point to correct locations
- [x] Code syntax is valid
- [x] Markdown formatting is correct
- [x] All new pages are added to mkdocs.yml navigation

### 4. Deploy to GitHub Pages

Once testing is complete and changes are committed:

```bash
git add .
git commit -m "Update documentation"
python -m mkdocs gh-deploy
```

The documentation will be live at: <https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/>

***Note:** It may take 1-2 minutes for GitHub Pages to update after deployment.*