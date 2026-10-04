# Krea2 T2I/I2I/Inpaint 2-Pass Workflow — Guide

**Source:** `E:\Krea2\krea2T2iI2iInpaint2pass_v15.json` (highly-voted production workflow)
**Configured copy:** `user\default\workflows\krea2_2pass_bf16_turbo.json`
**What it is:** a Krea2 image workflow that does **text-to-image, image-to-image, and inpainting** in a **2-pass** setup (a fast 1st pass + a Clownshark 2nd pass for quality), with a bunch of optional "bells and whistles" you can toggle on/off.

---

## The 3 modes (pick ONE)

The workflow can do three things. You switch between them with the **group toggles** at the bottom of the canvas (rgthree Fast Groups nodes):

| Mode | What it does | Base image? |
|------|-------------|-------------|
| **T2I** (text2image) | Generate from scratch from the prompt | No |
| **I2I full image** (image2image) | Re-render the WHOLE image guided by prompt + base image | Yes (LoadImage) |
| **Inpaint** | Regenerate ONLY a painted region, keep the rest | Yes (LoadImage + mask) |

**The workflow ships in T2I mode** — that's why the **LoadImage node is bypassed** (greyed out with a slash). This is NORMAL, not a bug. To use I2I/Inpaint you switch the toggles (below), which activates the LoadImage.

---

## The toggles (bottom of canvas — be careful here)

These are the rgthree "Fast Groups" nodes. Each one controls a group of nodes:

| Toggle node | Title | Controls |
|-------------|-------|----------|
| **Whatcha Up To?** | `text2image` / `image2image` | Which top-level mode. Pick **image2image** for I2I/Inpaint. |
| **Full Image i2i = On \| Inpainting = Off** | `i2i Entire Image` group | **ON** = full-image I2I. **OFF** = Inpaint (uses your painted mask). |
| **Latent Size** | `Aspect Ratio` / `Custom Size` | Pick one. Aspect Ratio = use the ResolutionSelector (e.g. 9:16). Custom Size = use the Width/Height primitives. |
| **Bells and Whistles** | `Turbo LoRA?` / `Negative Conditioning` / `Enhancer` / `Misc Quality Functions` | Optional extras. Toggle each on/off as needed. |
| (untitled muter) | `2nd Pass` group | Enable/disable the Clownshark 2nd pass. |

**For inpainting, the toggle recipe:**
1. **Whatcha Up To?** → `image2image`
2. **Full Image i2i = On | Inpainting = Off** → toggle to **OFF** (now it's inpainting)
3. **Latent Size** → `Aspect Ratio` (or Custom Size)
4. **Bells and Whistles** → enable `Turbo LoRA?` + `Negative Conditioning` (see below)

---

## Where to paint (inpainting)

1. Set the **LoadImage** node to your base image (e.g. `mic_small_id_00001_.png`).
2. **Right-click the LoadImage node → "Open in Mask Editor".**
3. **Paint the region you want to REGENERATE** (e.g. the black mic). Paint it **white/opaque**.
4. The mask is saved to clipspace and the LoadImage **MASK** output picks it up → feeds `InpaintModelConditioning` → only that region is regenerated, everything else stays.

> **Mask polarity caveat:** ComfyUI's `LoadImage` MASK output = `1 − alpha`. If the result regenerates the *wrong* region (the complement), **invert the mask** in the Mask Editor (or paint the region you want to *keep* instead). Test once and you'll see which way it goes.

---

## The model chain (what I configured)

```
UNETLoader (krea2_turbo_bf16) ─┐
CLIPLoader (qwen3vl_4b_fp8)  ──┤
                                ▼
                       ApplyKrea2NegPiP   ← negative-pipe patch (installed from blue-pen5805/ComfyUI-krea2-negpip)
                                ▼
              ComfyUI-Krea2T-Enhancer (bypassed by default)
                                ▼
              ModelSamplingFlux (bypassed) → CFGOverride (bypassed)
                                ▼
              Power Lora Loader (Turbo LoRA, on)   ← feeds BOTH passes
                                ▼
        ┌───────────────────────┴───────────────────────┐
        ▼                                               ▼
  1st Pass KSampler (307)                    2nd Pass Clownshark subgraph (186)
  20 steps, cfg 1, exp_heun_2_x0_sde         (refines the 1st pass)
        ▼                                               ▼
  1st Pass Preview                          2nd Pass Preview → Final Image (Image Saver Simple)
```

**Configured for (per your choice):**
- **UNet** = `krea2_turbo_bf16.safetensors` (bf16 Krea2, 26 GB)
- **Turbo LoRA** = `krea2_turbo_lora_rank_64_bf16.safetensors` @ 1.0 (enabled in the active Power Lora Loader)
- **VAE** = `krea2RealVae_v10.safetensors` (already in place, now picked up by the server)
- **CLIP** = `qwen3vl_4b_fp8_scaled.safetensors` (type `krea2`) — unchanged
- **LoadImage** = `mic_small_id_00001_.png` (base image)

> **Note on the Turbo LoRA:** the workflow author's note says *"Only enable the Turbo LoRA if you're using a Raw version of Krea2."* We're using the **Turbo** base (`krea2_turbo_bf16`), so the Turbo LoRA is technically redundant — but it's harmless and you asked for it, so it's enabled. If results look off, try toggling `Turbo LoRA?` OFF.

---

## The "bells and whistles" (optional, toggle as needed)

- **Negative Conditioning** — *super important* (author's words). Add `(word:-1.0)` to the prompt to negatively weight a term. The `ApplyKrea2NegPiP` node is what makes negative weights actually work on Krea2.
- **Enhancer** (`ComfyUI-Krea2T-Enhancer`) — "jazz up boring seeds." Bypassed by default.
- **Misc Quality Functions** — `ModelSamplingFlux`, `CFGOverride`, `ImageResizeKJv2` — all bypassed by default; experiment.
- **2nd Pass** (Clownshark subgraph) — a second refinement pass. Keep it on for quality; mute it for speed.

---

## Run steps (inpainting example)

```powershell
Stop-Process -Name "llama-server" -Force
```
1. Open **`krea2_2pass_bf16_turbo.json`** in a **fresh tab**.
2. Set **Whatcha Up To?** → `image2image`; **Full Image i2i** → OFF (inpaint); **Latent Size** → `Aspect Ratio`.
3. **LoadImage** = `mic_small_id_00001_.png` (already set).
4. **Right-click LoadImage → Open in Mask Editor** → paint the region to regenerate (white).
5. Write the **positive prompt** (node 247) + add `(bad_thing:-1.0)` negatives.
6. **Queue Prompt** → check **1st Pass Preview** and **2nd Pass Preview** (Image Comparer shows A/B).
7. Restart Qwen:
```powershell
Start-Process "D:\models\qwen\Qwen3.827BMTP.bat"
```

---

## Validation note

`validate_workflow` reports 5 `unknown_class_type` errors for `Fast Groups Muter/Bypasser (rgthree)` — these are **false positives** (frontend-only canvas widgets; the server prunes them, confirmed by the "feeds no output node" warnings). They do **not** block the run. All real generation nodes validate clean.

## Setup scripts (in `utilities/`)
- `configure_2pass.py` — writes `krea2_2pass_bf16_turbo.json` (bf16 krea + turbo LoRA + krea2RealVae + base image)
- `diagnose_krea2_2pass.py` — lists which node packs are missing
- `dump_2pass_full.py` / `dump_2pass_toggles.py` / `trace_2pass_model.py` — structure dumps for reference
