# DAB Workflow Template - Codex CLI Instructions

This file provides instructions for OpenAI Codex CLI to work with the Databricks Asset Bundle workflow template.

## Project Overview

This project provides a template for creating, testing, and deploying Databricks workflows using notebooks. It leverages Databricks Asset Bundles (DAB) for infrastructure-as-code workflow management with serverless compute.

## Available Skills

The following skills are available in `.claude/skills/` and can be used by referencing their instructions:

### 1. databricks-asset-bundle

**Purpose**: Generate DAB configurations from notebooks with task dependencies

**When to use**: Setting up Databricks workflows, creating jobs with task dependencies, converting pipelines to DAB

**Key commands**:
```bash
# Generate DAB from text description
scripts/generate_dab.py my_pipeline \
  -d "extract: src/extract.py
      transform: src/transform.py [depends_on: extract]
      load: src/load.py [depends_on: transform]"

# Generate DAB from Mermaid diagram
scripts/generate_dab.py my_pipeline --mermaid-file workflow.mermaid

# Deploy and run
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle run -t dev <job_name>
```

### 2. mermaid-diagrams-creator

**Purpose**: Create workflow visualizations and architecture diagrams

**When to use**: Visualizing workflows, creating architecture diagrams, documenting pipelines

**Key commands**:
```bash
# Check if mermaid CLI is installed
mmdc --version

# Install if needed
npm install -g @mermaid-js/mermaid-cli

# Generate image from mermaid file
mmdc -i diagram.mermaid -o diagram.png -b white
```

**Workflow**:
1. Create `.mermaid` file with diagram content
2. Generate image using `mmdc` command
3. Both source and image files should be created

### 3. pytest-test-creator

**Purpose**: Generate comprehensive unit tests for Python code

**When to use**: Creating tests, setting up pytest, analyzing test coverage

**Key commands**:
```bash
# Install test dependencies
uv add --dev pytest pytest-cov pytest-mock

# Run tests with coverage
uv run pytest --cov=src --cov-report=html --cov-report=term-missing

# Generate test templates
python scripts/generate_tests.py <source_file>
```

**Test patterns**:
- Use `test_<module_name>.py` naming convention
- Include fixtures for common setup
- Add parametrized tests for multiple scenarios
- Test edge cases and error conditions

### 4. python-code-formatter

**Purpose**: Format Python code for consistency

**When to use**: Formatting code, fixing style issues, preparing for CI/CD

**Key commands**:
```bash
# Install formatters
uv add --dev black isort blackbricks ruff

# Format Databricks notebooks
uv run blackbricks <notebook.py>

# Format regular Python files
uv run isort <file.py>
uv run black <file.py>

# Lint and auto-fix
uv run ruff check --fix <file_or_directory>
```

**File type detection**:
- Databricks notebooks: Use `blackbricks` (preserves cell markers)
- Regular Python: Use `isort` + `black`
- All files: Use `ruff` for linting

## Workflow Steps

Follow these steps to create a complete Databricks workflow:

### Step 1: Create Workflow Diagram
Create a Mermaid diagram for your workflow in the order of notebook prefixes (e.g., `01_`, `02_`, `03_`).

### Step 2: Generate Databricks Asset Bundle
Use the databricks-asset-bundle skill to create DAB configuration from the diagram.

### Step 3: Create Unit Tests
Generate and run unit tests for notebook code using pytest.

### Step 4: Format Code
Format all Python code using appropriate formatters (blackbricks for notebooks, black+isort for regular Python).

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

## Configuration

### pyproject.toml
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]

[tool.black]
line-length = 100
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 100

[tool.ruff]
line-length = 100
target-version = "py311"
```

## Notes for Codex CLI

- Read skill files in `.claude/skills/` for detailed instructions
- Use `uv` for Python package management
- Databricks CLI must be configured with workspace profiles
- Always create both `.mermaid` source files AND image files for diagrams
- Use serverless compute by default (Databricks client version 3)
