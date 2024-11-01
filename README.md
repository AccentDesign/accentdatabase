[![Test](https://github.com/accentdesign/accentdatabase/actions/workflows/test.yml/badge.svg)](https://github.com/accentdesign/accentdatabase/actions/workflows/test.yml)

## Commands

### Install dependencies

```bash
uv sync --all-extras
```

### Run tests

```bash
uv run pytest tests
```

### Run linters

ruff:
```bash
uv run ruff format accentdatabase example tests
```
```bash
uv run ruff check --fix accentdatabase example tests
```

### Build package

install dependencies:
```bash
uv tool install hatch
```

build package:
```bash
rm -rf dist && uv build
```

### Publish package

```bash
uv publish --token <token>
```