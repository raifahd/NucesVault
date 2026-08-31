import os
import glob
import re

html_files = glob.glob("**/*.html", recursive=True)

for filepath in html_files:
    if "index.html" in filepath:
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Add sidebar toggle button to sidebar-header
    if 'sidebar-toggle-btn' not in content:
        content = content.replace(
            '<div class="sidebar-header">',
            '<div class="sidebar-header">\n        <button class="sidebar-toggle-btn" onclick="document.getElementById(\'sidebar\').classList.toggle(\'collapsed\')" title="Toggle Sidebar">\n          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="9" y1="3" x2="9" y2="21"></line></svg>\n        </button>'
        )
        
    # 2. Add autoshrink logic on load and resize
    if 'function showTopic(id)' in content and 'checkSidebarSize()' not in content:
        script_addition = """
      function checkSidebarSize() {
        if (window.innerWidth <= 1024) {
          document.getElementById('sidebar').classList.add('collapsed');
        } else {
          document.getElementById('sidebar').classList.remove('collapsed');
        }
      }
      window.addEventListener('resize', checkSidebarSize);
      checkSidebarSize();
        """
        content = content.replace('function showTopic(id) {', script_addition + '\n      function showTopic(id) {')
        
    # 3. Change scroll logic from main-content to the topic card itself
    if '.scrollTo({ top: 0, behavior: "smooth" });' in content:
        content = content.replace(
            'document\n          .getElementById("main-content")\n          .scrollTo({ top: 0, behavior: "smooth" });',
            'if (t) t.scrollIntoView({ behavior: "smooth", block: "start" });'
        )
    elif 'document.getElementById("main-content").scrollTo({ top: 0, behavior: "smooth" });' in content:
        content = content.replace(
            'document.getElementById("main-content").scrollTo({ top: 0, behavior: "smooth" });',
            'if (t) t.scrollIntoView({ behavior: "smooth", block: "start" });'
        )

    # 4. If they wanted to get rid of the "Module 1 - Title" in the sidebar and just list topics directly:
    # Let's keep it as is, but we've fixed the scroll which was the main annoyance.

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
print(f"Patched {len(html_files)} HTML files.")
