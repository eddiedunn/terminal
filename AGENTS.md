# Ansible Collection Contributor Guide

## Development Environment Setup
None. Everything will already be set up for you. There is a user named app user. The idea is that we will run `playbooks/local_setup.yml` using sudo as the user `appuser` we will then check the playbook output as well as the user's home directory to ensure everything is set up correctly.

After verifying your environment, build and install the collection so the playbook has access to required roles and modules. Run:
```
ansible-galaxy collection build . --force
ansible-galaxy collection install ./eddiedunn-terminal-1.0.0.tar.gz --force -p /usr/share/ansible/collections
```
Next, execute the setup playbook as the `appuser` and verify the environment:
```
sudo -u appuser ansible-playbook playbooks/local_setup.yml
./scripts/verify_appuser_terminal_env.sh
```
If the environment has no internet access, expect failures when the playbook tries to download external binaries.


## Testing Guidelines
- Run the test playbook: `ansible-playbook tests/test.yml`
- For module testing, use `ansible-test` commands from the collection root:
  - `ansible-test units` - Run unit tests
  - `ansible-test sanity` - Run sanity tests
  - `ansible-test integration` - Run integration tests (requires test environment)
- Run linting: `ansible-lint`
- Test your changes in a container environment before submitting PRs
- Ensure all tests pass before creating pull requests

## Code Style & Best Practices
- Follow [Ansible coding conventions](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_best_practices.html)
- Document all modules with proper examples in the module's DOCUMENTATION section
- Include return values in the RETURN section of each module
- Add appropriate error handling and meaningful error messages
- Keep modules idempotent where possible
- Use FQCN (Fully Qualified Collection Name) in examples and documentation

## Pull Request Guidelines
- Title format: `[collection_name] Brief description of changes`
- Reference related issues in the PR description using `Fixes #123` or `Related to #123`
- Include test cases for new features or bug fixes
- Update documentation to reflect any changes
- Ensure your code passes all CI/CD pipeline checks- Keep PRs focused on a single feature or bug fix
