# Molecule Scenario: tool_installer (default)

This scenario tests the installation of selected tools, their binaries, completions, and shell init snippets using the tool_installer role.

- **converge.yml**: Applies the role with a test set of tools and shells.
- **verify.yml**: Checks for installed binaries, completions, and shell initialization scripts for each enabled tool.

Run tests in the project UV virtual environment and ensure `DOCKER_HOST` is set if using Colima.
