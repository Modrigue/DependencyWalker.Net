import os
import re
import sys

# Path to AssemblyInfo.cs (relative to repo root)
ASSEMBLY_INFO_GUI_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'DependencyWalker', 'Properties', 'AssemblyInfo.cs')
ASSEMBLY_INFO_CLI_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'DependencyWalker.Net.Cli', 'Properties', 'AssemblyInfo.cs')

# Get the tag from environment variable set by GitHub Actions (GITHUB_REF or GITHUB_TAG)
GITHUB_REF = os.environ.get('GITHUB_REF', '')

def get_tag_from_ref(ref):
    # GitHub ref format: refs/tags/1.2.3.4
    if ref.startswith('refs/tags/'):
        return ref[len('refs/tags/'):]
    
    return None

def update_assembly_version(filename, tag):
    pattern = re.compile(r'Version\(".*"\)')
    replacement = f'Version("{tag}")'

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace version lines
    new_content, count = pattern.subn(replacement, content)
    if count > 0 and new_content != content:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename} AssemblyVersion to {tag}")

def main():
    tag = get_tag_from_ref(GITHUB_REF)
    if not tag:
        return
    
    update_assembly_version(ASSEMBLY_INFO_GUI_PATH, tag)
    update_assembly_version(ASSEMBLY_INFO_CLI_PATH, tag)

if __name__ == '__main__':
    main() 