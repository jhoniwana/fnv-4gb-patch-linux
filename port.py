#!/usr/bin/env python3
"""FNV 4GB Patcher - Linux port.

Applies the 4GB patch to FalloutNV.exe using the native ELF
FalloutNVPatcher (the "for Proton" build of the mod). No Wine.

The ELF runs from the game directory and modifies FalloutNV.exe, creating
FalloutNV_backup.exe. NOTE: the ELF exits with code 0 even on failure
("FalloutNV.exe not found!") - success is detected by the presence of the
backup file.

Usage:
  python3 port.py [--game-dir DIR]
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PATCHER = HERE / "FalloutNVPatcher"
GAME_DIR_NAME = "Fallout New Vegas"
STEAM_LIBRARIES = [
    Path.home() / ".steam/steam/steamapps",
    Path.home() / ".local/share/Steam/steamapps",
    Path("/mnt/games/steamapps"),
]


def info(msg):
    print(f"  i {msg}", flush=True)


def ok(msg):
    print(f"  + {msg}", flush=True)


def fail(msg, code=1):
    print(f"  ! {msg}", flush=True)
    return code


def find_game():
    for lib in STEAM_LIBRARIES:
        cand = lib / "common" / GAME_DIR_NAME
        if (cand / "FalloutNV.exe").exists():
            return cand
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--game-dir")
    args = ap.parse_args()

    game_dir = Path(args.game_dir) if args.game_dir else find_game()
    if game_dir is None:
        return fail("game not found - use --game-dir")
    if not PATCHER.exists():
        return fail(f"{PATCHER.name} missing from the repo")

    if (game_dir / "FalloutNV_backup.exe").exists():
        ok("FalloutNV.exe already patched (backup exists)")
        return 0

    dst = game_dir / "FalloutNVPatcher"
    shutil.copy2(PATCHER, dst)
    dst.chmod(0o755)
    info("patching FalloutNV.exe (native ELF)...")
    r = subprocess.run([str(dst)], cwd=str(game_dir), capture_output=True,
                       text=True, timeout=120)
    output = (r.stdout + r.stderr).strip()
    if (game_dir / "FalloutNV_backup.exe").exists():
        ok(f"FalloutNV.exe patched ({output[-60:] or 'backup created'})")
        return 0
    return fail(f"patcher did not create the backup. Output: {output[:120]}")


if __name__ == "__main__":
    sys.exit(main())
