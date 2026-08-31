import os
import glob
import re

course_dirs = [
    "Artifical Intelligence (AI)",
    "Data Analysis & Visualization",
    "Data Warehousing & Business Intelligence"
]

for cdir in course_dirs:
    if not os.path.isdir(cdir): continue
    
    html_files = sorted(glob.glob(f"{cdir}/*.html"))
    if not html_files: continue
    
    # Extract info from each file
    file_info = []
    for fpath in html_files:
        if "index.html" in fpath or "_template.html" in fpath: continue
        
        filename = os.path.basename(fpath)
        # Title is everything after "X- " and before ".html"
        m = re.match(r'(\d+)-\s*(.*)\.html', filename)
        num = m.group(1) if m else "0"
        title = m.group(2) if m else filename.replace('.html', '')
        
        # Read the file to extract its topics
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract nav-sublist
        sublist_match = re.search(r'<ul class="nav-sublist">.*?</ul>', content, re.DOTALL)
        sublist = sublist_match.group(0) if sublist_match else '<ul class="nav-sublist"></ul>'
        
        file_info.append({
            'path': fpath,
            'filename': filename,
            'num': num.zfill(2),
            'title': title,
            'sublist': sublist,
            'content': content
        })
        
    # Now rebuild the nav-list for each file
    for current_file in file_info:
        nav_html = '<ul class="nav-list" id="nav-list">\n'
        
        for fi in file_info:
            if fi['filename'] == current_file['filename']:
                # Current file is an accordion
                nav_html += f'''        <li class="nav-section">
          <div class="nav-section-title" onclick="toggleSection(this)">
            <span>{fi['title']}</span><span class="chevron">▼</span>
          </div>
          {fi['sublist']}
        </li>\n'''
            else:
                # Other file is a link
                nav_html += f'''        <li>
          <a class="nav-module-link" href="./{fi['filename']}">
            <span class="nav-num">{fi['num']}</span>{fi['title']}
          </a>
        </li>\n'''
                
        nav_html += '      </ul>'
        
        content = current_file['content']
        
        # Replace old nav-list
        content = re.sub(r'<ul class="nav-list" id="nav-list">.*?</ul>', nav_html, content, flags=re.DOTALL)
        
        # Fix the sidebar toggle button placement
        # First remove any existing buttons to avoid duplicates
        content = re.sub(r'<button class="sidebar-toggle-btn".*?</button>', '', content, flags=re.DOTALL)
        
        # Now insert the button properly outside the header text wrapper
        header_repl = r'''<div class="sidebar-header">
        <div class="sidebar-header-text">
          <div class="sidebar-course-label">\1</div>
          <div class="sidebar-title">\2</div>
        </div>
        <button class="sidebar-toggle-btn" onclick="document.getElementById('sidebar').classList.toggle('collapsed')" title="Toggle Sidebar">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><polyline points="15 18 9 12 15 6"></polyline></svg>
        </button>
      </div>'''
      
        content = re.sub(r'<div class="sidebar-header">.*?<div class="sidebar-course-label">(.*?)</div>.*?<div class="sidebar-title">(.*?)</div>.*?</div>', header_repl, content, flags=re.DOTALL)
        
        with open(current_file['path'], 'w', encoding='utf-8') as f:
            f.write(content)

print("Done rebuilding sidebars.")
