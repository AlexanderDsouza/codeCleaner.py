# HOW TO RUN
# $python codecleaner.py <yourfile.py> <outputfile.py>
# outputfile is optional if you only want to overwrite the current file.
# file must compile properly

import ast
import sys


def remove_unused_imports(code):
    tree = ast.parse(code)
    imports = set()
    used_names = set()

    # Extract imports and used names
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name:
                    imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module
            for alias in node.names:
                if alias.name:
                    imports.add(f"{module}.{alias.name}")
        elif isinstance(node, ast.Name):
            used_names.add(node.id)

    # Identify unused imports
    unused_imports = imports - used_names

    # Filter out lines with unused imports
    cleaned_lines = []
    for line in code.split('\n'):
        if not any(f"import {imp}" in line or f"from {imp}" in line for imp in unused_imports):
            cleaned_lines.append(line)

    # Generate cleaned code
    cleaned_code = '\n'.join(cleaned_lines)
    return cleaned_code


def process_file(input_file_path, output_file_path=None):
    with open(input_file_path, 'r') as file:
        original_code = file.read()

    # Convert tabs to spaces
    cleaned_code = original_code.replace('\t', '    ')

    # Check for tabs in the cleaned code
    if '\t' in cleaned_code:
        print("Error: The cleaned code still contains tabs. Please check your indentation.")
        sys.exit(1)

    cleaned_code = remove_unused_imports(cleaned_code)


    if output_file_path:
        with open(output_file_path, 'w') as file:
            file.write(cleaned_code)
    else:
        with open(input_file_path, 'w') as file:
            file.write(cleaned_code)


if __name__ == "__main__":
    if len(sys.argv) not in [2, 3]:
        print("Usage: python script.py <input_file_path> [<output_file_path>]")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2] if len(sys.argv) == 3 else None

    # If output_file_path is not provided, overwrite the original file
    process_file(input_file_path, output_file_path)