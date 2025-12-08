# Project Context: DAB Workflow Template

## Project Overview
This project provides a template for creating, testing, and deploying Databricks workflows using notebooks. It leverages Databricks Asset Bundles (DAB) for infrastructure-as-code workflow management with serverless compute.

## Selected Skills

### 1. databricks-asset-bundle
- **Purpose**: Generate DAB configurations from notebooks with task dependencies
- **Usage**: Create workflow YAML files, job definitions, and bundle configurations
- **Supports**: Text descriptions, Mermaid diagrams, and workflow diagram images as input

### 2. pytest-test-creator
- **Purpose**: Generate comprehensive unit tests for Python code
- **Usage**: Create tests for notebooks and utility functions with coverage reports

### 3. python-code-formatter
- **Purpose**: Format Python code for consistency
- **Usage**: Uses blackbricks for Databricks notebooks, black+isort for regular Python files

### 4. mermaid-diagrams-creator
- **Purpose**: Create workflow visualizations and architecture diagrams
- **Usage**: Design workflows visually before generating DAB configurations

## Skill Integration Points

1. **Design Phase**: Use `mermaid-diagrams-creator` to visualize workflow architecture
2. **Development Phase**: Create notebooks in `notebooks/` directory
3. **Testing Phase**: Use `pytest-test-creator` to generate and run tests
4. **Formatting Phase**: Use `python-code-formatter` to ensure code quality
5. **Deployment Phase**: Use `databricks-asset-bundle` to generate DAB from notebooks/diagrams

## Development Workflow

1. **Visualize**: Create a Mermaid diagram of your workflow
2. **Develop**: Write notebooks in `notebooks/` directory
3. **Test**: Generate and run tests with pytest
4. **Format**: Run formatters to ensure code quality
5. **Bundle**: Generate DAB configuration from notebooks
6. **Deploy**: Use `databricks bundle deploy` to deploy to Databricks

## Directory Structure
```
.
├── .claude/
│   ├── skills-repo/          # Git submodule with skill definitions
│   ├── skills/               # Symlinks to active skills
│   └── project-context.md    # This file
├── docs/                     # Project documentation
├── src/                      # Shared Python utilities
├── tests/                    # Test files
├── notebooks/                # Databricks notebooks
├── configs/                  # Configuration files
├── pyproject.toml           # Python project config (uv)
└── README.md
```
