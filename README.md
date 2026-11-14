# Locale Guard

Validate JSON translation catalogs before release. Detect missing/extra keys and placeholder mismatches against a canonical locale.

```bash
python -m pip install .
locale-guard locales/en.json locales/de.json locales/fr.json
locale-guard --json locales/en.json locales/de.json
```

Supports nested JSON objects and named brace or printf-style placeholders. This is a structural QA tool, not a machine translation or grammatical quality checker.

## Tests
```bash
python -m unittest discover -s tests -v
```

MIT License.
