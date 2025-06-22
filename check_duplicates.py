import yaml
import os

def check_file(path):
    with open(path, 'r') as f:
        try:
            docs = list(yaml.compose_all(f))
        except Exception as e:
            print(f'YAML ERROR in {path}: {e}')
            return
    def find_dupes(node, path_stack):
        if isinstance(node, yaml.MappingNode):
            keys = [k.value for k, _ in node.value]
            for k in set(keys):
                if keys.count(k) > 1:
                    print(f'Duplicate key in {path}: {k} at {"->".join(path_stack+[str(k)])}')
            for k, v in node.value:
                find_dupes(v, path_stack+[str(k.value)])
        elif isinstance(node, yaml.SequenceNode):
            for idx, item in enumerate(node.value):
                find_dupes(item, path_stack+[str(idx)])
    for doc in docs:
        find_dupes(doc, [])
for root, dirs, files in os.walk('roles'):
    for file in files:
        if file.endswith('.yml') or file.endswith('.yaml'):
            check_file(os.path.join(root, file))
