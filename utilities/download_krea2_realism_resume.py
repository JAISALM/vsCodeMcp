import urllib.request, os, time

url = "https://huggingface.co/RudySen/Krea2-Realism-Checkpoint/resolve/main/Krea2Realism_V1.safetensors"
dest_dir = r"E:\ComfyUI_windows_portable\ComfyUI\models\diffusion_models"
os.makedirs(dest_dir, exist_ok=True)
dest = os.path.join(dest_dir, "Krea2Realism_V1.safetensors")
tmp = dest + ".part"
EXPECTED = 13141769680  # exact bytes (author-confirmed)

def part_size():
    try:
        return os.path.getsize(tmp)
    except OSError:
        return 0

attempt = 0
while True:
    done = part_size()
    if done >= EXPECTED:
        break
    attempt += 1
    print(f"[attempt {attempt}] {done/1e9:.2f} GB on disk "
          f"({done*100.0/EXPECTED:.1f}% of {EXPECTED/1e9:.2f} GB)", flush=True)
    headers = {"Range": f"bytes={done}-"} if done > 0 else {}
    req = urllib.request.Request(url, headers=headers)
    last_print = 0
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            # If the server ignored our Range and sent the full body, start clean.
            if done > 0 and r.status == 200:
                r.close()
                os.remove(tmp)
                done = 0
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req, timeout=120) as r:
                    body = r
            else:
                body = r
            with open(tmp, "ab") as f:
                while True:
                    chunk = body.read(16 * 1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    done += len(chunk)
                    if done - last_print >= 256 * 1024 * 1024:
                        last_print = done
                        print(f"\r{done/1e9:.2f}/{EXPECTED/1e9:.2f} GB ({done*100.0/EXPECTED:.1f}%)",
                              end="", flush=True)
    except Exception as e:
        print(f"\n! error ({e.__class__.__name__}: {e}) — retrying in 5s", flush=True)
        time.sleep(5)
        continue
    done = part_size()
    if done < EXPECTED:
        print(f"\n! stream ended at {done/1e9:.2f} GB ({done*100.0/EXPECTED:.1f}%) — resuming in 3s", flush=True)
        time.sleep(3)
        continue

os.replace(tmp, dest)
sz = os.path.getsize(dest)
print(f"\nDONE: {dest}  {sz/1e9:.2f} GB  ({'OK' if sz == EXPECTED else 'SIZE MISMATCH: ' + str(sz)})", flush=True)
