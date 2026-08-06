#!/usr/bin/env python3
"""FNV 4GB Patcher — Linux port.

Aplica el parche de 4GB a FalloutNV.exe usando el ELF nativo
FalloutNVPatcher (la build "for Proton" del mod). Sin Wine.

El ELF corre desde el directorio del juego y modifica FalloutNV.exe
creando FalloutNV_backup.exe. ⚠️ El ELF sale con código 0 incluso si
falla ("FalloutNV.exe not found!") → el éxito se detecta por la
existencia del backup.

Uso:
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
    print(f"  ℹ {msg}", flush=True)


def ok(msg):
    print(f"  ✔ {msg}", flush=True)


def fail(msg, code=1):
    print(f"  ✘ {msg}", flush=True)
    return code


def buscar_juego():
    for lib in STEAM_LIBRARIES:
        cand = lib / "common" / GAME_DIR_NAME
        if (cand / "FalloutNV.exe").exists():
            return cand
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--game-dir")
    args = ap.parse_args()

    game_dir = Path(args.game_dir) if args.game_dir else buscar_juego()
    if game_dir is None:
        return fail("no encontré el juego — usá --game-dir")
    if not PATCHER.exists():
        return fail(f"falta {PATCHER.name} en el repo")

    if (game_dir / "FalloutNV_backup.exe").exists():
        ok("FalloutNV.exe ya estaba parcheado (existe el backup)")
        return 0

    dst = game_dir / "FalloutNVPatcher"
    shutil.copy2(PATCHER, dst)
    dst.chmod(0o755)
    info("parcheando FalloutNV.exe (ELF nativo)...")
    r = subprocess.run([str(dst)], cwd=str(game_dir), capture_output=True,
                       text=True, timeout=120)
    salida = (r.stdout + r.stderr).strip()
    if (game_dir / "FalloutNV_backup.exe").exists():
        ok(f"FalloutNV.exe parcheado ({salida[-60:] or 'backup creado'})")
        return 0
    return fail(f"el patcher no creó el backup. Salida: {salida[:120]}")


if __name__ == "__main__":
    sys.exit(main())
