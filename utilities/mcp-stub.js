// Zero-tool MCP stdio stub.
// Purpose: shadow VS Code's built-in remote "github-mcp-server" (which exposes a
// large tool catalog that pushes the agent's per-request tool count over the
// 128 limit -> 502 "Cannot have more than 128 tools per request").
// Register it in .vscode/mcp.json under the name "github-mcp-server"; the
// agent host then skips the built-in remote server and uses this stub instead.
// The stub answers the MCP handshake and reports NO tools.

'use strict';
const readline = require('readline');

function reply(obj) {
  process.stdout.write(JSON.stringify(obj) + '\n');
}

const rl = readline.createInterface({ input: process.stdin, terminal: false });

rl.on('line', (line) => {
  line = line.trim();
  if (!line) return;

  let msg;
  try {
    msg = JSON.parse(line);
  } catch {
    return;
  }

  const id = msg.id;
  const method = msg.method;

  // Notifications (no id) need no response.
  if (id === undefined || id === null) return;

  switch (method) {
    case 'initialize': {
      const requested = msg.params && msg.params.protocolVersion;
      reply({
        jsonrpc: '2.0',
        id,
        result: {
          protocolVersion: requested || '2025-03-26',
          capabilities: { tools: { listChanged: false } },
          serverInfo: { name: 'github-mcp-server', version: '0.0.0-stub' },
          instructions:
            'Stub server providing no tools. The built-in remote GitHub MCP ' +
            'server is intentionally replaced to keep the tool count under the ' +
            '128 per-request limit.'
        }
      });
      break;
    }
    case 'tools/list':
      reply({ jsonrpc: '2.0', id, result: { tools: [] } });
      break;
    case 'tools/call':
      reply({
        jsonrpc: '2.0',
        id,
        error: { code: -32601, message: 'Stub server has no tools' }
      });
      break;
    case 'resources/list':
      reply({ jsonrpc: '2.0', id, result: { resources: [] } });
      break;
    case 'prompts/list':
      reply({ jsonrpc: '2.0', id, result: { prompts: [] } });
      break;
    case 'ping':
      reply({ jsonrpc: '2.0', id, result: {} });
      break;
    default:
      // Unknown request: answer with method-not-found so clients never hang.
      reply({
        jsonrpc: '2.0',
        id,
        error: { code: -32601, message: `Method not supported by stub: ${method}` }
      });
  }
});

process.on('SIGTERM', () => process.exit(0));
process.on('SIGINT', () => process.exit(0));
