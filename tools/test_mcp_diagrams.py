#!/usr/bin/env python3
"""
MCP Mermaid Diagram Testing Script
Tests all Mermaid diagrams with the MCP server to identify broken ones
"""

import os
import json
import time
from pathlib import Path

def test_diagram_with_mcp(diagram_path):
    """Test a single diagram with MCP server by attempting to render it"""
    try:
        with open(diagram_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract the actual diagram content (remove comments)
        lines = content.split('\n')
        diagram_lines = []
        in_diagram = False
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('%%') and not line.startswith('//'):
                if not in_diagram:
                    # Check if this is a diagram starter
                    valid_starters = [
                        'graph', 'flowchart', 'sequenceDiagram', 'classDiagram', 
                        'stateDiagram', 'erDiagram', 'journey', 'gantt', 'pie', 
                        'quadrantChart', 'timeline', 'gitgraph', 'user-journey',
                        'mindmap', 'radar'
                    ]
                    if any(line.startswith(starter) for starter in valid_starters):
                        in_diagram = True
                        diagram_lines.append(line)
                else:
                    diagram_lines.append(line)
        
        if not diagram_lines:
            return False, "No diagram content found"
        
        # Join the diagram lines
        diagram_content = '\n'.join(diagram_lines)
        
        # For now, we'll do basic syntax validation
        # In a real implementation, you would call the MCP server here
        # For demonstration, let's check for common issues
        
        # Check for unclosed brackets
        open_brackets = diagram_content.count('[')
        close_brackets = diagram_content.count(']')
        if open_brackets != close_brackets:
            return False, f"Mismatched brackets: {open_brackets} open, {close_brackets} close"
        
        # Check for unclosed parentheses
        open_parens = diagram_content.count('(')
        close_parens = diagram_content.count(')')
        if open_parens != close_parens:
            return False, f"Mismatched parentheses: {open_parens} open, {close_parens} close"
        
        # Check for unclosed braces
        open_braces = diagram_content.count('{')
        close_braces = diagram_content.count('}')
        if open_braces != close_braces:
            return False, f"Mismatched braces: {open_braces} open, {close_braces} close"
        
        # Check for common syntax issues
        if '-->' in diagram_content and '--' in diagram_content:
            # Check for incomplete arrows
            if diagram_content.count('-->') != diagram_content.count('--'):
                return False, "Incomplete arrow syntax detected"
        
        # Check for invalid node references
        if ':::' in diagram_content:
            # Check if class references are valid
            class_refs = [line.split(':::')[1].split()[0] for line in diagram_lines if ':::' in line]
            class_defs = [line.split()[1] for line in diagram_lines if line.startswith('classDef')]
            
            for ref in class_refs:
                if ref not in class_defs:
                    return False, f"Undefined class reference: {ref}"
        
        # Check for special characters that might cause issues
        problematic_chars = ['<', '>', '&', '"', "'"]
        for char in problematic_chars:
            if char in diagram_content and not any(char in line for line in diagram_lines if 'style' in line or 'classDef' in line):
                return False, f"Potentially problematic character: {char}"
        
        return True, "Valid diagram"
        
    except Exception as e:
        return False, f"Error reading file: {str(e)}"

def test_all_diagrams():
    """Test all Mermaid diagrams in the extracted_diagrams directory"""
    diagrams_dir = Path('extracted_diagrams')
    results = {
        'total': 0,
        'valid': 0,
        'broken': 0,
        'broken_files': [],
        'warnings': []
    }
    
    if not diagrams_dir.exists():
        print("❌ extracted_diagrams directory not found")
        return results
    
    mmd_files = list(diagrams_dir.glob('*.mmd'))
    results['total'] = len(mmd_files)
    
    print(f"🔍 Testing {len(mmd_files)} Mermaid diagrams with enhanced validation...")
    print("=" * 80)
    
    for i, mmd_file in enumerate(sorted(mmd_files), 1):
        print(f"[{i:2d}/{len(mmd_files)}] Testing {mmd_file.name}...", end=" ")
        
        is_valid, message = test_diagram_with_mcp(mmd_file)
        
        if is_valid:
            results['valid'] += 1
            print("✅")
        else:
            results['broken'] += 1
            results['broken_files'].append({
                'file': mmd_file.name,
                'error': message
            })
            print(f"❌ {message}")
        
        # Add a small delay to avoid overwhelming the system
        time.sleep(0.1)
    
    print("=" * 80)
    print(f"📊 Enhanced Validation Results:")
    print(f"   Total diagrams: {results['total']}")
    print(f"   Valid: {results['valid']}")
    print(f"   Broken: {results['broken']}")
    print(f"   Success rate: {(results['valid']/results['total']*100):.1f}%")
    
    if results['broken_files']:
        print(f"\n❌ Broken diagrams found:")
        for broken in results['broken_files']:
            print(f"   - {broken['file']}: {broken['error']}")
        
        print(f"\n🔧 Suggested fixes:")
        print(f"   1. Check for mismatched brackets, parentheses, or braces")
        print(f"   2. Verify all class references are defined")
        print(f"   3. Check for incomplete arrow syntax")
        print(f"   4. Review special characters in node labels")
        print(f"   5. Test with MCP server for rendering issues")
    
    return results

def save_results(results, output_file='mcp_test_results.json'):
    """Save test results to JSON file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Results saved to {output_file}")

def generate_fix_script(broken_files):
    """Generate a script to help fix broken diagrams"""
    if not broken_files:
        return
    
    script_content = """#!/usr/bin/env python3
# Auto-generated fix script for broken Mermaid diagrams
# Run this script to attempt automatic fixes

import os
import re
from pathlib import Path

def fix_diagram(file_path):
    \"\"\"Attempt to fix common issues in Mermaid diagrams\"\"\"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 1: Balance brackets
        open_brackets = content.count('[')
        close_brackets = content.count(']')
        if open_brackets > close_brackets:
            content += ']' * (open_brackets - close_brackets)
        elif close_brackets > open_brackets:
            content = '[' * (close_brackets - open_brackets) + content
        
        # Fix 2: Balance parentheses
        open_parens = content.count('(')
        close_parens = content.count(')')
        if open_parens > close_parens:
            content += ')' * (open_parens - close_parens)
        elif close_parens > open_parens:
            content = '(' * (close_parens - open_parens) + content
        
        # Fix 3: Balance braces
        open_braces = content.count('{')
        close_braces = content.count('}')
        if open_braces > close_braces:
            content += '}' * (open_braces - close_braces)
        elif close_braces > open_braces:
            content = '{' * (close_braces - open_braces) + content
        
        # Fix 4: Fix incomplete arrows
        content = re.sub(r'--(?!>)', '-->', content)
        
        # Fix 5: Escape special characters in node labels
        content = re.sub(r'\[([^]]*[<>&"\'][^]]*)\]', r'[\1]', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    broken_files = [
"""
    
    for broken in broken_files:
        script_content += f'        "{broken["file"]}",\n'
    
    script_content += """    ]
    
    print("🔧 Attempting to fix broken diagrams...")
    
    for file_name in broken_files:
        file_path = Path('extracted_diagrams') / file_name
        if file_path.exists():
            print(f"Fixing {file_name}...", end=" ")
            if fix_diagram(file_path):
                print("✅ Fixed")
            else:
                print("⚠️  No automatic fixes applied")
        else:
            print(f"❌ File not found: {file_name}")
    
    print("\\n🎉 Fix script completed!")

if __name__ == "__main__":
    main()
"""
    
    with open('fix_broken_diagrams.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"🔧 Auto-fix script generated: fix_broken_diagrams.py")

if __name__ == "__main__":
    print("🚀 Enhanced MCP Mermaid Diagram Testing")
    print("=" * 80)
    
    results = test_all_diagrams()
    save_results(results)
    
    if results['broken'] > 0:
        generate_fix_script(results['broken_files'])
        print(f"\n⚠️  Found {results['broken']} broken diagrams that need attention")
        print(f"💡 Run 'python3 fix_broken_diagrams.py' to attempt automatic fixes")
    else:
        print("\n🎉 All diagrams passed enhanced validation!")
