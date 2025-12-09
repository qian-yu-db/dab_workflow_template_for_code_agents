# DAB Workflow Template for Code Agents

A template for creating, testing, and deploying Databricks workflows using AI code agents. This template leverages Databricks Asset Bundles (DAB) for infrastructure-as-code workflow management with serverless compute.

**Supported AI Code Agents:** Claude Code | OpenAI Codex CLI | Google Gemini CLI

> **Multi-Platform Support**: This template includes platform-specific instruction files (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`) so you can use your preferred AI coding assistant. See [Cross-Platform AI Agent Support](#cross-platform-ai-agent-support) for details.

## Prerequisites

- [Databricks CLI](https://docs.databricks.com/dev-tools/cli/index.html) configured with workspace profiles
- [uv](https://github.com/astral-sh/uv) for Python package management
- One of the supported AI code agents:
  - [Claude Code](https://claude.ai/claude-code) (Anthropic)
  - [Codex CLI](https://github.com/openai/codex) (OpenAI)
  - [Gemini CLI](https://github.com/google/gemini-cli) (Google)

## Project Structure

```
.
├── .claude/
│   ├── skills-repo/          # Git submodule with skill definitions
│   ├── skills/               # Symlinks to active skills
│   └── project-context.md    # Project context for AI agents
├── docs/                     # Project documentation
├── src/                      # Shared Python utilities
├── tests/                    # Test files
├── notebooks/                # Databricks notebooks
├── configs/                  # Configuration files
├── pyproject.toml           # Python project config (uv)
├── CLAUDE.md                # Claude Code instructions
├── AGENTS.md                # Codex CLI instructions
├── GEMINI.md                # Gemini CLI instructions
└── README.md
```

## How to Use This Template with Skills

Follow these steps to create a complete Databricks workflow using AI code agent skills:

### Step 1: Create Workflow Diagram

Use the `mermaid-diagrams-creator` skill to create a workflow diagram based on your notebooks in `@notebooks`. Design your workflow as a linear pipeline in the order of notebook prefixes (e.g., `01_`, `02_`, `03_`).

```
Invoke skill: mermaid-diagrams-creator
```

### Step 2: Generate Databricks Asset Bundle

Use the `databricks-asset-bundle` skill to set up a Databricks Asset Bundle based on the Mermaid diagram from Step 1. Configure it with your target Databricks workspace profile.

```
Invoke skill: databricks-asset-bundle
```

### Step 3: Create Unit Tests

Use the `pytest-test-creator` skill to generate and run unit tests for your notebook code.

```
Invoke skill: pytest-test-creator
```

### Step 4: Format Code

Use the `python-code-formatter` skill to format your notebook code. This uses `blackbricks` for Databricks notebooks and `black`+`isort` for regular Python files.

```
Invoke skill: python-code-formatter
```

### Step 5: Deploy and Run

Validate, deploy, and run the asset bundle on Databricks:

```bash
# Validate the bundle
databricks bundle validate --profile <YOUR_PROFILE> --target dev

# Deploy the bundle
databricks bundle deploy --profile <YOUR_PROFILE> --target dev

# Run the workflow
databricks bundle run --profile <YOUR_PROFILE> --target dev <JOB_NAME>
```

### Step 6: Document

Update the README with documentation about your asset bundle, including the workflow diagram image.

## Available Skills

| Skill | Description |
|-------|-------------|
| `mermaid-diagrams-creator` | Create workflow visualizations and architecture diagrams |
| `databricks-asset-bundle` | Generate DAB configurations from notebooks with task dependencies |
| `pytest-test-creator` | Generate comprehensive unit tests with coverage reports |
| `python-code-formatter` | Format Python code (blackbricks for notebooks, black+isort for Python) |

## Quick Start Example

Here's an example workflow instruction you can give to your AI code agent:

```
1. Use the mermaid-diagrams-creator skill to create a workflow diagram based on the notebooks in @notebooks
2. Use the databricks-asset-bundle skill to set up a Databricks asset bundle based on the diagram
3. Use the pytest-test-creator skill to create and run unit tests on the notebook code
4. Use the python-code-formatter skill to format the notebook code
5. Validate, deploy, and run the asset bundle using databricks CLI
6. Update the README to document the asset bundle with the workflow diagram
```

You can find a working example in the [document_parsing_workflow_example](https://github.com/qian-yu-db/dab_workflow_template_for_code_agents/tree/document_parsing_workflow_example) branch.

## Development Workflow

1. **Visualize**: Create a Mermaid diagram of your workflow
2. **Develop**: Write notebooks in `notebooks/` directory with numbered prefixes
3. **Test**: Generate and run tests with pytest
4. **Format**: Run formatters to ensure code quality
5. **Bundle**: Generate DAB configuration from notebooks
6. **Deploy**: Use `databricks bundle deploy` to deploy to Databricks

## Cross-Platform AI Agent Support

This template supports multiple AI coding assistants with platform-specific instruction files:

| Platform | Instruction File | Description |
|----------|-----------------|-------------|
| Claude Code | `CLAUDE.md` | Instructions for Anthropic's Claude Code CLI |
| Codex CLI | `AGENTS.md` | Instructions for OpenAI's Codex CLI |
| Gemini CLI | `GEMINI.md` | Instructions for Google's Gemini CLI |

All instruction files contain equivalent guidance adapted for each platform's conventions. The skills in `.claude/skills/` work with all platforms as they use standard Python and bash commands.

### Using with Different Agents

**Claude Code:**
```bash
claude  # Skills auto-detected from .claude/skills/
```

**Codex CLI:**
```bash
codex  # Reads AGENTS.md for instructions
```

**Gemini CLI:**
```bash
gemini  # Reads GEMINI.md for instructions
```
