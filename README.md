# proj2md Usage Guide

## Overview

`proj2md` is a Python script that traverses a given project directory, records its structure, and extracts contents from specified file types into a well-formatted Markdown document named `project_document.md`.
This tool serves a **key purpose**: enabling web-based LLM tools (like ChatGPT, Claude, etc.) to systematically and comprehensively understand the structure and content of your entire project. You can use the generated Markdown document as a prompt input for these LLMs, providing them with a holistic view of your project.

## Directory Structure

The script directory should contain the following two files:

1. **proj2md.py**: The main script.
2. **searching_files.txt**: A text file specifying which file extensions to include and their corresponding code types.

### Example of `searching_files.txt`:

```
*.py(python),*.txt(text),*.c(C),*.md(markdown)
```

Each entry follows the format `*.extension(code_type)`, separated by commas.

## Installation

Ensure you have Python 3 installed on your system. Clone or download the script files (`proj2md.py` and `searching_files.txt`) to your desired directory.

## Usage

Open your terminal or command prompt and navigate to the directory containing `proj2md.py` and `searching_files.txt`.

Run the script using the following command:

```bash
python proj2md.py --proj_path /path/to/project/root
```

### Optional Argument

- `--include_hidden`: Include hidden files and directories (those starting with a dot `.`). By default, hidden files and directories are ignored.

#### Example with Hidden Files Included:

```bash
python proj2md.py --proj_path /path/to/project/root --include_hidden
```

## Output

Upon execution, the script will generate a `project_document.md` file in the specified project root directory. This Markdown document will contain:

1. **Project Name**: The name of the project directory.
2. **Directory Structure**: A tree-like representation of all subdirectories and files.
3. **Specific Content**: Contents of files with extensions specified in `searching_files.txt`, formatted with appropriate code blocks.

## Example

```bash
python proj2md.py --proj_path ~/my_project --include_hidden
```

This command will generate `project_document.md` in the `~/my_project` directory, including all hidden files and directories in the documentation.

## Notes

- Ensure that `searching_files.txt` is correctly formatted to avoid parsing issues.
- The script assumes `searching_files.txt` is located in the same directory as `proj2md.py`.
- The generated Markdown file provides a comprehensive overview of the project structure and key file contents, useful for documentation and review purposes.
