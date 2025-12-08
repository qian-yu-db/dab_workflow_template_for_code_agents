# Requirements: DAB Workflow Template

## Functional Requirements

### Workflow Development
- Create Databricks notebooks with proper structure
- Define task dependencies between notebooks
- Support for parameterized workflows

### Testing
- Unit tests for notebook logic
- Integration tests for workflow execution
- Coverage reporting

### Deployment
- Generate Databricks Asset Bundle configurations
- Support multiple deployment targets (dev, staging, prod)
- Serverless compute configuration

## Technical Requirements

### Environment
- Python 3.11+
- Databricks workspace access
- Databricks CLI installed

### Dependencies

#### Runtime
- `databricks-sdk>=0.73.0`

#### Development
- `pytest>=9.0.2`
- `pytest-cov>=7.0.0`
- `black>=25.12.0`
- `isort>=7.0.0`
- `ruff>=0.14.8`

### Tools Required
- **uv**: Python package manager
- **Databricks CLI**: For bundle deployment
- **Git**: Version control
- **Claude Code**: For skill execution

## Skill-Specific Requirements

### databricks-asset-bundle
- Databricks workspace URL
- Authentication configured (token or OAuth)
- Target cluster or serverless compute

### pytest-test-creator
- Test directory structure (`tests/`)
- pytest configuration in `pyproject.toml`

### python-code-formatter
- `.pre-commit-config.yaml` for hooks
- Formatter configuration in `pyproject.toml`

### mermaid-diagrams-creator
- Mermaid CLI (optional, for PNG/SVG export)
- Diagrams directory (`docs/diagrams/`)

## Setup Instructions

### 1. Clone Repository
```bash
git clone --recurse-submodules <repo-url>
cd dab_workflow_template_for_code_agents
```

### 2. Install Dependencies
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync project dependencies
uv sync
```

### 3. Configure Databricks
```bash
# Configure Databricks CLI
databricks configure

# Or set environment variables
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="your-token"
```

### 4. Verify Setup
```bash
# Run tests
uv run pytest

# Check Databricks connection
databricks auth describe
```

## Testing Requirements

### Unit Tests
- Located in `tests/` directory
- Follow `test_*.py` naming convention
- Use pytest fixtures for common setup

### Coverage
- Minimum 80% coverage target
- Generate HTML reports with `uv run pytest --cov --cov-report=html`

### Pre-commit Hooks
- Formatting checks (black, isort)
- Linting (ruff)
- Type checking (optional)
