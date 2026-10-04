import json

files = [
    r"c:\Users\user\AppData\Roaming\Code\User\workspaceStorage\cba11f6546ae9da7922a38728436c8b2\GitHub.copilot-chat\chat-session-resources\30d3de1b-e298-4a61-a145-5ef55c362ff0\LYtaUFNWY5MjL3iavrq67rNyZ8qYOF2Y__vscode-1790597932035\content.json",
    r"c:\Users\user\AppData\Roaming\Code\User\workspaceStorage\cba11f6546ae9da7922a38728436c8b2\GitHub.copilot-chat\chat-session-resources\30d3de1b-e298-4a61-a145-5ef55c362ff0\AHMyZ3YztP3wxGP6cASsYZG5ZaVz9W11__vscode-1790597932036\content.json",
]
for f in files:
    raw = open(f, encoding="utf-8").read()
    d = json.loads(raw)
    if isinstance(d, str):
        d = json.loads(d)
    print("=" * 70)
    print("FILE:", f.split("\\")[-2])
    print(json.dumps(d, indent=1)[:4000])
