# AutoJs6 6.7.0 headless protocol (decoded from master source, 2026-10-28)

Sources: app/src/main/java/org/autojs/autojs/pluginclient/{JsonSocketServer.kt,
JsonSocketServerTool.kt, JsonSocket.java, DevPluginResponseHandler.java,
Router.java, Handler.java}, DevPluginService.kt (Partial).

## Ports
- `Port.AJ_SERVER = 7347` — the app's SERVER mode socket (app listens;
  PC connects). Started only when the app's "server mode" (服务端模式) is
  toggled (DevPluginService.enableLocalServer() ← JsonSocketServerTool.connect()).
- `Port.PC_SERVER = 6347` — client-mode endpoint the app connects TO
  (VSCode extension). Not what we need.

## Framing (JsonSocket.java)
- Header: 8 bytes = int32BE payload-length + int32BE type.
- Type codes: `Type.JSON = 1`, `Type.BYTES = 2`.
- Payload: UTF-8 JSON (type 1) or raw bytes (type 2).
- Handshake: client sends `{"type":"hello"}` → server state connected.
- Bytes commands use an md5 handshake (TYPE_BYTES_COMMAND, md5 flow).

## Commands (DevPluginResponseHandler)
JSON `{"type":"command", "command": <one of: run|stop|save|stopAll>, ...}`:
- `run`: fields `id`, `name`, `script` (full JS source inline — NO file
  push needed). Runs via StringScriptSource in the app's engine.
- `stop`, `stopAll`, `save`.
JSON `{"type":"bytes_command", "bytes_command": <run_project|save_project>}`
with the bytes/md5 flow for project dirs.

## Client script
`autojs_client.ps1` in this dir implements the protocol (connect 7347,
hello, run, read responses). Port default 7347.

## SIMPLER RUN PATH (no server mode needed) — verified from source
RunIntentActivity (exported, org.autojs.autojs6/.external.open.RunIntentActivity)
handles VIEW intents for file:// and content:// URIs with
application/x-javascript / text/plain:
- content:// → reads stream → Scripts.run(StringScriptSource)
- file:// → ScriptIntents.handleIntent → path = data.path →
  PathChecker → JavaScriptFileSource → scriptEngineService.execute()
So:
    am start -n org.autojs.autojs6/.external.open.RunIntentActivity \
      -a android.intent.action.VIEW -d file:///sdcard/your_script.js
runs the script headlessly. (Use for one-shot scripts. Use the 7347
server for long-running/stoppable scripts — the bot's 8h loop.)

## App internals
- Package: org.autojs.autojs6 (x86_64 build).
- Accessibility service: org.autojs.autojs.core.accessibility.AccessibilityServiceUsher
  (exported, BIND_ACCESSIBILITY_SERVICE). Enable headlessly:
    settings put secure enabled_accessibility_services \
      org.autojs.autojs6/org.autojs.autojs.core.accessibility.AccessibilityServiceUsher
- Main/splash activities: .ui.splash.SplashActivity (launcher),
  .ui.main.MainActivity (exported).
- All-files access: appops set org.autojs.autojs6 ANDROID_MANAGE_EXTERNAL_STORAGE allow
- Background-run scripts cwd: /data/user/0/org.autojs.autojs6/cache/tmp-scripts/
