import glob
import re

html_files = glob.glob("**/*.html", recursive=True)

for filepath in html_files:
    if "index.html" in filepath or "_template.html" in filepath:
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the nav-list block
    m = re.search(r'<ul class="nav-list" id="nav-list">(.*?)</ul>\s*(?:</div>\s*<div id="main-content"|</div>\s*<!--)', content, re.DOTALL)
    if not m:
        # Try a different boundary
        m = re.search(r'<ul class="nav-list" id="nav-list">(.*?)</ul>\s*</div>', content, re.DOTALL)
        
    if m:
        nav_content = m.group(1)
        # Split by top-level <li> elements
        # This is tricky with regex, but we can split by <li class="nav-section"> and <li>
        # A safer way without bs4 is to find all top level <li> chunks.
        chunks = []
        current_chunk = ""
        depth = 0
        
        # A simple state machine to parse HTML list items
        i = 0
        while i < len(nav_content):
            if nav_content.startswith('<li', i):
                if depth == 0:
                    current_chunk = ""
                depth += 1
                current_chunk += '<li'
                i += 3
            elif nav_content.startswith('</li', i):
                depth -= 1
                current_chunk += '</li'
                i += 4
                if depth == 0:
                    current_chunk += '>'
                    chunks.append(current_chunk)
                    # skip to '>'
                    while i < len(nav_content) and nav_content[i] != '>':
                        i += 1
                    i += 1
            else:
                if depth > 0:
                    current_chunk += nav_content[i]
                i += 1
                
        # Now process chunks
        processed = []
        for c in chunks:
            # strip module string
            c = re.sub(r'Module \d+ [—\-\–]\s*', '', c)
            
            # extract number
            num = 999
            num_m = re.search(r'<span class="nav-num">0?(\d+)</span>', c)
            if num_m:
                num = int(num_m.group(1))
            else:
                # Look for "Module X" if we hadn't stripped it (too late), or look for href
                # Let's see if there's a title with a number, e.g. "1 - "
                pass
                
            processed.append((num, c))
            
        processed.sort(key=lambda x: x[0])
        
        new_nav = "\n" + "\n".join([x[1] for x in processed]) + "\n"
        
        content = content[:m.start(1)] + new_nav + content[m.end(1):]
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done with regex patch.")
