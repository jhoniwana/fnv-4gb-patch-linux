# FNV 4GB Patcher — Linux Port

Native Linux port of the [FNV4GB Patcher (for Proton)](https://www.nexusmods.com/newvegas/mods/62552). No Wine: the included `FalloutNVPatcher` is the **native Linux ELF** ("for Proton") build of the mod.

## Usage

```bash
python3 port.py [--game-dir /path/to/game]
```

## What it does

1. Copies `FalloutNVPatcher` (ELF) to the game directory
2. Runs it → modifies `FalloutNV.exe` (4GB heap)
3. Verifies success by the presence of `FalloutNV_backup.exe` (the ELF exits with code 0 even on failure)

Verified on a real game: `FalloutNV.exe patched!` + backup created.

## Notes

- Use THIS patcher on Steam. The **Epic Games Patcher** (from the same pack) is ONLY for the EGS version — see `epic-games-patcher-linux`.
- The patched `FalloutNV.exe` still matches the SHA1s supported by the UE ESM Fixes installer (hash `0021023E...` in the author's list).
