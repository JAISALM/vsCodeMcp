// Analyze Copilot chat session main.jsonl files for large tool outputs (OOM suspects)
const fs = require('fs');
const path = require('path');
const logDir = 'c:\\Users\\user\\AppData\\Roaming\\Code\\User\\workspaceStorage\\cba11f6546ae9da7922a38728436c8b2\\GitHub.copilot-chat\\debug-logs';
const sessions = process.argv.slice(2);
for (const s of sessions) {
  const f = path.join(logDir, s, 'main.jsonl');
  if (!fs.existsSync(f)) { console.log(`=== ${s}: NOT FOUND ===`); continue; }
  const raw = fs.readFileSync(f, 'utf8');
  const lines = raw.split('\n').filter(Boolean).map(l => { try { return JSON.parse(l); } catch (e) { return null; } }).filter(Boolean);
  const tc = lines.filter(e => e.type === 'tool_call');
  const big = tc.map(e => ({ name: e.name, len: (e.attrs && e.attrs.result ? String(e.attrs.result).length : 0), dur: e.dur || 0 }))
    .sort((a, b) => b.len - a.len).slice(0, 8);
  const llm = lines.filter(e => e.type === 'llm_request');
  const maxIn = Math.max(0, ...llm.map(e => (e.attrs && e.attrs.inputTokens) || 0));
  const maxOut = Math.max(0, ...llm.map(e => (e.attrs && e.attrs.outputTokens) || 0));
  const errs = lines.filter(e => e.status === 'error');
  console.log(`\n=== ${s}  (main.jsonl ${(raw.length / 1024 / 1024).toFixed(1)} MB) ===`);
  console.log(`tool_calls: ${tc.length} | llm_requests: ${llm.length} | max inputTokens: ${maxIn} | max outputTokens: ${maxOut} | errors: ${errs.length}`);
  console.log('Top tool outputs by size:');
  big.forEach(b => console.log(`  ${b.name}  ${(b.len / 1024).toFixed(0)}KB  dur=${(b.dur / 1000).toFixed(1)}s`));
  if (errs.length) {
    console.log('Errors:');
    errs.slice(0, 6).forEach(e => console.log(`  ERR ${e.type} ${e.name}: ${e.attrs && e.attrs.error ? String(e.attrs.error).slice(0, 140) : (e.attrs && e.attrs.result ? String(e.attrs.result).slice(0, 140) : '')}`));
  }
}
