#!/usr/bin/env python3
# Quick fix script for failed Mermaid diagrams
# Generated automatically from fast MCP test results

import re
from pathlib import Path

def quick_fix_diagram(file_path):
    """Apply quick fixes to common Mermaid issues"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixed = False
        
        # Fix 1: Balance brackets
        open_brackets = content.count('[')
        close_brackets = content.count(']')
        if open_brackets > close_brackets:
            content += ']' * (open_brackets - close_brackets)
            fixed = True
        elif close_brackets > open_brackets:
            content = '[' * (close_brackets - open_brackets) + content
            fixed = True
        
        # Fix 2: Balance parentheses
        open_parens = content.count('(')
        close_parens = content.count(')')
        if open_parens > close_parens:
            content += ')' * (open_parens - close_parens)
            fixed = True
        elif close_parens > open_parens:
            content = '(' * (close_parens - open_parens) + content
            fixed = True
        
        # Fix 3: Balance braces
        open_braces = content.count('{')
        close_braces = content.count('}')
        if open_braces > close_braces:
            content += '}' * (open_braces - close_braces)
            fixed = True
        elif close_braces > open_braces:
            content = '{' * (close_braces - open_braces) + content
            fixed = True
        
        # Fix 4: Fix incomplete arrows
        if '--' in content and '-->' in content:
            content = re.sub(r'--(?!>)', '-->', content)
            fixed = True
        
        if fixed and content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    failed_files = [
        "README_diagram_1_enhanced.mmd",
        "README_diagram_1.mmd",
        "ai-developer_diagram_1_enhanced.mmd",
        "README_diagram_3.mmd",
        "ai-developer_diagram_2_enhanced.mmd",
        "ai-engineer_diagram_1.mmd",
        "ai-roles-workflows-comprehensive_diagram_10.mmd",
        "ai-engineer_diagram_2_enhanced.mmd",
        "ai-roles-workflows-comprehensive_diagram_11.mmd",
        "ai-engineer_diagram_2.mmd",
        "ai-engineer_diagram_1_enhanced.mmd",
        "ai-roles-workflows-comprehensive_diagram_1_enhanced.mmd",
        "ai-roles-workflows-comprehensive_diagram_11_enhanced.mmd",
        "ai-roles-workflows-comprehensive_diagram_2_enhanced.mmd",
        "ai-roles-workflows-comprehensive_diagram_2.mmd",
        "ai-roles-workflows-comprehensive_diagram_4_enhanced.mmd",
        "ai-roles-workflows-comprehensive_diagram_5_enhanced.mmd",
        "ai-roles-workflows-comprehensive_diagram_6.mmd",
        "ai-roles-workflows-comprehensive_diagram_6_enhanced.mmd",
        "ai-roles-workflows-comprehensive_diagram_8.mmd",
        "data-engineer_diagram_2.mmd",
        "data-engineer_diagram_2_enhanced.mmd",
        "cost-optimization_diagram_1_enhanced.mmd",
        "data-engineer_diagram_1_enhanced.mmd",
        "ml-engineer_diagram_1.mmd",
        "ml-engineer_diagram_2.mmd",
        "data-scientist_diagram_2.mmd",
        "data-engineer_diagram_1.mmd",
        "ml-engineer_diagram_1_enhanced.mmd",
        "data-scientist_diagram_2_enhanced.mmd",
        "ml-engineer_diagram_2_enhanced.mmd",
        "data-scientist_diagram_1_enhanced.mmd",
        "mlops-architecture_diagram_1_enhanced.mmd",
        "performance-metrics_diagram_1_enhanced.mmd",
        "mlops-architecture_diagram_3_enhanced.mmd",
        "security-guide_diagram_2_enhanced.mmd",
        "role-template_diagram_1_enhanced.mmd",
        "security-guide_diagram_3_enhanced.mmd",
        "security-guide_diagram_1_enhanced.mmd",
        "mlops-architecture_diagram_2_enhanced.mmd",
        "security-guide_diagram_5_enhanced.mmd",
    ]
    
    print("🔧 Applying quick fixes to failed diagrams...")
    
    fixed_count = 0
    for file_name in failed_files:
        file_path = Path('extracted_diagrams') / file_name
        if file_path.exists():
            print(f"Fixing {file_name}...", end=" ")
            if quick_fix_diagram(file_path):
                print("✅ Fixed")
                fixed_count += 1
            else:
                print("⚠️  No automatic fixes applied")
        else:
            print(f"❌ File not found: {file_name}")
    
    print(f"\n🎉 Fixed {fixed_count} out of {len(failed_files)} diagrams!")

if __name__ == "__main__":
    main()
