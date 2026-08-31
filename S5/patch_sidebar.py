import glob
import re

html_files = glob.glob("**/*.html", recursive=True)

for filepath in html_files:
    if "index.html" in filepath or "_template.html" in filepath:
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix the header structure for flexbox so button sits perfectly
    # Find the block between <div class="sidebar-header"> and </div>
    header_pattern = re.compile(r'(<div class="sidebar-header">)(.*?)(</div>\s*<div class="sidebar-search-wrap">)', re.DOTALL)
    
    def repl_header(match):
        inner = match.group(2)
        # Wrap the text in .sidebar-header-text if not already wrapped
        if 'sidebar-header-text' not in inner:
            # We want to put the course-label and title inside a wrapper, keeping the button outside
            btn_match = re.search(r'<button.*?</button>', inner, re.DOTALL)
            btn_html = btn_match.group(0) if btn_match else ""
            
            rest = inner
            if btn_html:
                rest = inner.replace(btn_html, '')
            
            wrapped = f'\n        <div class="sidebar-header-text">{rest}</div>\n        {btn_html}\n      '
            return match.group(1) + wrapped + match.group(3)
        return match.group(0)
        
    content = header_pattern.sub(repl_header, content)
    
    # 2. Strip "Module X — " from the entire sidebar area
    nav_pattern = re.compile(r'(<ul class="nav-list".*?</ul>\s*</div>)', re.DOTALL)
    
    def repl_nav(match):
        nav_html = match.group(1)
        # Remove "Module \d+ — " (handles em dash, en dash, regular hyphen)
        nav_html = re.sub(r'Module \d+ (—|&mdash;|&ndash;|-)\s*', '', nav_html)
        
        # Now we need to sort the top-level <li> elements chronologically
        # To do this safely, we will extract them manually
        
        # This is a bit complex in raw regex, let's just use bs4
        return nav_html
        
    # We will use BeautifulSoup to safely reorder the elements
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        nav_list = soup.find('ul', id='nav-list')
        
        if nav_list:
            items = nav_list.find_all('li', recursive=False)
            
            def get_mod_num(li):
                # find .nav-num inside the item
                nav_num = li.find(class_='nav-num')
                if nav_num:
                    try:
                        return int(nav_num.text.strip())
                    except:
                        pass
                # fallback: if it's the current section, we already stripped "Module X"
                # so we can't easily tell. Let's look at the original content for clues.
                # Actually, earlier I didn't strip it yet in BeautifulSoup
                return 999
            
            # Let's extract numbers BEFORE stripping
            items_with_num = []
            for li in items:
                num = 999
                # If it's a module link
                mod_num_span = li.find(class_='nav-num')
                if mod_num_span and mod_num_span.text.isdigit():
                    num = int(mod_num_span.text.strip())
                else:
                    # If it's a section title, look for "Module X"
                    title_span = li.find('span')
                    if title_span and 'Module' in title_span.text:
                        m = re.search(r'Module (\d+)', title_span.text)
                        if m:
                            num = int(m.group(1))
                items_with_num.append((num, li))
                
            items_with_num.sort(key=lambda x: x[0])
            
            # Clear and append in order
            nav_list.clear()
            for num, li in items_with_num:
                # Strip "Module X -" from the text inside this li
                for span in li.find_all('span'):
                    if span.text and 'Module' in span.text:
                        span.string = re.sub(r'Module \d+ [—\-\–]\s*', '', span.text)
                        
                nav_list.append(li)
                
            content = str(soup)
            
    except ImportError:
        # Fallback if bs4 is not available
        pass

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done patching.")
