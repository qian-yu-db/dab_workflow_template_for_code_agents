# Setup Guide

## Prerequisites

### Required Tools
1. **Python 3.11+**: The project requires Python 3.11 or later
2. **uv**: Fast Python package manager
3. **Git**: Version control with submodule support
4. **Databricks CLI**: For bundle deployment

### Optional Tools
- **Mermaid CLI**: For exporting diagrams to PNG/SVG
- **Pre-commit**: For automated code checks

## Installation

### 1. Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### 2. Clone the Repository

```bash
git clone --recurse-submodules <repo-url>
cd dab_workflow_template_for_code_agents
```

If you forgot `--recurse-submodules`:
```bash
git submodule update --init --recursive
```

### 3. Install Python Dependencies

```bash
uv sync
```

This creates a `.venv/` directory and installs all dependencies.

### 4. Install Databricks CLI

```bash
# Using homebrew (macOS)
brew install databricks/tap/databricks

# Using pip
pip install databricks-cli

# Or download from Databricks
# https://docs.databricks.com/dev-tools/cli/install.html
```

## Configuration

### Databricks Authentication

#### Option 1: Interactive Configuration
```bash
databricks configure
```

#### Option 2: Environment Variables
```bash
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="your-token"
```

#### Option 3: Profile File
Create `~/.databrickscfg`:
```ini
[DEFAULT]
host = https://your-workspace.cloud.databricks.com
token = your-token
```

### Pre-commit Hooks (Optional)

```bash
# Install pre-commit
uv add --dev pre-commit

# Install hooks
uv run pre-commit install
```

## Verification

### Check Python Environment
```bash
uv run python --version
```

### Run Tests
```bash
uv run pytest -v
```

### Check Databricks Connection
```bash
databricks auth describe
```

### Validate Bundle (after creating one)
```bash
databricks bundle validate
```

## Development Workflow

### 1. Create Notebooks
Add your Databricks notebooks to the `notebooks/` directory.

### 2. Generate Tests
Use the `pytest-test-creator` skill to generate tests:
```
Ask Claude Code to use the pytest-test-creator skill
```

### 3. Run Tests
```bash
uv run pytest --cov
```

### 4. Format Code
Use the `python-code-formatter` skill or run manually:
```bash
uv run black .
uv run isort .
uv run ruff check --fix .
```

### 5. Create Workflow Diagram (Optional)
Use the `mermaid-diagrams-creator` skill to visualize your workflow.

### 6. Generate DAB Configuration
Use the `databricks-asset-bundle` skill to generate bundle configuration.

### 7. Deploy
```bash
# Validate
databricks bundle validate

# Deploy to development
databricks bundle deploy -t dev

# Deploy to production
databricks bundle deploy -t prod
```

## Troubleshooting

### uv Not Found
Ensure uv is in your PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Submodule Empty
```bash
git submodule update --init --recursive
```

### Databricks Auth Failed
1. Check your token hasn't expired
2. Verify the host URL is correct
3. Ensure network access to Databricks

### Python Version Issues
```bash
# Set specific Python version
uv python install 3.11
uv sync
```
