# Project Plan: DAB Workflow Template

## 1. Project Overview

- **Goal**: Provide a streamlined workflow for creating Databricks notebooks and deploying them as workflows using Databricks Asset Bundles
- **Deliverables**:
  - Template project structure for DAB-based workflows
  - Integrated skills for visualization, testing, and formatting
  - Documentation for workflow development process

## 2. Architecture

### Components
- **Notebooks**: Databricks notebooks containing workflow logic
- **DAB Configuration**: YAML files defining jobs, tasks, and dependencies
- **Shared Utilities**: Python modules in `src/` for reusable code
- **Tests**: Unit tests for notebooks and utilities

### Data Flow
1. User creates notebooks in `notebooks/` directory
2. Optional: Create Mermaid diagram to visualize workflow
3. Generate DAB configuration using `databricks-asset-bundle` skill
4. Deploy using `databricks bundle deploy`

### Integration Points
- Mermaid diagrams can be converted to DAB configurations
- Notebooks can have task dependencies defined in DAB
- Tests validate notebook logic before deployment

## 3. Development Phases

### Phase 1: Setup & Foundation
- [x] Initialize project structure
- [x] Set up uv for Python dependency management
- [x] Configure skills (databricks-asset-bundle, pytest, formatter, mermaid)
- [x] Create documentation templates

### Phase 2: Notebook Development
- [ ] Create notebooks in `notebooks/` directory
- [ ] Define shared utilities in `src/` if needed
- [ ] Visualize workflow with Mermaid diagrams (optional)

### Phase 3: Testing & Validation
- [ ] Generate tests using pytest-test-creator skill
- [ ] Run tests with `uv run pytest`
- [ ] Format code with python-code-formatter skill

### Phase 4: Bundle & Deployment
- [ ] Generate DAB configuration using databricks-asset-bundle skill
- [ ] Validate bundle with `databricks bundle validate`
- [ ] Deploy to target environment with `databricks bundle deploy`

## 4. Skills Utilized

### databricks-asset-bundle
- **Purpose**: Generate Databricks Asset Bundle configurations
- **Usage**: Create workflow definitions from notebooks with task dependencies
- **Deliverables**: `databricks.yml`, job configurations, resource definitions

### pytest-test-creator
- **Purpose**: Generate comprehensive unit tests
- **Usage**: Automatically create tests for Python code and notebooks
- **Deliverables**: Test files in `tests/`, coverage reports

### python-code-formatter
- **Purpose**: Ensure consistent code formatting
- **Usage**: Format notebooks with blackbricks, Python files with black/isort
- **Deliverables**: Formatted code, pre-commit configuration

### mermaid-diagrams-creator
- **Purpose**: Visualize workflow architecture
- **Usage**: Create flowcharts and sequence diagrams for workflows
- **Deliverables**: Mermaid diagram files, PNG/SVG exports

## 5. Dependencies

### Python Dependencies
- `databricks-sdk`: Databricks API interactions
- `pytest`, `pytest-cov`: Testing framework
- `black`, `isort`, `ruff`: Code formatting and linting

### External Tools
- Databricks CLI (for bundle deployment)
- uv (Python package manager)
- Git (version control)

## 6. Success Criteria

- [ ] Notebooks can be developed and tested locally
- [ ] DAB configuration successfully generates from notebooks
- [ ] Workflows deploy and run on Databricks
- [ ] Tests achieve adequate coverage
- [ ] Code passes formatting checks
