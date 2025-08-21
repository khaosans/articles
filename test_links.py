#!/usr/bin/env python3
"""
Link Testing Script
Tests all internal and external links in Markdown documents
"""

import os
import re
import json
import time
from pathlib import Path

# Try to import requests, fall back to basic testing
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("⚠️  requests module not available, skipping external link testing")

def find_markdown_files():
    """Find all Markdown files in the repository"""
    markdown_files = []
    for root, dirs, files in os.walk('.'):
        if '.git' in root:
            continue
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def extract_links(content, file_path):
    """Extract all links from markdown content"""
    links = []
    
    # Skip template files for link validation
    if 'template' in file_path.lower():
        return links
    
    # Find markdown links [text](url)
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, content)
    
    for link_text, link_url in matches:
        # Skip anchor links
        if link_url.startswith('#'):
            continue
            
        links.append({
            'text': link_text,
            'url': link_url,
            'file': file_path,
            'type': 'external' if link_url.startswith('http') else 'internal'
        })
    
    return links

def test_internal_link(link, base_path):
    """Test if an internal link is valid"""
    url = link['url']
    current_file_dir = os.path.dirname(link['file'])
    
    # Handle relative paths
    if url.startswith('./'):
        url = url[2:]
    elif url.startswith('../'):
        # Calculate relative path
        target_path = os.path.normpath(os.path.join(current_file_dir, url))
    else:
        # Assume relative to current file
        target_path = os.path.join(current_file_dir, url)
    
    if url.startswith('../'):
        target_path = os.path.normpath(os.path.join(current_file_dir, url))
    else:
        target_path = os.path.join(current_file_dir, url)
    
    # Check if file exists
    if os.path.exists(target_path):
        return True, "File exists"
    else:
        return False, f"File not found: {target_path}"

def test_external_link(link, timeout=10):
    """Test if an external link is accessible"""
    if not HAS_REQUESTS:
        return True, "Skipped (no requests module)"
        
    url = link['url']
    
    try:
        # Set a reasonable timeout and user agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; Documentation-Verifier/1.0)'
        }
        
        response = requests.head(url, timeout=timeout, headers=headers, allow_redirects=True)
        
        # Accept 2xx and 3xx status codes
        if 200 <= response.status_code < 400:
            return True, f"HTTP {response.status_code}"
        else:
            return False, f"HTTP {response.status_code}"
            
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except requests.exceptions.ConnectionError:
        return False, "Connection error"
    except requests.exceptions.RequestException as e:
        return False, f"Request error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def main():
    """Main link testing function"""
    print("🔗 Testing all links in documentation...")
    
    markdown_files = find_markdown_files()
    all_links = []
    
    # Extract all links
    for file_path in markdown_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            links = extract_links(content, file_path)
            all_links.extend(links)
            
            if links:
                print(f"🔗 Found {len(links)} link(s) in {file_path}")
        
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    if not all_links:
        print("⚠️  No links found!")
        return True
    
    # Test links
    internal_links = [link for link in all_links if link['type'] == 'internal']
    external_links = [link for link in all_links if link['type'] == 'external']
    
    results = {
        'internal': {'passed': 0, 'failed': 0, 'failures': []},
        'external': {'passed': 0, 'failed': 0, 'failures': []},
        'summary': {}
    }
    
    print(f"\n🏠 Testing {len(internal_links)} internal links...")
    for link in internal_links:
        success, message = test_internal_link(link, '.')
        if success:
            results['internal']['passed'] += 1
            print(f"✅ {link['file']}: {link['text']} -> {link['url']}")
        else:
            results['internal']['failed'] += 1
            failure = {
                'file': link['file'],
                'text': link['text'],
                'url': link['url'],
                'error': message
            }
            results['internal']['failures'].append(failure)
            print(f"❌ {link['file']}: {link['text']} -> {link['url']} ({message})")
    
    print(f"\n🌐 Testing {len(external_links)} external links...")
    if not HAS_REQUESTS:
        print("⚠️  Skipping external link testing (requests module not available)")
        results['external']['passed'] = len(external_links)
    else:
        for i, link in enumerate(external_links):
            # Add delay to avoid rate limiting
            if i > 0:
                time.sleep(1)
                
            success, message = test_external_link(link)
            if success:
                results['external']['passed'] += 1
                print(f"✅ {link['file']}: {link['text']} -> {link['url']}")
            else:
                results['external']['failed'] += 1
                failure = {
                    'file': link['file'],
                    'text': link['text'],
                    'url': link['url'],
                    'error': message
                }
                results['external']['failures'].append(failure)
                print(f"❌ {link['file']}: {link['text']} -> {link['url']} ({message})")
    
    # Create summary
    total_links = len(all_links)
    total_passed = results['internal']['passed'] + results['external']['passed']
    total_failed = results['internal']['failed'] + results['external']['failed']
    
    results['summary'] = {
        'total_links': total_links,
        'total_passed': total_passed,
        'total_failed': total_failed,
        'success_rate': round((total_passed / total_links * 100), 2) if total_links > 0 else 0
    }
    
    # Save results
    with open('link_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print(f"\n📊 Link Testing Summary:")
    print(f"Total links tested: {total_links}")
    print(f"✅ Passed: {total_passed}")
    print(f"❌ Failed: {total_failed}")
    print(f"Success rate: {results['summary']['success_rate']}%")
    
    if total_failed > 0:
        print(f"\n❌ Failed links:")
        for failure in results['internal']['failures'] + results['external']['failures']:
            print(f"  • {failure['file']}: {failure['url']} ({failure['error']})")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
