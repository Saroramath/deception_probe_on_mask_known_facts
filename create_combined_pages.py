#!/usr/bin/env python3
import os
import re
from pathlib import Path

def extract_content_from_html(html_file):
    """Extract the main content from an HTML file, fixing overflow issues"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the title
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1) if title_match else "Unknown"
    
    # Extract the header content
    header_match = re.search(r'<div class="header">(.*?)</div>', content, re.DOTALL)
    header = header_match.group(1) if header_match else ""
    
    # Extract the main content (everything inside the content div)
    content_match = re.search(r'<div class="content">(.*?)</div>\s*</div>\s*</body>', content, re.DOTALL)
    main_content = content_match.group(1) if content_match else ""
    
    return title, header, main_content

def create_combined_page(folder_name, folder_path, output_file):
    """Create a combined page for all HTML files in a folder"""
    html_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.html')])
    
    # Start building the combined HTML
    combined_html = f'''<!DOCTYPE html>
<html>
<head>
    <title>{folder_name.replace('_', ' ').title()} - Combined Analysis</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            line-height: 1.6;
        }}
        .main-container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .main-header {{
            background: #2c3e50;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .main-header h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .main-header p {{
            margin: 10px 0 0 0;
            font-size: 1.2em;
            opacity: 0.9;
        }}
        .navigation {{
            background: #34495e;
            padding: 15px;
            text-align: center;
        }}
        .nav-link {{
            color: white;
            text-decoration: none;
            margin: 0 20px;
            padding: 8px 16px;
            border-radius: 4px;
            transition: background-color 0.3s;
        }}
        .nav-link:hover {{
            background-color: #2c3e50;
        }}
        .content {{
            padding: 20px;
        }}
        .example-container {{
            margin-bottom: 40px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            overflow: hidden;
        }}
        .example-header {{
            background: #f8f9fa;
            padding: 15px 20px;
            border-bottom: 1px solid #dee2e6;
        }}
        .example-title {{
            margin: 0;
            color: #495057;
            font-size: 1.3em;
        }}
        .example-content {{
            padding: 20px;
        }}
        .container {{
            max-width: none;
            margin: 0;
            background: transparent;
            border-radius: 0;
            box-shadow: none;
            overflow: visible;
        }}
        .header {{
            background: #2c3e50;
            color: white;
            padding: 15px;
            text-align: center;
            margin-bottom: 20px;
        }}
        .metadata {{
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }}
        .metadata-item {{
            margin: 5px 0;
            font-size: 14px;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }}
        .metadata-label {{
            font-weight: bold;
            color: #2c3e50;
        }}
        .prompt-section, .response-section, .full-text-section, .response-only-section {{
            margin: 20px 0;
            padding: 15px;
            background: #f8f9fa;
            border-left: 4px solid #007bff;
            border-radius: 0 5px 5px 0;
            word-wrap: break-word;
            overflow-wrap: break-word;
            overflow-x: auto;
        }}
        .response-section {{
            border-left-color: #28a745;
        }}
        .full-text-section {{
            background: #fff3cd;
            border-left-color: #ffc107;
        }}
        .response-only-section {{
            background: #d1ecf1;
            border-left-color: #17a2b8;
        }}
        .section-title {{
            font-weight: bold;
            margin-bottom: 10px;
            color: #495057;
        }}
        .score-highlight {{
            background: #e9ecef;
            padding: 8px 12px;
            border-radius: 4px;
            margin: 10px 0;
            font-weight: bold;
        }}
        pre, code {{
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow-wrap: break-word;
            max-width: 100%;
            overflow-x: auto;
        }}
        .back-to-top {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #007bff;
            color: white;
            padding: 10px 15px;
            border-radius: 50px;
            text-decoration: none;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            transition: all 0.3s;
        }}
        .back-to-top:hover {{
            background: #0056b3;
            transform: translateY(-2px);
        }}
    </style>
</head>
<body>
    <div class="main-container">
        <div class="main-header">
            <h1>{folder_name.replace('_', ' ').title()}</h1>
            <p>Combined Analysis - {len(html_files)} Examples</p>
        </div>
        
        <div class="navigation">
            <a href="index.html" class="nav-link">← Back to Main Index</a>
            <a href="probe_results_combined.html" class="nav-link">Probe Results</a>
            <a href="probe_analysis_user_only_combined.html" class="nav-link">User Only</a>
            <a href="probe_analysis_belief2_combined.html" class="nav-link">Belief2</a>
        </div>
        
        <div class="content">'''
    
    # Add each example
    for i, html_file in enumerate(html_files):
        html_path = os.path.join(folder_path, html_file)
        title, header, main_content = extract_content_from_html(html_path)
        
        combined_html += f'''
            <div class="example-container" id="example-{i}">
                <div class="example-header">
                    <h2 class="example-title">{title}</h2>
                </div>
                <div class="example-content">
                    <div class="container">
                        <div class="header">
                            {header}
                        </div>
                        <div class="content">
                            {main_content}
                        </div>
                    </div>
                </div>
            </div>'''
    
    # Close the HTML
    combined_html += '''
        </div>
    </div>
    
    <a href="#" class="back-to-top">↑ Top</a>
    
    <script>
        // Smooth scrolling for back to top
        document.querySelector('.back-to-top').addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
        
        // Show/hide back to top button
        window.addEventListener('scroll', function() {
            const backToTop = document.querySelector('.back-to-top');
            if (window.pageYOffset > 300) {
                backToTop.style.display = 'block';
            } else {
                backToTop.style.display = 'none';
            }
        });
        
        // Initially hide the back to top button
        document.querySelector('.back-to-top').style.display = 'none';
    </script>
</body>
</html>'''
    
    # Write the combined HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(combined_html)
    
    print(f"Created {output_file} with {len(html_files)} examples")

def main():
    # Create combined pages for each folder
    folders = [
        ('probe_results', 'probe_results_combined.html'),
        ('probe_analysis_user_only', 'probe_analysis_user_only_combined.html'),
        ('probe_analysis_belief2', 'probe_analysis_belief2_combined.html')
    ]
    
    for folder_name, output_file in folders:
        if os.path.exists(folder_name):
            create_combined_page(folder_name, folder_name, output_file)
        else:
            print(f"Warning: Folder {folder_name} not found")

if __name__ == "__main__":
    main()
