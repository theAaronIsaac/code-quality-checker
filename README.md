# Code Quality Checker

A Python utility that analyzes repositories for common code quality issues and generates comprehensive reports.

## Overview

This tool scans your codebase to identify potential code quality issues like TODOs, large files, and style violations. It also attempts to collect test coverage information for Python projects. The results are compiled into a nicely formatted Markdown report.

## Features

- Analyzes multiple file types (Python, JavaScript, Java, C/C++, Go, Rust, TypeScript)
- Identifies TODO comments in code
- Flags files that may be too large (over 500 lines)
- Detects style issues (e.g., line length violations in Python)
- Attempts to collect test coverage data for Python projects
- Generates a comprehensive Markdown report

## Requirements

- Python 3.x
- For Python test coverage reporting:
  - `pytest`
  - `coverage`

## Installation

1. Save the script as `code_quality_checker.py`
2. Install required dependencies for test coverage analysis (optional):
   ```
   pip install pytest coverage
   ```

## Usage

Run the script in the repository you want to analyze:

```python
# Analyze current directory
python code_quality_checker.py

# Or specify a path
python code_quality_checker.py /path/to/your/repo
```

Alternatively, import and use in your own Python code:

```python
from code_quality_checker import check_code_quality

# Analyze current directory
check_code_quality()

# Or specify a path
check_code_quality("/path/to/your/repo")
```

## Output

The script generates a file named `CODE_QUALITY_REPORT.md` in the repository root, containing:

- Summary statistics (files analyzed, total line count, test coverage)
- List of TODO comments with file and line references
- List of large files that may need refactoring
- Code style issues with severity ratings

## Supported Languages

The tool currently supports the following file extensions:
- `.py` (Python)
- `.js` (JavaScript)
- `.java` (Java)
- `.c`, `.cpp`, `.h`, `.hpp` (C/C++)
- `.go` (Go)
- `.rs` (Rust)
- `.ts` (TypeScript)

## Customization

You can easily modify the script to:
- Adjust the line limit for "large files" (default: 500 lines)
- Change the maximum line length for Python files (default: 120 characters)
- Add support for additional file extensions
- Implement more language-specific checks

## Limitations

- Test coverage reporting only works for Python projects with pytest and coverage installed
- Style checking is currently limited to line length for Python files
- Binary files or files with encoding issues may be skipped

## Contributing

Feel free to submit issues or pull requests to improve the tool or add more checks!