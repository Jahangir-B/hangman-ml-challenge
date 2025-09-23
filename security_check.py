#!/usr/bin/env python3
"""
Security Check Script for Hangman ML Challenge Repository

This script helps identify potential security issues in the repository.
Run this before committing any changes to ensure the repository remains secure.
"""

import re
import sys
from pathlib import Path

# Patterns that might indicate security issues
SECURITY_PATTERNS = {
    'api_keys': [
        r'api[_-]?key\s*[:=]\s*["\'][^"\']+["\']',
        r'apikey\s*[:=]\s*["\'][^"\']+["\']',
        r'api_key\s*[:=]\s*["\'][^"\']+["\']',
    ],
    'passwords': [
        r'password\s*[:=]\s*["\'][^"\']+["\']',
        r'passwd\s*[:=]\s*["\'][^"\']+["\']',
        r'pwd\s*[:=]\s*["\'][^"\']+["\']',
    ],
    'tokens': [
        r'token\s*[:=]\s*["\'][^"\']+["\']',
        r'access_token\s*[:=]\s*["\'][^"\']+["\']',
        r'auth_token\s*[:=]\s*["\'][^"\']+["\']',
    ],
    'urls_with_credentials': [
        r'https?://[^:]+:[^@]+@[^\s]+',
        r'https?://[a-zA-Z0-9._-]+:[a-zA-Z0-9._-]+@[^\s]+',
    ],
    'railway_urls': [
        r'https?://[^/]*railway[^/]*\.app',
        r'https?://[^/]*\.up\.railway\.app',
    ],
    'secrets': [
        r'secret\s*[:=]\s*["\'][^"\']+["\']',
        r'private_key\s*[:=]\s*["\'][^"\']+["\']',
        r'privatekey\s*[:=]\s*["\'][^"\']+["\']',
    ]
}

# Files to check
FILES_TO_CHECK = ['.py', '.md', '.txt', '.json', '.yaml', '.yml', '.toml', '.cfg', '.ini']

# Files to ignore
IGNORE_FILES = {
    'security_check.py',  # This file itself
    '.gitignore',
    'SECURITY.md',
    'training_words.txt',  # Contains words that might match patterns
    'sample_words.txt',    # Contains words that might match patterns
}

def check_file_security(file_path):
    """Check a single file for security issues"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for category, patterns in SECURITY_PATTERNS.items():
                    for pattern in patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            issues.append({
                                'file': file_path,
                                'line': line_num,
                                'category': category,
                                'content': line.strip(),
                                'pattern': pattern
                            })
    except (IOError, UnicodeDecodeError) as e:
        print(f"Error reading {file_path}: {e}")
    
    return issues

def main():
    """Main security check function"""
    print("Hangman ML Challenge - Security Check")
    print("=" * 50)
    
    issues_found = []
    files_checked = 0
    
    # Check all relevant files
    for file_path in Path('.').rglob('*'):
        if file_path.is_file():
            # Skip ignored files
            if file_path.name in IGNORE_FILES:
                continue
            
            # Skip files in .git directory
            if '.git' in file_path.parts:
                continue
            
            # Check file extension
            if file_path.suffix.lower() in FILES_TO_CHECK:
                files_checked += 1
                issues = check_file_security(file_path)
                issues_found.extend(issues)
    
    # Report results
    print(f"Files checked: {files_checked}")
    print(f"Security issues found: {len(issues_found)}")
    print()
    
    if issues_found:
        print("POTENTIAL SECURITY ISSUES DETECTED:")
        print("-" * 50)
        
        for issue in issues_found:
            print(f"File: {issue['file']}")
            print(f"Line: {issue['line']}")
            print(f"Category: {issue['category']}")
            print(f"Content: {issue['content']}")
            print()
        
        print("SECURITY CHECK FAILED")
        print("Please review and fix these issues before committing.")
        print("Follow security best practices.")
        return 1
    else:
        print("SECURITY CHECK PASSED")
        print("No potential security issues detected.")
        print("Repository is safe to commit.")
        return 0

if __name__ == "__main__":
    sys.exit(main())
