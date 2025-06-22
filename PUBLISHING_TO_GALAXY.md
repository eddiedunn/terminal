# Publishing This Collection to Ansible Galaxy

This guide explains how to prepare, tag, and publish your Ansible collection to Ansible Galaxy so others can install it with `ansible-galaxy` and `collections/requirements.yml`.

---

## 1. Prerequisites
- You have an [Ansible Galaxy](https://galaxy.ansible.com/) account.
- Your collection follows the [Ansible collection structure](https://docs.ansible.com/ansible/latest/dev_guide/collections_galaxy_meta.html).
- Your `galaxy.yml` is correctly filled out (namespace, name, version, etc.).
- You have the [Ansible CLI](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) installed.

---

## 2. Build the Collection
From the root of your collection repo:

```sh
ansible-galaxy collection build
```

This creates a `.tar.gz` file (e.g., `eddiedunn-terminal-1.0.0.tar.gz`).

---

## 3. Tag a Release (Recommended)
Tag your release in git so users and Galaxy can reference a version:

```sh
git tag v1.0.0
git push origin v1.0.0
```
Replace `1.0.0` with your version.

---

## 4. Publish to Galaxy
Upload the built tarball to Galaxy:

1. Go to https://galaxy.ansible.com/my-content/collections/upload
2. Log in and select your namespace.
3. Upload the `.tar.gz` file you built.

Alternatively, use the CLI (if supported):

```sh
ansible-galaxy collection publish eddiedunn-terminal-1.0.0.tar.gz --api-key <your_galaxy_api_key>
```

---

## 5. Verify and Use
After publishing, users can install your collection with:

```yaml
collections:
  - name: eddiedunn.terminal
```

```sh
ansible-galaxy collection install -r collections/requirements.yml
```

---

## 6. Updating the Collection
- Bump the version in `galaxy.yml`.
- Build, tag, and publish again.

---

## References
- [Ansible Galaxy Collection Docs](https://docs.ansible.com/ansible/latest/dev_guide/collections_galaxy_meta.html)
- [Publishing Collections](https://docs.ansible.com/ansible/latest/dev_guide/collections_galaxy.html#publishing-collections)

---

*Last updated: June 2025*
