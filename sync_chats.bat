@echo off
echo ========================================================
echo   Antigravity Permanent Conversation Web Sync
echo ========================================================
node scripts\sync_chats.js
git add _chat_archive scripts\sync_chats.js sync_chats.bat
git commit -m "chore(backup): auto-sync Antigravity conversation history to web"
git push origin main
echo ========================================================
echo   Done! All conversations are safely backed up to GitHub.
echo ========================================================
pause
