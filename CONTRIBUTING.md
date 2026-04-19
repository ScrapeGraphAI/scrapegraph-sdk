# Contributing to scrapegraph-py

## Setup

```bash
uv sync
```

## Development

```bash
uv build             # build to dist/
uv run ruff check .  # lint
```

## Before committing

Run all checks:

```bash
uv run ruff format src/ tests/  # auto-fix formatting
uv run ruff check src/ tests/   # check for errors
uv run pytest tests/test_client.py -v  # unit tests
```

## Testing

```bash
uv run pytest tests/test_client.py -v       # unit tests only
uv run pytest tests/test_integration.py -v  # live API tests (requires SGAI_API_KEY)
```

For integration tests, set `SGAI_API_KEY` in your environment or `.env` file.

## Commit messages

Use conventional commits:

- `feat:` new feature
- `fix:` bug fix
- `refactor:` code change (no new feature, no bug fix)
- `chore:` maintenance (deps, config)
- `test:` add/update tests
- `docs:` documentation

## Pull requests

1. Fork and create a branch from `main`
2. Make changes
3. Run all checks (see above)
4. Submit PR to `main`

## License

MIT - contributions are licensed under the same license.
