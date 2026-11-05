"""Extract X (x.com) session cookies from the user's DESKTOP BROWSER profiles
and set the X_AUTH_TOKEN / X_CT0 user-level env vars that rag/x_browser_fetch.py
already reads (lines 37-43) to unlock the browser tier for X.

Why: anonymous X is login-walled; the user's X account is Google-only (no
password), so a fresh login in our headless Chromium is impossible (Google
blocks sign-ins in automation-flagged browsers). But the user's normal browser
(Edge) already carries a valid logged-in X session in its cookie store — we
just read it.

Scans (in order): Edge, Chrome, Brave — every profile dir that has a Cookies
DB. Decrypts v20/v10 cookies (DPAPI key from `Local State`). Picks the
candidate with BOTH auth_token + ct0 and the newest last_update_stamp, sets
HKCU\\Environment, prints a masked report. Read-only on the browser files.

Usage: python extract_x_cookies.py          (extract + set env)
       python extract_x_cookies.py --show   (report only, no env write)
"""
import base64
import ctypes
import json
import os
import sqlite3
import sys
import winreg
from datetime import datetime, timedelta, timezone

if sys.platform == "win32":
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

WIN_EPOCH = datetime(1601, 1, 1, tzinfo=timezone.utc)

BROWSERS = [
    ("Edge",  os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data")),
    ("Chrome", os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")),
    ("Brave", os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data")),
]


def dpapi_unprotect(data: bytes) -> bytes:
    buf_in = ctypes.create_string_buffer(data)
    buf_out = ctypes.c_char_p()
    CRYPTPROTECT_UI_FORBIDDEN = 0x01
    if not ctypes.windll.crypt32.CryptUnprotectData(
            buf_in, None, None, None, None, CRYPTPROTECT_UI_FORBIDDEN,
            ctypes.byref(buf_out)):
        raise RuntimeError("CryptUnprotectData failed (wrong user context?)")
    out = ctypes.string_at(buf_out)
    ctypes.windll.kernel32.LocalFree(buf_out)
    return out


def profile_key(local_state_path: str) -> bytes:
    with open(local_state_path, "r", encoding="utf-8") as f:
        js = json.load(f)
    enc_key = base64.b64decode(js["os_crypt"]["encrypted_key"])
    if enc_key[:5] != b"DPAPI":
        raise RuntimeError("unexpected os_crypt key format")
    return dpapi_unprotect(enc_key[5:])


def decrypt_cookie(encrypted: bytes, key: bytes) -> str:
    if encrypted[:3] == b"v20":
        # v20: 'v20' + 12-byte nonce + AES-256-GCM ciphertext + 16-byte tag
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        nonce, rest = encrypted[3:15], encrypted[15:]
        ct, tag = rest[:-16], rest[-16:]
        return AESGCM(key).decrypt(nonce, ct + tag, None).decode("utf-8", "replace")
    if encrypted[:3] == b"v10":
        # v10: 'v10' + 12-byte IV + ciphertext + 16-byte tag (768-byte buffer)
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        nonce, rest = encrypted[3:15], encrypted[15:]
        ct, tag = rest[:-16], rest[-16:]
        return AESGCM(key).decrypt(nonce, ct + tag, None).decode("utf-8", "replace")
    return encrypted.decode("utf-8", "replace")  # plaintext (older versions)


def stamp_to_dt(us: int) -> str:
    try:
        return (WIN_EPOCH + timedelta(microseconds=us)).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return "?"


def scan_browser(bname: str, user_data: str):
    """Return (browser, profile, {name: (value, stamp)} or None) for x.com cookies."""
    if not os.path.isdir(user_data):
        return None
    local_state = os.path.join(user_data, "Local State")
    if not os.path.isfile(local_state):
        return None
    profiles = ["Default"] + sorted(
        d for d in os.listdir(user_data)
        if d.startswith("Profile") and os.path.isdir(os.path.join(user_data, d)))
    for prof in profiles:
        # new Chromium layout: Cookies moved to <profile>/Network/Cookies
        candidates = [os.path.join(user_data, prof, "Cookies"),
                      os.path.join(user_data, prof, "Network", "Cookies")]
        db = next((c for c in candidates if os.path.isfile(c)), None)
        if not db:
            continue
        try:
            con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
            # schema varies across Chromium versions: pick an available stamp col
            cols = {r[1] for r in con.execute("PRAGMA table_info(cookies)")}
            stamp_col = next((c for c in ("last_update_stamp", "last_update_utc",
                                          "last_access_utc") if c in cols), None)
            sel = "SELECT name, encrypted_value, value" + (
                f", {stamp_col}" if stamp_col else ", 0")
            rows = con.execute(
                sel +
                " FROM cookies WHERE (host_key LIKE '%x.com%' OR "
                "host_key LIKE '%twitter.com%') "
                "AND name IN ('auth_token','ct0')").fetchall()
            con.close()
        except sqlite3.OperationalError as e:
            print(f"  {bname}/{prof}: DB busy ({e}) — is the browser running?")
            continue
        if not rows:
            continue
        try:
            key = profile_key(local_state)
        except Exception as e:
            print(f"  {bname}/{prof}: key read failed: {e}")
            continue
        found = {}
        for name, enc, plain, stamp in rows:
            if enc:
                try:
                    found[name] = (decrypt_cookie(enc, key), stamp)
                except Exception as e:
                    print(f"  {bname}/{prof}: {name} decrypt failed: {e}")
            elif plain:
                found[name] = (plain, stamp)
        if found:
            newest = max(found.values(), key=lambda t: t[1] or 0)
            print(f"  FOUND {bname}/{prof}: " + ", ".join(
                f"{n}={v[:4]}…{v[-4:]} (len {len(v)}, updated {stamp_to_dt(s or 0)})"
                for n, (v, s) in sorted(found.items())))
            return (bname, prof, found, newest[1])
    return None


def main():
    show_only = "--show" in sys.argv
    print("scanning desktop browser profiles for x.com session cookies...")
    best = None
    for bname, user_data in BROWSERS:
        res = scan_browser(bname, user_data)
        if res:
            _, _, found, stamp = res
            if best is None or (best[3] or 0) < (stamp or 0):
                best = res
    if not best:
        print("\nNO x.com auth_token/ct0 found in any browser profile.")
        print("=> the user is not logged into X in a desktop browser. "
              "One-time: open x.com in Edge, sign in with Google (works in the "
              "real browser), close Edge, re-run this script.")
        sys.exit(2)

    bname, prof, found, stamp = best
    if "auth_token" not in found or "ct0" not in found:
        print(f"\n{bname}/{prof} has {sorted(found)} but is missing "
              f"{['auth_token','ct0'][0] if 'auth_token' not in found else 'ct0'} — "
              "partial session; login may be incomplete.")

    if show_only:
        print("\n(--show: env vars NOT set)")
        return

    auth = found.get("auth_token", ("", None))[0]
    ct0 = found.get("ct0", ("", None))[0]
    if not (auth and ct0):
        print("refusing to set env without both cookies")
        sys.exit(3)

    k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0,
                       winreg.KEY_SET_VALUE)
    winreg.SetValueEx(k, "X_AUTH_TOKEN", 0, winreg.REG_SZ, auth)
    winreg.SetValueEx(k, "X_CT0", 0, winreg.REG_SZ, ct0)
    winreg.CloseKey(k)
    print(f"\nSET HKCU\\Environment X_AUTH_TOKEN ({auth[:4]}…{auth[-4:]}, len {len(auth)})"
          f" and X_CT0 ({ct0[:4]}…{ct0[-4:]}) — from {bname}/{prof} "
          f"(updated {stamp_to_dt(stamp or 0)}).")
    print("New processes (incl. the 08:00 daily task and future agent shells) pick "
          "these up automatically.")


if __name__ == "__main__":
    main()
