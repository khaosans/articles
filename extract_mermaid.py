#!/usr/bin/env python3
"""
Mermaid Diagram Extraction Script
Extracts all Mermaid diagrams from Markdown files for testing
"""

import os
import re
import json
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

def extract_mermaid_blocks(content, file_path):
    """Extract all Mermaid code blocks from content"""
    mermaid_blocks = []
    pattern = r'```mermaid\s*\n(.*?)\n```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for i, match in enumerate(matches):
        mermaid_blocks.append({
            'content': match.strip(),
            'file': file_path,
            'index': i + 1,
            'filename': f"{Path(file_path).stem}_diagram_{i+1}.mmd"
        })
    
    return mermaid_blocks

def create_puppeteer_config():
    """Create Puppeteer configuration for headless Chrome"""
    config = {
        "args": [
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-accelerated-2d-canvas",
            "--no-first-run",
            "--no-zygote",
            "--single-process",
            "--disable-gpu"
        ]
    }
    
    os.makedirs('extracted_diagrams', exist_ok=True)
    with open('extracted_diagrams/puppeteer.config.json', 'w') as f:
        json.dump(config, f, indent=2)

def main():
    """Main extraction function"""
    print("🔍 Extracting Mermaid diagrams...")
    
    # Create output directory
    os.makedirs('extracted_diagrams', exist_ok=True)
    
    # Create Puppeteer config
    create_puppeteer_config()
    
    markdown_files = find_markdown_files()
    all_diagrams = []
    
    for file_path in markdown_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            diagrams = extract_mermaid_blocks(content, file_path)
            all_diagrams.extend(diagrams)
            
            if diagrams:
                print(f"📊 Found {len(diagrams)} diagram(s) in {file_path}")
        
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    # Save each diagram to a separate file
    for diagram in all_diagrams:
        diagram_path = os.path.join('extracted_diagrams', diagram['filename'])
        
        try:
            with open(diagram_path, 'w', encoding='utf-8') as f:
                f.write(diagram['content'])
            print(f"💾 Saved: {diagram['filename']}")
        
        except Exception as e:
            print(f"❌ Error saving {diagram['filename']}: {e}")
    
    # Create summary report
    summary = {
        'total_files': len(markdown_files),
        'total_diagrams': len(all_diagrams),
        'diagrams_by_file': {}
    }
    
    for diagram in all_diagrams:
        file_path = diagram['file']
        if file_path not in summary['diagrams_by_file']:
            summary['diagrams_by_file'][file_path] = 0
        summary['diagrams_by_file'][file_path] += 1
    
    with open('extracted_diagrams/summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n✅ Extraction complete!")
    print(f"📁 Total files processed: {summary['total_files']}")
    print(f"📊 Total diagrams extracted: {summary['total_diagrams']}")
    
    if summary['total_diagrams'] == 0:
        print("⚠️  No Mermaid diagrams found!")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
