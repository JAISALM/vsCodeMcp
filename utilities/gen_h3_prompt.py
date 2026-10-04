# -*- coding: utf-8 -*-
r"""
Generate / refine a MiniMax H3 R2V prompt using the purpose-built H3 prompt model
(Qwen3-VL-32B-Instruct-MiniMax-H3-L0-49) running on port 8104.

WHY: hand-crafted R2V prompts kept getting the structure wrong (generic "school
kid" instead of our character, <Picture N> tags not matching the actual refs).
This model is a VISION-LANGUAGE model fine-tuned on MiniMax H3 prompt data, so we
feed it the ACTUAL reference images + a short shot description, and it writes a
proper H3-structured prompt that matches what's really in the images.

PREREQ: the model must be running on port 8104:
    D:\models\Writing\Qwen\run-minimax-h3-heretic.bat
(It is a SEPARATE llama-server; it does NOT stop Qwen. It is a quick job, not a
long render, so it is fine to run while Qwen is up.)

USAGE:
    python gen_h3_prompt.py --desc "Shot 1 THE WALK IN: the empty dark room, a
        single bare bulb above a wooden table. The boy enters from the darkness,
        drags the chair, and sits down. WIDE STATIC eye-level 35mm, locked
        camera. Black & white, high contrast, fine grain." \
        --refs "D:\models\vsCodeMcp\Jaisal-intro\keyframes\table empty.png" \
               "D:\models\vsCodeMcp\Jaisal-intro\keyframes\jaisal_hand_under_the_table.png" \
        --out "D:\models\vsCodeMcp\Jaisal-intro\prompts\shot_A_walkin.txt"

    (or --desc-file shot_A.txt instead of --desc)

The model sees each --refs image in order and tags them <Picture 1>, <Picture 2>,
... in that order. Keep it to 2-3 refs (per D020).
"""
import argparse, base64, json, os, sys, urllib.request

PORT = 8104
URL = f"http://127.0.0.1:{PORT}/v1/chat/completions"

SYSTEM = """You are a MiniMax H3 reference-to-video (R2V) prompt writer.
You are given a short shot description and 1-3 reference images (in order).
Write a production-quality MiniMax H3 R2V prompt that animates smoothly from the
first reference image to the last.

STRICT RULES:
- Use the 6-section structure, in this exact order, with these exact headers:
  subject_definitions:
  summary:
  retention_analysis:
  detailed_description:
  overall_soundscape:
  non_diegetic_music:
- In subject_definitions, tag each reference image as <Picture 1>, <Picture 2>, ...
  in the SAME order the images were given. Assign each an explicit job (identity /
  style / motion / frame anchor). Use <Subject 1> for the reusable character.
- Describe the character from what is ACTUALLY visible in the reference images
  (do NOT invent a generic description). There is ONLY ONE character - no
  duplicates, no second person.
- summary starts with a [task-type] prefix like [reference generation].
- detailed_description is partitioned into [Shot 1] ... [Shot N] blocks with a
  camera angle + the action, and says the shot BEGINS from <Picture 1> and ENDS
  exactly on <Picture N>.
- overall_soundscape: NATURAL SOUNDS ONLY (footsteps, chair scrape, breath,
  room tone, paper rustle).
- non_diegetic_music MUST state: NO music, NO instrumental music, NO musical
  instruments, NO melody, NO beat, NO rhythm, NO soundtrack, NO song. Natural
  ambient sounds only.
- Add a final line: negative: <comma-separated things to avoid>
- Black & white, high contrast, fine film grain, 24fps unless told otherwise.
- Keep it tight (no 500-word bloat). Output ONLY the prompt, no commentary."""


def b64_data_uri(path):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    if ext == "jpg":
        ext = "jpeg"
    return f"data:image/{ext};base64,{data}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--desc", help="Short shot description (action + camera + look).")
    ap.add_argument("--desc-file", help="File containing the shot description.")
    ap.add_argument("--refs", nargs="+", required=True, help="Reference image paths, in order.")
    ap.add_argument("--out", help="Save the generated prompt to this file.")
    ap.add_argument("--port", type=int, default=PORT)
    ap.add_argument("--model", default="default", help="Model name (llama-server default).")
    ap.add_argument("--max-tokens", type=int, default=1200)
    args = ap.parse_args()

    global URL
    URL = f"http://127.0.0.1:{args.port}/v1/chat/completions"

    desc = args.desc
    if args.desc_file:
        with open(args.desc_file, encoding="utf-8") as f:
            desc = f.read().strip()
    if not desc:
        sys.exit("ERROR: provide --desc or --desc-file")

    # Build the user message: text + images in order.
    content = [{"type": "text", "text": desc.strip() + "\n\nReference images (in order):"}]
    for i, p in enumerate(args.refs, 1):
        if not os.path.exists(p):
            sys.exit(f"ERROR: reference image not found: {p}")
        content.append({"type": "text", "text": f"<Picture {i}> = {os.path.basename(p)}"})
        content.append({"type": "image_url", "image_url": {"url": b64_data_uri(p)}})

    body = {
        "model": args.model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": content},
        ],
        "max_tokens": args.max_tokens,
        "temperature": 0.4,
    }
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    print(f"Calling H3 prompt model on port {args.port} ...", file=sys.stderr)
    with urllib.request.urlopen(req, timeout=300) as r:
        resp = json.load(r)
    prompt = resp["choices"][0]["message"]["content"].strip()

    print(prompt)
    if args.out:
        os.makedirs(os.path.dirname(args.out), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(prompt + "\n")
        print(f"\n[saved to {args.out}]", file=sys.stderr)


if __name__ == "__main__":
    main()
