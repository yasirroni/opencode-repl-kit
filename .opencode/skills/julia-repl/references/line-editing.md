# Julia Line Editing Keys

Julia REPL processes full ANSI terminal line-editing sequences:

| Key | Code | Effect |
|-----|------|--------|
| Backspace | `\x7f` | Deletes character before cursor (multiple work sequentially) |
| Ctrl+U | `\x15` | Clears entire line (kill to beginning) |
| Ctrl+K | `\x0b` | Kills from cursor to end of line |
| Ctrl+A | `\x01` | Moves cursor to beginning of line |
| Ctrl+E | `\x05` | Moves cursor to end of line |
| Cancel | `\x03` | Cancels continuation/partial input, prints `^C`, returns to prompt |

## In `pkg>` Mode

Backspace `\x7f` exits `pkg>` and returns to `julia>`. No other line-editing keys needed in pkg mode.

## Comparison with Other Languages

Julia has the most complete line editing support of the three languages:

| Feature | Python | MATLAB | Julia |
|---------|--------|--------|-------|
| Backspace | `\x7f` ✓ | `\x08` ✓ | `\x7f` ✓ |
| Clear line (Ctrl+U) | ✓ | ✗ | ✓ |
| Kill to EOL (Ctrl+K) | ~ (no effect) | ✗ | ✓ |
| Move to BOL (Ctrl+A) | ✓ | ✗ | ✓ |
| Move to EOL (Ctrl+E) | ✓ | ✗ | ✓ |
| Cancel (Ctrl+C) | ✓ | ✓ | ✓ |
