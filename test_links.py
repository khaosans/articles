#!/usr/bin/env python3
"""
Link Testing Script
Tests all internal and external links in Markdown documents
"""

import os
import re
import json
import time
import requests
from pathlib import Path
from urllib.parse import urlparse, urljoin

def extract_links_from_markdown(file_path):
    """Extract all links from a Markdown file"""
    links = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all markdown links [text](url)
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        matches = re.findall(link_pattern, content)
        
        for text, url in matches:
            links.append({
                'text': text,
                'url': url,
                'file': str(file_path)
            })
            
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return links

def test_internal_link(link, base_path):
    """Test if an internal link exists"""
    if link.startswith('#'):
        # Anchor link - assume it's valid
        return True, "Anchor link"
    
    if link.startswith('/'):
        # Absolute path from root
        target_path = base_path / link[1:]
    else:
        # Relative path
        target_path = base_path / link
    
    if target_path.exists():
        return True, "File exists"
    else:
        return False, f"File not found: {target_path}"

def test_external_link(url, timeout=5):
    """Test if an external link is accessible"""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        if response.status_code < 400:
            return True, f"Status: {response.status_code}"
        else:
            return False, f"Status: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"Error: {str(e)}"

def main():
    """Main link testing function"""
    print("🔗 Testing links in Markdown files...")
    
    # Find all markdown files
    markdown_files = []
    for root, dirs, files in os.walk('.'):
        if '.git' in root or 'venv' in root:
            continue
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(Path(root) / file)
    
    print(f"Found {len(markdown_files)} Markdown files")
    
    all_links = []
    internal_links = []
    external_links = []
    
    # Extract all links
    for file_path in markdown_files:
        links = extract_links_from_markdown(file_path)
        all_links.extend(links)
    
    print(f"Found {len(all_links)} total links")
    
    # Categorize links
    for link in all_links:
        url = link['url']
        if url.startswith(('http://', 'https://')):
            external_links.append(link)
        else:
            internal_links.append(link)
    
    print(f"Internal links: {len(internal_links)}")
    print(f"External links: {len(external_links)}")
    
    # Test internal links
    internal_results = {'total': len(internal_links), 'passed': 0, 'failed': 0, 'errors': []}
    for link in internal_links:
        is_valid, message = test_internal_link(link['url'], Path(link['file']).parent)
        if is_valid:
            internal_results['passed'] += 1
        else:
            internal_results['failed'] += 1
            internal_results['errors'].append({
                'file': link['file'],
                'url': link['url'],
                'text': link['text'],
                'error': message
            })
    
    # Test external links (sample only to avoid timeouts)
    external_results = {'total': len(external_links), 'passed': 0, 'failed': 0, 'errors': []}
    sample_size = min(10, len(external_links))  # Test only first 10 external links
    for link in external_links[:sample_size]:
        is_valid, message = test_external_link(link['url'])
        if is_valid:
            external_results['passed'] += 1
        else:
            external_results['failed'] += 1
            external_results['errors'].append({
                'file': link['file'],
                'url': link['url'],
                'text': link['text'],
                'error': message
            })
    
    # Save results
    results = {
        'internal': internal_results,
        'external': external_results,
        'summary': {
            'total_links': len(all_links),
            'internal_links': len(internal_links),
            'external_links': len(external_links),
            'tested_external': sample_size
        }
    }
    
    with open('link_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print(f"\n📊 Link Test Results:")
    print(f"Internal links: {internal_results['passed']}/{internal_results['total']} passed")
    print(f"External links: {external_results['passed']}/{sample_size} passed (sampled)")
    
    if internal_results['failed'] > 0:
        print(f"\n❌ Internal link failures:")
        for error in internal_results['errors']:
            print(f"  - {error['file']}: {error['url']} ({error['error']})")
    
    if external_results['failed'] > 0:
        print(f"\n⚠️  External link failures:")
        for error in external_results['errors']:
            print(f"  - {error['file']}: {error['url']} ({error['error']})")
    
    print(f"\n💾 Results saved to link_test_results.json")

if __name__ == "__main__":
    main()
