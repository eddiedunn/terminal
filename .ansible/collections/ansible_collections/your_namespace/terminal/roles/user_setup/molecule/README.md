# Molecule Test Scenarios for terminal_setup

This directory contains Molecule scenarios for testing the `terminal_setup` Ansible role with different feature toggle combinations.

## Usage

From the role directory, run:

    molecule test -s <scenario_name>

Or run all scenarios:

    molecule test --all

## Scenarios

-   **`default`**: Verifies the role performs a clean no-op when `terminal_setup_profile_tools` is empty.
-   **`master_disabled`**: Verifies the role performs a clean no-op when `terminal_setup_enabled: false`, even if tools are listed.
-   **`bash_full`**: A comprehensive test with all tools enabled in a **Bash** environment. It verifies all binaries, configuration files, aliases, and Bash-specific completions.
-   **`zsh_full`**: A comprehensive test with all tools enabled in a **Zsh** environment. It verifies all binaries, configuration files, and Zsh-specific initializations (`.zshrc`, `.zshenv`) and completions.
-   **`minimal`**: A "selectivity" test that enables only a few tools (`fzf`, `bat`). It verifies that artifacts for enabled tools are present and artifacts for disabled tools are **absent**.

## Platform

All scenarios use Docker with the `geerlingguy/docker-ubuntu2204-ansible` image by default, which provides a `testuser` with `sudo` access, `bash`, and `zsh`.

## Extending

To test a new feature or combination:
1.  Add a new scenario directory (e.g., `molecule/my_new_test`).
2.  Create `molecule.yml` and a `converge.yml` to define the test conditions.
3.  Add a `verify.yml` with assertions to validate the expected state.

## What Each Scenario Tests

- **default:** All features off; verifies no files/configs are created (no-op)
- **all_enabled:** All features on; verifies all managed files/configs are present
- **starship_only:** Only Starship enabled
- **sheldon_only:** Only Sheldon enabled
- **multiple_combinations:** Example mix of features (Starship, Bat, Zoxide)
- **master_disabled:** All features on but master enable off; verifies no changes

## Extending

Add new scenarios for additional feature combos, destructive reset logic, or idempotency as needed. You can use `verify.yml` or [Testinfra](https://testinfra.readthedocs.io/) for advanced validation.
