# Python Line Editing Keys

Python REPL processes ANSI terminal control sequences:

| Key | Code | Effect |
|-----|------|--------|
| Backspace | `\x7f` | Deletes character before cursor |
| Ctrl+U | `\x15` | Clears entire line (kill to beginning) |
| Ctrl+K | `\x0b` | No visible effect in Python REPL |
| Ctrl+A | `\x01` | Moves cursor to beginning of line |
| Ctrl+E | `\x05` | Moves cursor to end of line |
| Cancel | `\x03` | KeyboardInterrupt — exits continuation cleanly |

## Backspace Behavior

**At empty prompt:** No-op
**With text:** Deletes character before cursor
**Multiple backspaces:** Sequentially delete characters
**In continuation (`...`):** Deletes character, can damage original line

## Canceling Continuation — Ctrl+C Preferred

**Ctrl+C (`\x03`) cleanly cancels continuation** and returns to `>>>` with no error:

```
>>> if True:
...     x = 1
\x03
KeyboardInterrupt
>>> _   # Clean, no error
```

**This is better than backspace** for canceling multi-line input — backspace can damage the original line.

## Recovery from Broken States

| Situation | Best Recovery |
|-----------|--------------|
| Stuck in continuation `...` | `pty_write(data="\x03\n")` — Ctrl+C then newline |
| Partially typed line at `>>>` | Send enough `\x7f` to clear, then `\n` |
| Damaged line (garbled) | `\n` to execute/ignore, then continue |
