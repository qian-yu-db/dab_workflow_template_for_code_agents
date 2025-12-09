# DAB Workflow Template - Claude Code Instructions

This file provides instructions for Claude Code to work with the Databricks Asset Bundle workflow template.

## Project Overview

This project provides a template for creating, testing, and deploying Databricks workflows using notebooks. It leverages Databricks Asset Bundles (DAB) for infrastructure-as-code workflow management with serverless compute.

## Available Skills

The following skills are available in `.claude/skills/`:

| Skill | Description | Invoke |
|-------|-------------|--------|
| `databricks-asset-bundle` | Generate DAB from notebooks with task dependencies | Use skill |
| `mermaid-diagrams-creator` | Create workflow diagrams (source + images) | Use skill |
| `pytest-test-creator` | Generate unit tests with coverage | Use skill |
| `python-code-formatter` | Format code (blackbricks/black/isort/ruff) | Use skill |

## Workflow

### Step 1: Create Workflow Diagram
Use the `mermaid-diagrams-creator` skill to visualize your workflow based on notebooks in `notebooks/`.

### Step 2: Generate Databricks Asset Bundle
Use the `databricks-asset-bundle` skill to create DAB configuration from the diagram.

### Step 3: Create Unit Tests
Use the `pytest-test-creator` skill to generate and run tests for notebook code.

### Step 4: Format Code
Use the `python-code-formatter` skill to format all Python code.

### Step 5: Deploy and Run
```bash
databricks bundle validate --profile <PROFILE> --target dev
databricks bundle deploy --profile <PROFILE> --target dev
databricks bundle run --profile <PROFILE> --target dev <JOB_NAME>
```

### Step 6: Document
Update README with documentation and workflow diagram images.

## Project Structure

```
.
├── .claude/
│   ├── skills-repo/          # Git submodule with skill definitions
│   ├── skills/               # Symlinks to active skills
│   └── project-context.md    # Project context
├── docs/                     # Project documentation
├── src/                      # Shared Python utilities
├── tests/                    # Test files
├── notebooks/                # Databricks notebooks
├── configs/                  # Configuration files
├── pyproject.toml           # Python project config (uv)
└── README.md
```

## Cross-Platform Support

This template supports multiple AI code agents:
- **Claude Code**: This file (`CLAUDE.md`)
- **Codex CLI**: `AGENTS.md`
- **Gemini CLI**: `GEMINI.md`

All three files contain equivalent instructions adapted for each platform.

## Key Commands

### Mermaid Diagrams
```bash
mmdc -i workflow.mermaid -o workflow.png -b white
```

### Databricks Asset Bundle
```bash
scripts/generate_dab.py my_pipeline --mermaid-file workflow.mermaid
databricks bundle validate -t dev
databricks bundle deploy -t dev
```

### Testing
```bash
uv run pytest --cov=src --cov-report=term-missing
```

### Formatting
```bash
uv run blackbricks notebooks/   # Databricks notebooks
uv run isort src/ && uv run black src/  # Regular Python
uv run ruff check --fix .       # Linting
```

## Configuration

See `pyproject.toml` for tool configurations (pytest, black, isort, ruff).
See `.claude/project-context.md` for detailed project context.
