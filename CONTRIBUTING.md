# Contributing to Dynamic Viz

Thank you for your interest in contributing! 💚

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/dynamic-viz.git`
3. Install dev dependencies: `pip install -e ".[dev]"`
4. Create a branch: `git checkout -b feature/your-feature`

## Development

```bash
# Run tests
pytest

# Format code
black src tests

# Lint
ruff check src tests
```

## Pull Request Process

1. Ensure tests pass
2. Update documentation if needed
3. Add a clear description of changes
4. Reference any related issues

## Code Style

- We use Black for formatting (line length 100)
- Type hints are encouraged
- Docstrings for all public methods

## Adding New Chart Types

1. Add generator method to `DynamicVizEngine._gen_{chart_type}()`
2. Add to `generators` dict in `generate()`
3. Add helper method to `AIVizAssistant`
4. Add tests
5. Update README

## Questions?

Open an issue or reach out to opensource@getcognition.ai

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
