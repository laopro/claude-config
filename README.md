# claude-config

Config para que Claude Code gaste menos tokens. Pensada para cualquiera, sin dependencias.

## Qué hace
- **Bloquea leer archivos grandes completos.** Por encima de `max_read_kb` (150 KB por defecto), Claude debe usar grep y luego leer por ventanas.
- **Desactiva herramientas pesadas.** Lo que pongas en `denied_tools`, por ejemplo capturas de pantalla.
- **Guarda respaldo** de tu `settings.json` antes de cambiar nada.

## Instalar
```bash
git clone <URL_DEL_REPO> ~/claude-config
python3 ~/claude-config/install.py --dry-run   # revisa antes
python3 ~/claude-config/install.py
```
Luego reinicia Claude Code o usa `/hooks`.

## Configurar
Edita `config.json`:
- `max_read_kb`: límite en KB. Pon `0` para desactivar el bloqueo de lecturas.
- `denied_tools`: nombres de herramientas a bloquear. Los nombres exactos aparecen en `/permissions`.

Vuelve a correr `install.py` después de cambiar algo.

## Quitar
```bash
python3 ~/claude-config/install.py --uninstall
```

## Hábitos que más ahorran (lo que la config no puede hacer)
- Usa `/clear` al cambiar de tema. Cada turno reenvía toda la conversación.
- Revisa qué ocupa el contexto con `/context`.
- Para algo simple, pide respuesta corta en la misma instrucción.
- `CLAUDE.example.md` tiene reglas cortas. Cópialo si quieres, pero mantenlo breve: se carga en cada turno.

## No subas nunca
`~/.claude/.credentials.json`, `history.jsonl`, `projects/` ni los respaldos `settings.json.bak-*`. Este repo no los incluye.
