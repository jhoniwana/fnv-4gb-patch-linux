# FNV 4GB Patcher — Linux Port

Port nativo a Linux del [FNV4GB Patcher (for Proton)](https://www.nexusmods.com/newvegas/mods/62552). Sin Wine: el patcher incluido (`FalloutNVPatcher`) es la build **ELF nativo Linux** ("for Proton") del mod.

## Uso

```bash
python3 port.py [--game-dir /ruta/al/juego]
```

## Qué hace

1. Copia `FalloutNVPatcher` (ELF) al directorio del juego
2. Lo ejecuta → modifica `FalloutNV.exe` (heap de 4GB)
3. Verifica el éxito por la existencia de `FalloutNV_backup.exe` (el ELF sale con código 0 incluso si falla)

Verificado en juego real: `FalloutNV.exe patched!` + backup creado.

## Notas

- En Steam se usa ESTE patcher. El **Epic Games Patcher** (también del pack) es SOLO para la versión EGS — ver `epic-games-patcher-linux`.
- El `FalloutNV.exe` parcheado sigue matcheando los SHA1 soportados del instalador de UE ESM Fixes (hash `0021023E...` en la lista del autor).
