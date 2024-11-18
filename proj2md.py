import argparse
import os
import sys
import re
from pathlib import Path

def parse_searching_files(file_path):
    """
    Parses the searching_files.txt file and returns a dictionary mapping file extensions to code types.
    
    Expected format: *.py(python),*.txt(text),*.c(C),*.md(markdown)
    """
    extension_to_code = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            patterns = content.split(',')
            for pattern in patterns:
                match = re.match(r'\*\.(\w+)\((\w+)\)', pattern.strip())
                if match:
                    ext, code_type = match.groups()
                    extension_to_code[ext] = code_type
                else:
                    print(f"Warning: Unable to parse pattern '{pattern}'. Skipping.")
    except FileNotFoundError:
        print(f"Error: '{file_path}' not found.")
        sys.exit(1)
    return extension_to_code

def generate_directory_tree(root_path, include_hidden):
    """
    Generates the directory tree as a list of strings using DFS traversal.
    
    Parameters:
        root_path (Path): Project root path
        include_hidden (bool): Whether to include hidden files and directories
    """
    tree_lines = []
    root = Path(root_path)
    tree_lines.append(f"{root.name}/")
    
    def dfs(current_path, prefix=""):
        try:
            entries = sorted(current_path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        except PermissionError:
            print(f"Warning: Cannot access directory '{current_path}'. Skipping.")
            return
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            if not include_hidden and entry.name.startswith('.'):
                continue
            connector = "├── " if index < entries_count - 1 else "└── "
            if entry.is_dir():
                tree_lines.append(f"{prefix}{connector}{entry.name}/")
                extension = "│   " if index < entries_count - 1 else "    "
                dfs(entry, prefix + extension)
            else:
                tree_lines.append(f"{prefix}{connector}{entry.name}")
    
    dfs(root)
    return tree_lines

def collect_specific_files(root_path, extension_to_code, include_hidden):
    """
    Collects files that match the specified extensions.
    
    Parameters:
        root_path (Path): Project root path
        extension_to_code (dict): Mapping of extensions to code types
        include_hidden (bool): Whether to include hidden files and directories
    
    Returns:
        list of tuples: (relative_path, code_type, content)
    """
    specific_files = []
    root = Path(root_path)
    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        # Sort to maintain DFS order
        dirnames.sort()
        filenames.sort()
        
        # If not including hidden files/directories, remove hidden directories from dirnames
        if not include_hidden:
            dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        
        for filename in filenames:
            if not include_hidden and filename.startswith('.'):
                continue
            file_path = Path(dirpath) / filename
            rel_path = file_path.relative_to(root)
            ext = file_path.suffix.lstrip('.')
            if ext in extension_to_code:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    specific_files.append((str(rel_path), extension_to_code[ext], content))
                except Exception as e:
                    print(f"Warning: Could not read file '{file_path}'. Error: {e}")
    return specific_files

def write_markdown(proj_root, dir_tree, specific_files, output_path):
    """
    Writes the content to a Markdown file.
    
    Parameters:
        proj_root (Path): Project root path
        dir_tree (list): List of directory structure lines
        specific_files (list): List of specific file contents
        output_path (Path): Path to the output Markdown file
    """
    proj_name = Path(proj_root).name
    with open(output_path, 'w', encoding='utf-8') as md:
        # Title
        md.write(f"# Project: {proj_name}\n\n")
        
        # Directory Structure
        md.write("## Directory Structure\n\n")
        md.write("```\n")
        for line in dir_tree:
            md.write(f"{line}\n")
        md.write("```\n\n")
        md.write("---\n\n")
        
        # Specific Content
        md.write("## Specific Content\n\n")
        for idx, (rel_path, code_type, content) in enumerate(specific_files, 1):
            md.write(f"### {idx}. `{rel_path}`\n\n")
            md.write(f"```{code_type}\n")
            md.write(f"{content}\n")
            md.write("```\n\n")

def main():
    # Argument Parsing
    parser = argparse.ArgumentParser(description="Traverse a project directory and generate a Markdown documentation.")
    parser.add_argument('--proj_path', required=True, help='Path to the project root directory.')
    parser.add_argument('--include_hidden', action='store_true', help='Include hidden files and directories. Ignored by default.')
    args = parser.parse_args()
    
    proj_path = args.proj_path
    include_hidden = args.include_hidden
    proj_root = Path(proj_path)
    
    if not proj_root.exists() or not proj_root.is_dir():
        print(f"Error: The provided project path '{proj_path}' is not a valid directory.")
        sys.exit(1)
    
    # Determine the path to searching_files.txt (assumed to be in the same directory as the script)
    script_dir = Path(__file__).parent
    searching_files_path = script_dir / 'searching_files.txt'
    
    # Parse searching_files.txt
    extension_to_code = parse_searching_files(searching_files_path)
    
    # Generate Directory Tree
    dir_tree = generate_directory_tree(proj_root, include_hidden)
    
    # Collect Specific Files
    specific_files = collect_specific_files(proj_root, extension_to_code, include_hidden)
    
    # Write to Markdown
    output_md = proj_root / 'project_document.md'
    write_markdown(proj_root, dir_tree, specific_files, output_md)
    
    print(f"Markdown documentation has been generated at '{output_md}'.")

if __name__ == "__main__":
    main()
