"""PreToolUse hook para Read: bloquea leer archivos grandes completos.
Uso: python3 -I block-large-reads.py <max_kb>
Si Claude pasa offset o limit, la lectura se permite (ya es parcial)."""
import json, os, sys

MAX_KB = int(sys.argv[1]) if len(sys.argv) > 1 else 150
LIMIT = MAX_KB * 1024

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

inp = data.get("tool_input", {}) or {}
if inp.get("offset") is not None or inp.get("limit") is not None:
    sys.exit(0)

try:
    size = os.path.getsize(inp.get("file_path", ""))
except OSError:
    sys.exit(0)

if size > LIMIT:
    reason = (f"El archivo pesa {size // 1024} KB y el limite es {MAX_KB} KB. "
              "No lo leas completo: usa grep para ubicar lo necesario y luego Read "
              "con offset y limit (ventanas de 100-200 lineas).")
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason}}))
sys.exit(0)
