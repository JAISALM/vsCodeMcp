#!/usr/bin/env node
/**
 * mcp_fetch.js — fetch a URL with the SAME extraction engine VS Code uses
 * (D:\MCP\web-search-mcp: axios fast path -> playwright chromium fallback with
 * randomized UA/viewport/timezone, same as the websearch MCP gateway).
 *
 * Usage:  node mcp_fetch.js <url> [maxContentLength]
 * Output: JSON {url, title, content, wordCount, fetchStatus}
 *
 * Called by rag/fetch_news.py for reddit/X pages where plain HTTP gets
 * 403/429 anti-bot walls. Exit 0 on success, 1 on failure (JSON still printed).
 */
import { EnhancedContentExtractor } from "../../../MCP/web-search-mcp/dist/enhanced-content-extractor.js";

const url = process.argv[2];
const maxLen = parseInt(process.argv[3] || "12000", 10);
if (!url) {
  console.error("usage: node mcp_fetch.js <url> [maxContentLength]");
  process.exit(2);
}

// Mirror the gateway's browser env (D:\MCP\mcp-gateway\index.js BACKEND_DEFS)
process.env.BROWSER_HEADLESS = "true";
process.env.BROWSER_TYPES = "chromium";
process.env.BROWSER_FALLBACK_THRESHOLD = "3";
process.env.DEFAULT_TIMEOUT = "15000";

// Silence library debug noise (BrowserPool / extractor logs) — keep stdout JSON-only
const _err = console.error;
console.log = () => {};
console.info = () => {};
console.warn = () => {};
console.error = (m) => { if (typeof m === "string" && !m.startsWith("[mcp_fetch")) _err("[lib]", m); };

const out = { url, title: null, content: "", wordCount: 0, fetchStatus: "error", error: null };

try {
  const extractor = new EnhancedContentExtractor();
  const content = await extractor.extractContent({ url, timeout: 20000, maxContentLength: maxLen });
  out.content = content || "";
  out.wordCount = out.content ? out.content.split(/\s+/).filter(Boolean).length : 0;
  out.fetchStatus = out.wordCount >= 30 ? "success" : "low_quality";
  // Challenge-wall / paywall markers
  const probe = out.content.slice(0, 400).toLowerCase();
  if (/prove your humanity|are you a robot|access denied|captcha|rate limit|too many requests/.test(probe)) {
    out.fetchStatus = "blocked";
    out.blocked_reason = probe.slice(0, 120);
  }
} catch (e) {
  out.error = String(e && e.message || e);
} finally {
  try {
    // best-effort cleanup of any pooled browser
  } catch (_) {}
}

console.log = (m) => _err("[mcp_fetch]", m);
console.error = (m) => _err("[mcp_fetch-err]", m);
process.stdout.write(JSON.stringify(out) + "\n");
process.exit(out.fetchStatus === "success" ? 0 : 1);
