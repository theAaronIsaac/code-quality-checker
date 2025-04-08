"""
Code Quality Checker - Analyzes repository for common quality issues
"""
import os
import subprocess
from pathlib import Path

def check_code_quality(repo_path="."):
    """
    Runs multiple code quality checks and generates a report
    """
    repo_path = Path(repo_path)
    report = {
        'files_analyzed': 0,
        'total_lines': 0,
        'todo_comments': [],
        'large_files': [],
        'potential_issues': [],
        'test_coverage': None
    }
    
    # Supported file extensions
    code_extensions = {'.py', '.js', '.java', '.c', '.cpp', '.h', '.hpp', '.go', '.rs', '.ts'}
    
    # Analyze each file
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = Path(root) / file
            ext = file_path.suffix.lower()
            
            if ext in code_extensions:
                report['files_analyzed'] += 1
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        report['total_lines'] += len(lines)
                        
                        # Check for TODOs
                        for i, line in enumerate(lines, 1):
                            if 'TODO' in line.upper() and not line.strip().startswith('#'):
                                report['todo_comments'].append({
                                    'file': str(file_path.relative_to(repo_path)),
                                    'line': i,
                                    'comment': line.strip()
                                })
                        
                        # Check for large files
                        if len(lines) > 500:
                            report['large_files'].append({
                                'file': str(file_path.relative_to(repo_path)),
                                'lines': len(lines)
                            })
                        
                        # Simple style checks (example for Python)
                        if ext == '.py':
                            for i, line in enumerate(lines, 1):
                                if len(line) > 120:
                                    report['potential_issues'].append({
                                        'file': str(file_path.relative_to(repo_path)),
                                        'line': i,
                                        'issue': f"Line too long ({len(line)} characters)",
                                        'severity': 'warning'
                                    })
                
                except (UnicodeDecodeError, PermissionError) as e:
                    print(f"Could not read {file_path}: {e}")
    
    # Try to get test coverage (for Python projects)
    try:
        result = subprocess.run(
            ['coverage', 'run', '-m', 'pytest'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            cov_result = subprocess.run(
                ['coverage', 'report'],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            if cov_result.returncode == 0:
                for line in cov_result.stdout.split('\n'):
                    if 'TOTAL' in line:
                        parts = line.split()
                        report['test_coverage'] = parts[-1]
    except FileNotFoundError:
        pass
    
    # Generate markdown report
    report_md = f"""# Code Quality Report

## 📝 Summary
- Files analyzed: {report['files_analyzed']}
- Total lines of code: {report['total_lines']}
- Test coverage: {report['test_coverage'] or 'Not available'}

## 🚨 Potential Issues
"""
    
    if report['todo_comments']:
        report_md += "\n### TODO Comments\n"
        for todo in report['todo_comments']:
            report_md += f"- **{todo['file']}** (line {todo['line']}): `{todo['comment']}`\n"
    
    if report['large_files']:
        report_md += "\n### Large Files (consider splitting)\n"
        for large_file in report['large_files']:
            report_md += f"- **{large_file['file']}**: {large_file['lines']} lines\n"
    
    if report['potential_issues']:
        report_md += "\n### Code Style Issues\n"
        for issue in report['potential_issues']:
            report_md += f"- **{issue['file']}** (line {issue['line']}): {issue['issue']} ({issue['severity']})\n"
    else:
        report_md += "\nNo major code style issues found!\n"
    
    # Write to file
    with open(repo_path / "CODE_QUALITY_REPORT.md", "w") as f:
        f.write(report_md)
    
    print(f"Code quality report generated at {repo_path / 'CODE_QUALITY_REPORT.md'}")

if __name__ == "__main__":
    check_code_quality()