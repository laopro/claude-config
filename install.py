#!/usr/bin/env python3
"""Instala, actualiza o quita la config de ahorro de tokens de Claude Code.

  python3 install.py               instala o actualiza (idempotente)
  python3 install.py --dry-run     muestra que cambiaria, sin escribir nada
  python3 install.py --uninstall   quita el hook y las reglas de este repo

Antes de cambiar settings.json guarda una copia: settings.json.bak-<fecha>.
Solo toca hooks.PreToolUse y permissions.deny; el resto de tu config no se modifica.
"""
import json, os, shutil, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
CLAUDE = os.path.join(os.path.expanduser("~"), ".claude")
HOOK_SRC = os.path.join(HERE, "hooks", "block-large-reads.py")
HOOK_DST = os.path.join(CLAUDE, "hooks", "block-large-reads.py")
SETTINGS = os.path.join(CLAUDE, "settings.json")
MARK = "block-large-reads"

DRY = "--dry-run" in sys.argv
UNDO = "--uninstall" in sys.argv

cfg = json.load(open(os.path.join(HERE, "config.json")))
s = json.load(open(SETTINGS)) if os.path.exists(SETTINGS) else {}
before = json.dumps(s, sort_keys=True)

hooks = s.get("hooks", {})
pre = [h for h in hooks.get("PreToolUse", [])
       if not any(MARK in c.get("command", "") for c in h.get("hooks", []))]
if not UNDO and cfg["max_read_kb"] > 0:
    pre.append({"matcher": "Read", "hooks": [{
        "type": "command",
        "command": f"python3 -I {HOOK_DST} {cfg['max_read_kb']}",
        "timeout": 5}]})
if pre:
    hooks["PreToolUse"] = pre
else:
    hooks.pop("PreToolUse", None)
if hooks:
    s["hooks"] = hooks
else:
    s.pop("hooks", None)

deny = s.get("permissions", {}).get("deny", [])
if UNDO:
    deny = [d for d in deny if d not in cfg["denied_tools"]]
else:
    deny = deny + [d for d in cfg["denied_tools"] if d not in deny]
perms = s.get("permissions", {})
if deny:
    perms["deny"] = deny
else:
    perms.pop("deny", None)
if perms:
    s["permissions"] = perms
else:
    s.pop("permissions", None)

if DRY:
    print(json.dumps(s, indent=2, ensure_ascii=False))
    print("\n(dry-run: no se escribio nada)")
    sys.exit(0)

if json.dumps(s, sort_keys=True) == before and not UNDO:
    print("Sin cambios: ya estaba instalado.")
else:
    if os.path.exists(SETTINGS):
        bak = f"{SETTINGS}.bak-{time.strftime('%Y%m%d-%H%M%S')}"
        shutil.copy(SETTINGS, bak)
        print(f"Respaldo: {bak}")
    os.makedirs(os.path.dirname(SETTINGS), exist_ok=True)
    json.dump(s, open(SETTINGS, "w"), indent=2, ensure_ascii=False)
    print("settings.json actualizado.")

if UNDO:
    if os.path.exists(HOOK_DST):
        os.remove(HOOK_DST)
    print("Hook y reglas quitados.")
else:
    os.makedirs(os.path.dirname(HOOK_DST), exist_ok=True)
    shutil.copy(HOOK_SRC, HOOK_DST)
    print(f"Hook instalado en {HOOK_DST} (limite {cfg['max_read_kb']} KB).")
print("Reinicia Claude Code o usa /hooks.")
