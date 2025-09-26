#!/usr/bin/env python3
import os
import re
from pathlib import Path

def fix_html_overflow(html_file):
    """Fix text overflow issues in HTML files"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add overflow handling to existing CSS classes
    overflow_fixes = {
        '.metadata': 'word-wrap: break-word; overflow-wrap: break-word;',
        '.metadata-item': 'word-wrap: break-word; overflow-wrap: break-word;',
        '.belief-section': 'word-wrap: break-word; overflow-wrap: break-word; overflow-x: auto;',
        '.response-section': 'word-wrap: break-word; overflow-wrap: break-word; overflow-x: auto;',
        '.combined-section': 'word-wrap: break-word; overflow-wrap: break-word; overflow-x: auto;',
        '.section-title': 'word-wrap: break-word; overflow-wrap: break-word;',
        'pre, code': 'white-space: pre-wrap; word-wrap: break-word; overflow-wrap: break-word; max-width: 100%; overflow-x: auto;'
    }
    
    # Apply fixes to each CSS class
    for selector, styles in overflow_fixes.items():
        # Find the CSS rule for this selector
        pattern = rf'({re.escape(selector)}\s*{{[^}}]*?)(}})'
        
        def add_styles(match):
            existing_rule = match.group(1)
            closing_brace = match.group(2)
            
            # Check if styles already exist to avoid duplicates
            if 'word-wrap' not in existing_rule:
                return existing_rule + styles + closing_brace
            return match.group(0)
        
        content = re.sub(pattern, add_styles, content, flags=re.DOTALL)
    
    # Also fix inline styles in div elements
    content = re.sub(
        r'(<div[^>]*style="[^"]*white-space: pre-wrap[^"]*")([^>]*>)',
        r'\1; word-wrap: break-word; overflow-wrap: break-word; max-width: 100%; overflow-x: auto;\2',
        content
    )
    
    # Write the fixed content back
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed overflow in {html_file}")

def main():
    probe_results_dir = 'probe_results'
    
    if not os.path.exists(probe_results_dir):
        print(f"Directory {probe_results_dir} not found")
        return
    
    html_files = [f for f in os.listdir(probe_results_dir) if f.endswith('.html')]
    
    print(f"Found {len(html_files)} HTML files in {probe_results_dir}")
    
    for html_file in html_files:
        html_path = os.path.join(probe_results_dir, html_file)
        fix_html_overflow(html_path)
    
    print(f"Fixed overflow issues in {len(html_files)} files")

if __name__ == "__main__":
    main()
