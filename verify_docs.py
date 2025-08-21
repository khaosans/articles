#!/usr/bin/env python3
"""
Documentation Verification Script
Verifies all Markdown documents render properly, especially Mermaid diagrams
"""

import os
import re
import subprocess
import sys
from pathlib import Path

def find_markdown_files():
    """Find all Markdown files in the repository"""
    markdown_files = []
    for root, dirs, files in os.walk('.'):
        # Skip .git directory
        if '.git' in root:
            continue
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def extract_mermaid_blocks(content):
    """Extract all Mermaid code blocks from content"""
    mermaid_blocks = []
    pattern = r'```mermaid\s*\n(.*?)\n```'
    matches = re.findall(pattern, content, re.DOTALL)
    return matches

def validate_mermaid_syntax(mermaid_code):
    """Basic Mermaid syntax validation"""
    issues = []
    
    # Check for common Mermaid syntax issues
    lines = mermaid_code.strip().split('\n')
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        # Check for basic graph syntax
        if line.startswith('graph') or line.startswith('flowchart'):
            continue
            
        # Check for other Mermaid diagram types
        if line.startswith('sequenceDiagram') or line.startswith('gantt') or line.startswith('pie') or line.startswith('radar') or line.startswith('stateDiagram') or line.startswith('classDiagram') or line.startswith('mindmap'):
            continue
            
        # Check for node definitions
        if re.match(r'^[A-Za-z0-9_]+\[.*\]', line):
            continue
            
        # Check for connections
        if re.match(r'^[A-Za-z0-9_]+\s*--+>?\s*[A-Za-z0-9_]+', line):
            continue
            
        # Check for style definitions
        if line.startswith('style') or line.startswith('classDef'):
            continue
            
        # Check for subgraph
        if line.startswith('subgraph') or line.startswith('end'):
            continue
            
        # Check for participant definitions
        if line.startswith('participant'):
            continue
            
        # Check for section definitions
        if line.startswith('section'):
            continue
            
        # Check for title definitions
        if line.startswith('title'):
            continue
            
        # Check for dateFormat
        if line.startswith('dateFormat'):
            continue
            
        # Check for state transitions
        if re.match(r'^\[.*\]\s*-->', line):
            continue
            
        # Check for class definitions
        if re.match(r'^class\s+[A-Za-z0-9_]+', line):
            continue
            
        # Check for class relationships
        if re.match(r'^[A-Za-z0-9_]+\s*[|<>-]+\s*[A-Za-z0-9_]+', line):
            continue
            
        # Check for mindmap nodes
        if re.match(r'^[A-Za-z0-9_]+\(\(.*\)\)', line):
            continue
            
        # Check for mindmap text nodes (simple text)
        if re.match(r'^[A-Za-z0-9_\s/]+$', line) and not line.startswith('root'):
            continue
            
        # Check for pie chart data
        if re.match(r'^".*"\s*:\s*\d+', line):
            continue
            
        # Check for radar chart data
        if re.match(r'^".*"\s*:\s*\d+', line):
            continue
            
        # Check for class diagram attributes and methods
        if re.match(r'^\+[A-Za-z0-9_<>~\[\]()]+', line):
            continue
            
        # Check for class diagram stereotypes
        if re.match(r'^<<.*>>', line):
            continue
            
        # Check for class diagram relationships
        if re.match(r'^[A-Za-z0-9_]+\s*[|<>-]+\s*[A-Za-z0-9_]+', line):
            continue
            
        # Check for state diagram transitions
        if re.match(r'^[A-Za-z0-9_]+\s*-->\s*\[.*\]', line):
            continue
            
        # Check for closing braces in class diagrams
        if line.strip() == '}':
            continue
            
        # Check for gantt tasks
        if re.match(r'^[A-Za-z0-9_\s]+\s*:\s*[a-z]+,', line):
            continue
            
        # Check for sequence diagram interactions
        if re.match(r'^[A-Za-z0-9_]+->>?[A-Za-z0-9_]+', line):
            continue
            
        # Check for alt/else blocks
        if line.startswith('alt') or line.startswith('else'):
            continue
            
        # Check for comments
        if line.startswith('%%'):
            continue
            
        # If we get here, the line might be problematic
        if line:
            issues.append(f"Line {i}: Potentially invalid syntax - '{line}'")
    
    return issues

def check_internal_links(content, file_path):
    """Check if internal links are valid"""
    issues = []
    
    # Skip link checking for template files
    if 'template' in file_path.lower():
        return issues
    
    # Find all internal links
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, content)
    
    for link_text, link_url in matches:
        # Skip external links
        if link_url.startswith('http'):
            continue
            
        # Handle relative paths
        if link_url.startswith('./'):
            link_url = link_url[2:]
        elif link_url.startswith('../'):
            # Calculate relative path
            current_dir = os.path.dirname(file_path)
            link_url = os.path.normpath(os.path.join(current_dir, link_url))
        else:
            # Assume relative to current file
            current_dir = os.path.dirname(file_path)
            link_url = os.path.join(current_dir, link_url)
        
        # Check if file exists
        if not os.path.exists(link_url):
            issues.append(f"Broken internal link: '{link_text}' -> '{link_url}'")
    
    return issues

def check_markdown_syntax(content, file_path):
    """Check for common Markdown syntax issues"""
    issues = []
    
    lines = content.split('\n')
    
    in_code_block = False
    code_block_start = None
    
    for i, line in enumerate(lines, 1):
        # Check for code block markers
        if line.strip().startswith('```'):
            if not in_code_block:
                # Starting a code block
                in_code_block = True
                code_block_start = i
            else:
                # Ending a code block
                in_code_block = False
                code_block_start = None
        
        # Check for malformed headers
        if line.startswith('#'):
            if not re.match(r'^#{1,6}\s+', line):
                issues.append(f"Line {i}: Malformed header - '{line}'")
    
    # Check if there's an unclosed code block at the end
    if in_code_block and code_block_start:
        issues.append(f"Line {code_block_start}: Unclosed code block")
    
    return issues

def verify_file(file_path):
    """Verify a single Markdown file"""
    print(f"\n🔍 Verifying: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [f"Error reading file: {e}"]
    
    issues = []
    
    # Check Mermaid diagrams
    mermaid_blocks = extract_mermaid_blocks(content)
    if mermaid_blocks:
        print(f"  📊 Found {len(mermaid_blocks)} Mermaid diagram(s)")
        for i, mermaid_code in enumerate(mermaid_blocks, 1):
            mermaid_issues = validate_mermaid_syntax(mermaid_code)
            if mermaid_issues:
                issues.extend([f"Mermaid diagram {i}: {issue}" for issue in mermaid_issues])
            else:
                print(f"    ✅ Mermaid diagram {i}: Valid syntax")
    
    # Check internal links
    link_issues = check_internal_links(content, file_path)
    if link_issues:
        issues.extend(link_issues)
    else:
        print(f"  🔗 Internal links: Valid")
    
    # Check Markdown syntax
    syntax_issues = check_markdown_syntax(content, file_path)
    if syntax_issues:
        issues.extend(syntax_issues)
    else:
        print(f"  📝 Markdown syntax: Valid")
    
    return issues

def main():
    """Main verification function"""
    print("🚀 Starting Documentation Verification...")
    print("=" * 60)
    
    markdown_files = find_markdown_files()
    print(f"Found {len(markdown_files)} Markdown files")
    
    all_issues = []
    files_with_issues = 0
    
    for file_path in sorted(markdown_files):
        issues = verify_file(file_path)
        if issues:
            files_with_issues += 1
            all_issues.extend([f"{file_path}: {issue}" for issue in issues])
    
    print("\n" + "=" * 60)
    print("📋 VERIFICATION SUMMARY")
    print("=" * 60)
    
    if all_issues:
        print(f"❌ Found {len(all_issues)} issues in {files_with_issues} files:")
        for issue in all_issues:
            print(f"  • {issue}")
        return False
    else:
        print("✅ All documents verified successfully!")
        print(f"  • {len(markdown_files)} files checked")
        print(f"  • All Mermaid diagrams valid")
        print(f"  • All internal links working")
        print(f"  • All Markdown syntax correct")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
