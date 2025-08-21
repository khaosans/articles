#!/usr/bin/env python3
# Auto-generated fix script for broken Mermaid diagrams
# Run this script to attempt automatic fixes

import os
import re
from pathlib import Path

def fix_diagram(file_path):
    """Attempt to fix common issues in Mermaid diagrams"""
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
        content = re.sub(r'\[([^]]*[<>&"'][^]]*)\]', r'[\1]', content)
        
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
        "README_diagram_1.mmd",
        "README_diagram_1_enhanced.mmd",
        "README_diagram_3.mmd",
        "README_diagram_4.mmd",
        "ai-developer_diagram_1.mmd",
        "ai-developer_diagram_1_enhanced.mmd",
        "ai-developer_diagram_2.mmd",
        "ai-developer_diagram_2_enhanced.mmd",
        "ai-developer_diagram_3.mmd",
        "ai-developer_diagram_3_enhanced.mmd",
        "ai-engineer_diagram_1.mmd",
        "ai-engineer_diagram_1_enhanced.mmd",
        "ai-engineer_diagram_2.mmd",
        "ai-engineer_diagram_2_enhanced.mmd",
        "ai-roles-workflows-comprehensive_diagram_1.mmd",
        "ai-roles-workflows-comprehensive_diagram_10.mmd",
        "ai-roles-workflows-comprehensive_diagram_10_enhanced.mmd",
        "ai-roles-workflows-comprehensive_diagram_11.mmd",
        "ai-roles-workflows-comprehensive_diagram_11_enhanced.mmd",
        "ai-roles-workflows-comprehensive_diagram_1_enhanced.mmd",
        "ai-roles-workflows-comprehensive_diagram_2.mmd",
        "ai-roles-workflows-comprehensive_diagram_2_enhanced.mmd",
        "ai-roles-workflows-comprehensive_diagram_3.mmd",
        "ai-roles-workflows-comprehensive_diagram_3_enhanced.mmd",
        "ai-roles-workflows-comprehensive_diagram_4.mmd",
        "ai-roles-workflows-comprehensive_diagram_4_enhanced.mmd",
        "ai-roles-workflows-comprehensive_diagram_5.mmd",
        "ai-roles-workflows-comprehensive_diagram_5_enhanced.mmd",
        "ai-roles-workflows-comprehensive_diagram_6.mmd",
        "ai-roles-workflows-comprehensive_diagram_6_enhanced.mmd",
        "ai-roles-workflows-comprehensive_diagram_7.mmd",
        "ai-roles-workflows-comprehensive_diagram_8.mmd",
        "ai-roles-workflows-comprehensive_diagram_8_enhanced.mmd",
        "ai-roles-workflows-comprehensive_diagram_9.mmd",
        "ai-roles-workflows-comprehensive_diagram_9_enhanced.mmd",
        "cost-optimization_diagram_1.mmd",
        "cost-optimization_diagram_1_enhanced.mmd",
        "data-engineer_diagram_1.mmd",
        "data-engineer_diagram_1_enhanced.mmd",
        "data-engineer_diagram_2.mmd",
        "data-engineer_diagram_2_enhanced.mmd",
        "data-scientist_diagram_1.mmd",
        "data-scientist_diagram_1_enhanced.mmd",
        "data-scientist_diagram_2.mmd",
        "data-scientist_diagram_2_enhanced.mmd",
        "ml-engineer_diagram_1.mmd",
        "ml-engineer_diagram_1_enhanced.mmd",
        "ml-engineer_diagram_2.mmd",
        "ml-engineer_diagram_2_enhanced.mmd",
        "mlops-architecture_diagram_1.mmd",
        "mlops-architecture_diagram_1_enhanced.mmd",
        "mlops-architecture_diagram_2.mmd",
        "mlops-architecture_diagram_2_enhanced.mmd",
        "mlops-architecture_diagram_3.mmd",
        "mlops-architecture_diagram_3_enhanced.mmd",
        "performance-metrics_diagram_1.mmd",
        "performance-metrics_diagram_1_enhanced.mmd",
        "role-template_diagram_1.mmd",
        "role-template_diagram_1_enhanced.mmd",
        "security-guide_diagram_1.mmd",
        "security-guide_diagram_1_enhanced.mmd",
        "security-guide_diagram_2.mmd",
        "security-guide_diagram_2_enhanced.mmd",
        "security-guide_diagram_3.mmd",
        "security-guide_diagram_3_enhanced.mmd",
        "security-guide_diagram_5.mmd",
        "security-guide_diagram_5_enhanced.mmd",
    ]
    
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
    
    print("\n🎉 Fix script completed!")

if __name__ == "__main__":
    main()
