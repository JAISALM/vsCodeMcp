# Litminer Bot — phone-only setup (no PC)

One app + one script on the Android phone. It runs the free claim every 8
hours by itself while the phone is on Wi-Fi, and shows a floating status
panel you can show anyone.

## 1. Install OpenAuto.js (free, open-source)

The maintained open-source Auto.js engine is **OpenAuto.js**:
<https://github.com/openautojs/openautojs>

Download the latest release APK (6.4.1) directly on the phone:

- **Most Android phones (2018+):**
  <https://github.com/openautojs/openautojs/releases/download/6.4.1/app-common-arm64-v8a-release.apk> (80 MB)
- **Older / 32-bit phone (or if the above fails):**
  <https://github.com/openautojs/openautojs/releases/download/6.4.1/app-common-universal-release.apk> (98 MB)
- All releases: <https://github.com/openautojs/openautojs/releases>

Open the APK → install (allow "unknown sources" if asked).

First open of the app — grant:
- **Accessibility** — required, it's how the script taps (the app shows a
  button that jumps you to the right settings page).
- **Display over other apps** — for the floating status panel.
- When the script first takes a screenshot, Android asks for
  **screen-capture** permission — allow it.

## 2. Get the script onto the phone

Easiest: send `litminer_bot.js` to yourself on Telegram/WhatsApp
("saved messages"), open it in the phone so it lands in **Downloads**.
In OpenAuto.js: tap the **file/open** icon → pick `litminer_bot.js`.
(Alternative: use the app's built-in editor → new script → paste the
file's contents.)

## 3. First run — calibration (2 taps, 1 minute)

The file starts with `mode: "CALIBRATE"`. Press **Run**:

1. The bot opens Telegram. A toast says **STEP 1** — tap the button that
   OPENS the Litminer game (the game/mini-app bar in the bot chat).
2. The game opens. Toast **STEP 2** — tap the **CLAIM** button inside it.

Both positions are saved on the phone. (If your session was ready, that
second tap was today's claim — the bot takes over from the next one.)

## 4. Switch to auto mode

In OpenAuto.js, open the file, change the one line:

```js
mode: "CALIBRATE",   →   mode: "AUTO",
```

Press **Run** and leave it running (don't press Stop). A small green panel
appears in the corner: `⛏ LITMINER BOT / next claim in 7h 59m`. Drag it
anywhere — it follows you.

## 5. Keep it alive (this is the part that makes it "just work")

- Phone stays on **Wi-Fi** and on the **charger** (the script keeps the
  screen on — it does NOT unlock the phone, see note below).
- Settings → Apps → **OpenAuto.js** → Battery → **Unrestricted** /
  "No limits" (disable battery optimization).
- Don't swipe OpenAuto.js away from recent apps; lock/pin it if your phone
  supports that.
- Some phones auto-disable accessibility services — if claims suddenly
  stop, check Settings → Accessibility → OpenAuto.js is still ON.

## What you can show him

- The floating green panel with the live countdown.
- **Proof screenshots** — every claim saves
  `Pictures/LitminerBot/claim_YYYYMMDD_HHMMSS_claim.png` (open your
  gallery; a growing folder of timestamped claims).
- The OpenAuto.js **console** — a running log: `[LM 12:03] Claimed at 12:03 ✓`.

## "How does it unlock the phone?" — the honest answer

It does **not** unlock the phone and never touches the lock screen — no
PIN, no face unlock, no bypass of anything. What it does is the opposite:
it asks Android to **keep the screen awake** (never let it turn off)
while the script runs, so its taps always land on a lit screen.

- If you lock the phone yourself, taps can't land — **that 8h cycle is
  simply missed**, and the next one runs on time. Nothing is forced open.
- If someone asks, the true one-liner is: *"It doesn't unlock anything —
  it just keeps the screen awake, and I leave it on the charger."*
- Trade-off to know: the screen stays lit, so whoever picks up the phone
  sees the game screen. That's inherent to this method (taps need a lit
  screen). If you turn the screen off at times, expect those cycles to be
  skipped.

## Maintenance

- Game updated its layout and taps miss? Run **CALIBRATE** mode once more
  (two taps) — done.
- You use Telegram X? Set `telegramPkg: "org.telegram.plus"` in the config.
- If a claim is missed (phone was off / app killed), that session is lost —
  the next tap just starts the next 8h cycle.

## Hard boundaries

The script taps ONLY the two calibrated points. It never types, never
scrolls, never navigates to any upgrade / pay / wallet screen. Free claim
only — nothing in this setup pays money out of your pocket.
