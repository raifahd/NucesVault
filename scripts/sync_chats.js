const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const workspaceRoot = path.resolve(__dirname, '..');
const brainDir = path.join(process.env.USERPROFILE, '.gemini', 'antigravity-ide', 'brain');
const outDir = path.join(workspaceRoot, '_chat_archive');

if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
}

const workspaceMap = {
    '4042cefa-e13a-4d98-b8f5-050ee898bef0': 'FBR Sales Tax Invoicing',
    '78b99f46-0909-4e8b-a5a7-af4f0f47c1b2': 'POS System (Cart)',
    '7d5fcbce-c8a6-4d08-b692-0b9bdb0499a3': 'Semester 5 Notes (Current)',
    'b57280fc-518b-4754-8575-74d3e9376a45': 'HR Attendance',
    'd01d49e9-1917-4179-88bc-31edcc0f6afe': 'FBR Invoicing',
    'd291d660-6418-49b9-ae9c-d7f64bf7b1e7': 'Semester 5 Notes (AI Lectures 1-9)',
    'e465a275-2b29-4de9-a657-ec4515b1c7c8': 'POS System'
};

const dirs = fs.readdirSync(brainDir, { withFileTypes: true })
    .filter(d => d.isDirectory() && d.name !== 'tempmediaStorage' && !d.name.startsWith('_'));

const indexData = [];

for (const d of dirs) {
    const convoId = d.name;
    const logFile = path.join(brainDir, convoId, '.system_generated', 'logs', 'transcript.jsonl');
    if (!fs.existsSync(logFile)) continue;

    const lines = fs.readFileSync(logFile, 'utf8').split('\n').filter(Boolean);
    const messages = [];
    let firstUserPrompt = '';
    let lastTime = '';

    for (const line of lines) {
        try {
            const entry = JSON.parse(line);
            if (entry.created_at) lastTime = entry.created_at;
            if (entry.type === 'USER_INPUT') {
                let text = entry.content || '';
                text = text.replace(/<USER_REQUEST>/g, '').replace(/<\/USER_REQUEST>/g, '').trim();
                if (text.includes('<ADDITIONAL_METADATA>')) {
                    text = text.split('<ADDITIONAL_METADATA>')[0].trim();
                }
                if (!firstUserPrompt && text) {
                    firstUserPrompt = text.slice(0, 100);
                }
                messages.push({ role: 'user', content: text, time: entry.created_at });
            } else if (entry.type === 'PLANNER_RESPONSE' && entry.content) {
                messages.push({ role: 'assistant', content: entry.content, time: entry.created_at });
            }
        } catch (e) {}
    }

    const title = firstUserPrompt ? firstUserPrompt.split('\n')[0].replace(/[^\w\s-]/g, '').slice(0, 55).trim() : `Session ${convoId.slice(0, 8)}`;
    const workspace = workspaceMap[convoId] || 'Workspace';

    // Generate Markdown
    let mdContent = `# ${title || 'Conversation'}\n\n`;
    mdContent += `* **ID**: \`${convoId}\`\n`;
    mdContent += `* **Workspace**: ${workspace}\n`;
    mdContent += `* **Last Active**: ${lastTime}\n`;
    mdContent += `* **Messages**: ${messages.length}\n\n---\n\n`;

    for (const msg of messages) {
        if (msg.role === 'user') {
            mdContent += `### 👤 User (${msg.time || ''})\n\n${msg.content}\n\n`;
        } else {
            mdContent += `### 🤖 Assistant (${msg.time || ''})\n\n${msg.content}\n\n---\n\n`;
        }
    }

    const safeFilename = `${workspace.replace(/[^a-zA-Z0-9_-]/g, '_')}_${convoId.slice(0, 8)}.md`;
    fs.writeFileSync(path.join(outDir, safeFilename), mdContent);

    indexData.push({
        id: convoId,
        title: title || 'Conversation',
        workspace,
        file: safeFilename,
        lastTime,
        messageCount: messages.length
    });
}

// Generate interactive HTML index
const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Antigravity Permanent Conversations Hub</title>
<style>
  :root { --bg: #090d16; --card: #131b2e; --border: #223152; --text: #d8e2f0; --accent: #38bdf8; --meta: #94a3b8; }
  * { box-sizing: border-box; }
  body { font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); padding: 2rem; max-width: 1200px; margin: 0 auto; line-height: 1.5; }
  header { border-bottom: 1px solid var(--border); padding-bottom: 1.5rem; margin-bottom: 2rem; }
  h1 { color: #f8fafc; font-size: 1.8rem; margin: 0 0 0.5rem 0; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; }
  .status-badge { font-size: 0.85rem; padding: 4px 12px; background: rgba(56, 189, 248, 0.15); color: var(--accent); border: 1px solid var(--accent); border-radius: 9999px; }
  p { color: var(--meta); margin: 0; }
  .search-box { width: 100%; padding: 14px 18px; border-radius: 10px; border: 1px solid var(--border); background: var(--card); color: #fff; font-size: 1.05rem; margin-bottom: 2rem; outline: none; }
  .search-box:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2); }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 1.25rem; }
  .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; text-decoration: none; color: inherit; display: flex; flex-direction: column; justify-content: space-between; transition: transform 0.2s, border-color 0.2s; }
  .card:hover { transform: translateY(-4px); border-color: var(--accent); }
  .badge { display: inline-block; background: rgba(56, 189, 248, 0.1); color: var(--accent); border: 1px solid rgba(56, 189, 248, 0.3); font-size: 0.75rem; padding: 3px 10px; border-radius: 20px; font-weight: 600; margin-bottom: 0.85rem; align-self: flex-start; }
  h3 { margin: 0 0 0.75rem 0; color: #fff; font-size: 1.15rem; line-height: 1.4; }
  .meta { font-size: 0.85rem; color: var(--meta); display: flex; justify-content: space-between; border-top: 1px solid var(--border); padding-top: 1rem; margin-top: 1rem; }
</style>
</head>
<body>
  <header>
    <h1>🛡️ Antigravity Permanent Cloud Hub <span class="status-badge">☁️ Web & Git Backed</span></h1>
    <p>All conversations permanently preserved, searchable across all workspaces, and immune to IDE resets or cache corruption.</p>
  </header>
  <input type="text" id="filter" class="search-box" placeholder="Search conversations by keywords, project, or topic..." oninput="filterConvos()">
  <div class="grid" id="convoGrid">
    ${indexData.map(c => `
      <a class="card" href="./${c.file}" target="_blank" data-text="${(c.title + ' ' + c.workspace).toLowerCase()}">
        <div>
          <span class="badge">${c.workspace}</span>
          <h3>${c.title}</h3>
        </div>
        <div class="meta">
          <span>💬 ${c.messageCount} messages</span>
          <span>📅 ${c.lastTime ? c.lastTime.slice(0,10) : 'Recent'}</span>
        </div>
      </a>
    `).join('')}
  </div>
  <script>
    function filterConvos() {
      const q = document.getElementById('filter').value.toLowerCase();
      document.querySelectorAll('.card').forEach(el => {
        el.style.display = el.getAttribute('data-text').includes(q) ? 'flex' : 'none';
      });
    }
  </script>
</body>
</html>`;

fs.writeFileSync(path.join(outDir, 'index.html'), html);
console.log(`Successfully exported ${indexData.length} conversations to ${outDir}`);
