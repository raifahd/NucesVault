const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, '../S5/Artifical Intelligence (AI)');
const files = [
  '1- Introduction to AI.html',
  '2- State Space Search.html',
  '3- Uninformed Search Algorithms.html',
  '4- Informed & Heuristic Search.html',
  '5- A-Star Search & Properties.html',
  '6- Adversarial Search & Game Playing.html',
  '7- Exam & Quiz Prep (Lectures 1-9).html',
  'index.html'
];

let allGood = true;

for (const f of files) {
  const p = path.join(dir, f);
  const html = fs.readFileSync(p, 'utf-8');
  const opens = (html.match(/<div[\s>]/g) || []).length;
  const closes = (html.match(/<\/div>/g) || []).length;
  const m = html.match(/const topics = \[(.*?)\];/);
  const cardIds = [...html.matchAll(/class="topic-card"[^>]*id="(.*?)"/g)].map(x => x[1]);
  
  console.log('--- ' + f + ' ---');
  console.log('  File Size: ' + (html.length / 1024).toFixed(1) + ' KB');
  console.log('  Divs count: opens=' + opens + ', closes=' + closes);
  if (m) {
    const topicsArr = JSON.parse('[' + m[1] + ']');
    console.log('  JS Topics: ' + topicsArr.join(', '));
    console.log('  DOM Cards: ' + cardIds.join(', '));
    const match = topicsArr.length === cardIds.length && topicsArr.every((t, i) => t === cardIds[i]);
    console.log('  Topics match Cards: ' + (match ? 'PASS' : 'FAIL'));
    if (!match) allGood = false;
  }
}

console.log('\nFinal Verification Result: ' + (allGood ? 'ALL PASS!' : 'FAILURES DETECTED'));
