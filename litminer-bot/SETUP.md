# Litminer Bot — phone-only setup (3 steps, tonight)

Everything runs on the phone in **AutoJs6** (the app you already use).
No PC, no ADB, no auto-clicker. The bot taps ONE button every 8 hours.

## Step 1 — Calibrate once (1 minute)

1. Open AutoJs6 → open the file **`litminer_bot.js`** (keep the first line
   `mode: "CALIBRATE"` as it is).
2. Press **Run**. A green panel appears.
3. Follow the 2 toasts:
   - **STEP 1** → tap the button that OPENS the Litminer game.
   - **STEP 2** → tap the **CLAIM** button inside the game.
4. Toast **STEP 3 DONE** appears. Both positions are now saved on the phone.

## Step 2 — Switch to TAP mode and run it

1. In AutoJs6, open `litminer_bot.js` again and change the one line:

   ```js
   mode: "CALIBRATE"   →   mode: "TAP"
   ```

2. Press **Run** and **leave it running** (don't press Stop, don't close the
   app from recent-apps).
3. Leave the phone **on the game screen**, on **Wi-Fi + charger**.
   That's it — the bot taps the claim button for you every 8 hours.

**Why TAP mode?** It's the version that cannot break: it never opens apps,
never searches, never navigates — it only taps the one button it calibrated.
The only requirement: the phone stays on that screen (screen stays awake).

## Step 3 — Keep it alive

- Settings → Apps → **AutoJs6** → Battery → **Unrestricted / No limits**.
- Don't swipe AutoJs6 away from recent apps.
- If claims stop: Settings → Accessibility → AutoJs6 must still be ON.

## What to show him

- The floating panel with the live countdown (`next claim in 7h 59m`).
- **Proof screenshots** — every claim saves a timestamped PNG in
  `Pictures/LitminerBot/` (a growing folder in the gallery).
- The AutoJs6 **console** — a running log: `[LM 12:03] Claimed at 12:03 ✓`.

## The honest answer to "does it unlock the phone?"

It does **not**. It keeps the screen **awake** (never lets it turn off) so its
tap lands on a lit screen. If you lock the phone yourself, that 8h cycle is
simply missed — the next one runs on time. One-liner: *"It doesn't unlock
anything — it just keeps the screen awake, and I leave it on the charger."*

## If something breaks

- **Game updated its layout and taps miss?** Set `mode: "RECALIBRATE"`, run,
  do the 2 taps, switch back to `TAP`. Done.
- **Using Telegram X?** Set `telegramPkg: "org.telegram.plus"` in the file.
- **Missed a cycle** (phone off / app killed)? No problem — the next tap
  starts the next 8h cycle.

## Hard boundaries

The script taps ONLY the calibrated button. It never types, never scrolls,
never opens any upgrade / pay / wallet screen. Free claim only — nothing in
this setup spends a single rupee.

---

### PC / emulator version (in progress, not needed tonight)

A headless Android emulator on the PC (same AutoJs6) is being built so the
bot can run without touching the phone. Once the emulator boots and the
API probe runs, this file gains a "PC mode" section. The phone script above
works regardless.
