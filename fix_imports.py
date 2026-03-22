import os
import re

# Find all SimObject class definitions and which file they're in
class_to_file = {}
for root, dirs, files in os.walk('src'):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            try:
                content = open(path).read()
                for match in re.finditer(r"^class (\w+)\s*\(", content, re.MULTILINE):
                    class_to_file[match.group(1)] = path
            except:
                pass

# For each .py file, find Param.X references and add missing imports
for root, dirs, files in os.walk('src'):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            try:
                content = open(path).read()
                # Find all Param.X references
                param_types = set(re.findall(r'Param\.([A-Z][a-zA-Z]+)', content))
                if not param_types:
                    continue
                # Find which ones need importing
                new_imports = []
                for ptype in sorted(param_types):
                    if ptype in class_to_file:
                        import_str = 'from m5.objects.%s import *' % os.path.splitext(os.path.basename(class_to_file[ptype]))[0]
                        if import_str not in content:
                            new_imports.append(import_str)
                if new_imports:
                    print("Fixing %s: adding %s" % (path, new_imports))
                    # Insert after last existing 'from m5' import
                    lines = content.split('\n')
                    last_import_idx = 0
                    for i, line in enumerate(lines):
                        if line.startswith('from m5') or line.startswith('import m5'):
                            last_import_idx = i
                    for imp in reversed(new_imports):
                        lines.insert(last_import_idx + 1, imp)
                    open(path, 'w').write('\n'.join(lines))
            except Exception as e:
                print("Error processing %s: %s" % (path, e))

print("Done!")