# Android emulator rig — state (2026-10-28, IST)

## BREAKTHROUGHS (late segment)
1. `qemu-system-x86_64-headless.exe` IS the emulator binary itself (usage header:
   "Android Emulator usage: emulator [options] [-qemu args]") — it takes EMULATOR
   options, NOT raw QEMU options. Raw QEMU args (`-m`, `-mem-path`, `-nodefaults`)
   → "unknown option" → silent exit code 1. All "silent death" direct runs were this.
2. That binary needs ~20 DLLs beside it (libandroid-emu-*, libglib2, liblibprotobuf,
   libvulkan_lvp, vulkan-1, d3dcompiler_47, libEGL/libGLESv2, ...). They live in
   sdk\emulator and sdk\emulator\lib64 — NOT on the default DLL search path from
   the exe dir (qemu\windows-x86_64). FIXED by copying all of them into the exe dir
   (done 2026-10-28). After that the binary starts and boots the guest.
3. Two-port form is `-ports 5555,5554` (`-port` takes a single integer).
4. Useful headless flags (from -help): `-show-kernel` (guest kernel messages to
   console), `-skip-adb-auth`, `-delay-adb`, `-detect-image-hang`,
   `-restart-when-stalled`, `-quit-after-boot <s>`, `-logcat-output <file>`,
   `-shell`, `-shell-serial <dev>`, `-memory <MB>` (not -m), `-cores <n>`.
5. Stale `.lock` files in the AVD dir → infinite "error: 5" flood (2.7 GB of log in
   one run). The emulator creates locks with CREATE_NEW semantics. Keep the AVD dir
   clean of .lock files; the emulator makes them.
6. `snapshots/default_boot/` dir must PRE-EXIST (qemu -mem-path points into it;
   the emulator does not create the dir itself). Created 2026-10-28.
7. The AVD dir now holds all generated files (initrd 2.18MB, hardware-qemu.ini
   4.3KB, cache.img + cache.img.qcow2, userdata-qemu.img + .qcow2,
   encryptionkey.img + .qcow2, snapshots/default_boot/ram.img 4.3GB = guest RAM
   file-backed, modem_simulator/, data/).
8. Event-log: crashpad_handler.exe (emulator's crash reporter) faults 0x80000003 at
   every emulator start (confined-context crashpad init failure) — benign-ish; the
   emulator itself survives. adb.exe loop-crashed in the earlier daemon attempts.
9. `parse_imports.py` / `check_deps.py` (workspace) — PE import-table parsers used
   to locate the missing-DLL problem (exit code 0xC0000135 = STATUS_DLL_NOT_FOUND
   is the signature of a missing DLL; the process exits before printing anything).
10. api-ms-win-crt-*.dll "missing" is a false positive: they are API-set virtual
    entries resolved by the loader, not files.

## Launch (current working way)
`D:\models\vsCodeMcp\android-emulator\boot_headless2.cmd` — runs
`qemu-system-x86_64-headless.exe` from its own dir with:
 -avd lm16 -memory 4096 -cores 4 -no-accel -no-window -no-audio -no-boot-anim
 -gpu off -no-snapshot-load -no-snapshot-save -no-metrics -show-kernel
 -skip-adb-auth -detect-image-hang -restart-when-stalled -ports 5555,5554
(TEMP/TMP pinned to workspace tmp\).
Legacy: `boot_emu.cmd` (emulator.exe, same flags, file stdout to emu_out.log).
Scheduled task `LmEmu` DELETED 2026-10-29 (recreate with:
`schtasks /create /tn LmEmu /tr "cmd.exe /c D:\models\vsCodeMcp\android-emulator\boot_headless2.cmd" /sc once /st 09:00` if wanted).

## Boot status — VERDICT (2026-10-29 00:10 IST): guest never boots on this machine
No run reached a bootable guest (no adbd answer, no serial/kernel output, no
sys.boot_completed). Two distinct failure points observed:

(A) Headless binary (`boot_headless2.cmd`, qemu-system-x86_64-headless.exe):
    dies right after netsim startup, BEFORE "Starting QEMU main loop".
    - With crashpad_handler present: process survives but DEADLOCKS — all 132
      threads in Wait state, guest-CPU flat ~0.2s at t=90s AND t=6min. The
      fatal error is caught by crashpad's handler, which is itself broken in
      this confined context (crashpad_handler faults 0x80000003 at every
      start) → process hangs in the handler path.
    - With crashpad_handler renamed away: the same fatal error is uncaught →
      clean BEX64 fastfail, faulting module ucrtbase.dll, 0xC0000409
      (STATUS_STACK_BUFFER_OVERRUN), P9=7 (FATAL_APP_EXIT), t<90s.
    So a fatal C++ abort fires early in this binary; crashpad presence only
    changes hang-vs-exit, not whether it happens.

(B) emulator.exe verbose (boot_emu.cmd -verbose): the ONLY run that reached
    the guest. Log shows "Starting QEMU main loop" + `android_fopen:
    /qemu.conf err: 2` (guest→host RPC = guest firmware ran ~0.2s), then the
    guest STALLS: CPU flat, adbd port 5554 pre-bound but never answers
    (raw `host:version` → 15s timeout, 0 bytes), no serial output even with
    -show-kernel, pstore crash file never created (guest didn't even panic).

Ruled out as the cause: WHPX availability (vmcompute stopped but "WHPX
installed and usable"; -no-accel TCG gives the same stall), DSH confinement
(same behavior via schtasks LmEmu OUTSIDE the DSH process tree), missing
system-image files (all present), stale .lock files (fixed; no change),
missing snapshots/default_boot dir (created; no change), stdout pipe deadlock
(file stdout; no change).

Root cause NOT pinned down. Two open hypotheses, indistinguishable with the
tools available tonight:
  1. An early fatal error in the emulator process (environmental) — the
     headless binary's ucrtbase abort. If so, the guest never even starts.
  2. A guest vCPU that never gets scheduled (hypervisor layer) — the verbose
     run's guest-firmware-then-stall. If so, the guest starts but never runs.
Likely machine-specific (AMD Zen 5 Family 26, Windows 11 26100, WHPX present
but guest never scheduled / emulator aborts). NOT a config bug — every launch
context reproduces the same no-boot outcome.

Decision (2026-10-29): PARKED for tonight. The phone bot (litminer-bot/,
TAP mode) is the ship path. If resumed tomorrow, options in order:
  (a) different machine — cloud VM with nested virt, or another local PC.
  (b) try a different system image (android-35 / x86_64) and/or different AVD
      (more cores); the android-36 image may be the trigger.
  (c) fully enable Hyper-V + reboot (vmcompute service currently Stopped),
      then retry WHPX.
  (d) capture a proper crash dump of the ucrtbase fastfail (needs a debugger
      / WER full dump) to see the aborting call stack — the decisive test.

## What works
- SDK at `D:\models\vsCodeMcp\android-emulator\sdk` (cmdline-tools, platform-tools,
  emulator 37.2.12, system-image android-36 google_apis x86_64).
- AVD `lm16` — the emulator resolves it to `C:\Users\user\.android\avd\lm16.avd`,
  which is a JUNCTION → `D:\models\vsCodeMcp\android-emulator\avds\lm16.avd`
  (workspace). The whole `C:\Users\user\.android` is also a junction →
  `D:\models\vsCodeMcp\android-emulator\home\.android`. This lets the
  sandbox-confined emulator.exe write all its state (it can only write to the
  workspace).
- Raw-socket adb client `emu_adb.ps1` (port 5554, no adb daemon needed).
- AutoJs6 protocol decoded from source (see PROTOCOL.md).
- AutoJs6 headless run path: `am start -n org.autojs.autojs6/.external.open.RunIntentActivity
  -a android.intent.action.VIEW -d file:///sdcard/script.js` — verified from
  RunIntentActivity.java + ScriptIntents.kt (runs the file's script).
- Accessibility service class: org.autojs.autojs6/org.autojs.autojs.core.accessibility.AccessibilityServiceUsher
- APK: `apks\autojs6-v6.7.0-x86_64.apk` (verified 143,874,294 bytes).
- Pipeline script: `pipeline.ps1` (install → perms → launch → run probe → cat report).

## Launch (the only working way so far)
`cmd /c D:\models\vsCodeMcp\android-emulator\boot_emu.cmd`
(sets TEMP/TMP to workspace tmp\, runs emulator with:
 -avd lm16 -no-window -no-audio -no-boot-anim -gpu off -memory 4096 -cores 4
 -no-accel -no-snapshot-load -no-snapshot-save -no-metrics
 >> emu_out.log 2>&1)

## Failure modes discovered (all fixed or worked around)
1. `emu-last-feature-flags.protobuf.lock (error: 5)` loop — confined emulator
   can't create files outside workspace. FIXED by junctioning .android to workspace.
2. Pre-created `.lock` files → "another process has lock" FATAL. DO NOT
   pre-create lock files — the emulator wants to create them itself
   (CREATE_NEW semantics). AVD dir must contain only config.ini (fresh).
3. "A snapshot operation for 'lm16' is pending and timeout has expired" —
   symptom of the lock failures above.
4. Guest VM stalls at ~0 CPU after early init — correlates with (a) stdout
   being a pipe (pipe-fill deadlock hypothesis) and (b) the snapshot.lock.lock
   error flood (2.7 GB of log in one run). Current launch avoids both
   (file stdout, clean AVD dir).
5. adb daemon unusable (confined, can't create Temp\adb.log). Bypassed via
   raw socket to 5554.
6. Emulator ignores ANDROID_AVD_HOME env — it always uses
   C:\Users\user\.android (junctioned to workspace).

## Next steps when guest boots (port 5554 stable + getprop sys.boot_completed=1)
1. `pipeline.ps1` (push APK, pm install, appops all-files, enable accessibility,
   am start splash, push emulator_probe.js, run via RunIntentActivity,
   cat /sdcard/lm_probe_report.txt).
2. From the probe report: confirm which launch APIs exist in AutoJs6 6.7.0
   (x86_64 build), patch litminer_bot.js open-link logic to proven functions.
3. Final deliverables: litminer_bot.js + 3-step user instructions (SETUP.md).

## Phone bot (separate, COMPLETE)
`D:\models\vsCodeMcp\litminer-bot\litminer_bot.js` v10 — TAP mode is the
recommended ship path (calibrate once, mode:"TAP", leave phone on game screen).
Bug fixed 2026-10-28: TAP mode no longer presses BACK after the claim tap
(that would have closed the game and broken later cycles).
