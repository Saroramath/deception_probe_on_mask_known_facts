#!/usr/bin/env python3
import os
import re
from pathlib import Path

def fix_html_overflow_properly(html_file):
    """Fix text overflow issues in HTML files with proper CSS"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix malformed inline styles first
    content = re.sub(
        r'style="([^"]*);"; word-wrap: break-word; overflow-wrap: break-word; max-width: 100%; overflow-x: auto;',
        r'style="\1; word-wrap: break-word; overflow-wrap: break-word; max-width: 100%; overflow-x: auto;"',
        content
    )
    
    # Fix malformed CSS rules (missing semicolons before new properties)
    content = re.sub(
        r'(\s+)(word-wrap: break-word; overflow-wrap: break-word;)(\s*)(overflow-x: auto;)(\s*})',
        r'\1\2\3\4\5',
        content
    )
    
    # Add proper CSS for all text containers
    css_fixes = {
        'body': 'word-wrap: break-word; overflow-wrap: break-word;',
        '.container': 'word-wrap: break-word; overflow-wrap: break-word; overflow-x: auto;',
        '.content': 'word-wrap: break-word; overflow-wrap: break-word; overflow-x: auto;',
        '.metadata': 'word-wrap: break-word; overflow-wrap: break-word; overflow-x: auto;',
        '.metadata-item': 'word-wrap: break-word; overflow-wrap: break-word;',
        '.belief-section': 'word-wrap: break-word; overflow-wrap: break-word; overflow-x: auto;',
        '.response-section': 'word-wrap: break-word; overflow-wrap: break-word; overflow-x: auto;',
        '.combined-section': 'word-wrap: break-word; overflow-wrap: break-word; overflow-x: auto;',
        '.section-title': 'word-wrap: break-word; overflow-wrap: break-word;',
        'div': 'word-wrap: break-word; overflow-wrap: break-word;'
    }
    
    # Apply CSS fixes
    for selector, styles in css_fixes.items():
        # Find existing CSS rules and add overflow handling
        pattern = rf'({re.escape(selector)}\s*{{[^}}]*?)(}})'
        
        def add_overflow_styles(match):
            existing_rule = match.group(1)
            closing_brace = match.group(2)
            
            # Check if overflow styles already exist
            if 'word-wrap' not in existing_rule and 'overflow-wrap' not in existing_rule:
                return existing_rule + styles + closing_brace
            return match.group(0)
        
        content = re.sub(pattern, add_overflow_styles, content, flags=re.DOTALL)
    
    # Fix inline styles in div elements
    content = re.sub(
        r'(<div[^>]*style="[^"]*white-space: pre-wrap[^"]*")([^>]*>)',
        r'\1; word-wrap: break-word; overflow-wrap: break-word; max-width: 100%; overflow-x: auto;\2',
        content
    )
    
    # Add a comprehensive CSS rule at the end of the style section
    style_end_pattern = r'(</style>)'
    comprehensive_css = '''
        /* Comprehensive overflow handling */
        * {
            box-sizing: border-box;
        }
        body, div, p, span, pre, code {
            word-wrap: break-word;
            overflow-wrap: break-word;
            max-width: 100%;
        }
        .container, .content, .metadata, .belief-section, .response-section, .combined-section {
            overflow-x: auto;
        }
        pre, code {
            white-space: pre-wrap;
            overflow-x: auto;
        }
    '''
    
    content = re.sub(style_end_pattern, comprehensive_css + r'\1', content)
    
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
        fix_html_overflow_properly(html_path)
    
    print(f"Fixed overflow issues in {len(html_files)} files")

if __name__ == "__main__":
    main()
