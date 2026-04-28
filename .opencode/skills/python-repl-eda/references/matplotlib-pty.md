# Matplotlib in PTY — Detailed Reference

## Backend Setup (Critical)

```python
import matplotlib
matplotlib.use('Agg')  # MUST be BEFORE importing pyplot
import matplotlib.pyplot as plt
```

If you import pyplot before setting the backend, the Agg backend won't take effect and `plt.show()` will try to open a GUI window (which hangs in PTY).

## Figure Directory Setup

```python
import os
os.makedirs('data/figures', exist_ok=True)
```

## Common Plot Types

### Heatmap (pcolormesh)

```python
fig, ax = plt.subplots(figsize=(10, 8))
im = ax.pcolormesh(lon_grid, lat_grid, data, cmap='RdBu_r', shading='auto')
fig.colorbar(im, ax=ax, label='Units')
plt.tight_layout()
plt.savefig('data/figures/name.png', dpi=120)
plt.close()
```

### Line Plot with Multiple Series

```python
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y1, 'r-', label='Series 1')
ax.plot(x, y2, 'b--', label='Series 2')
ax.legend()
ax.grid(True)
plt.tight_layout()
plt.savefig('data/figures/name.png', dpi=120)
plt.close()
```

### Scatter

```python
fig, ax = plt.subplots(figsize=(8, 8))
sc = ax.scatter(x, y, c=color_var, cmap='viridis', s=30, alpha=0.6)
fig.colorbar(sc, ax=ax, label='Color label')
plt.tight_layout()
plt.savefig('data/figures/name.png', dpi=120)
plt.close()
```

### Histogram

```python
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(data, bins=50, edgecolor='black', alpha=0.7)
plt.tight_layout()
plt.savefig('data/figures/name.png', dpi=120)
plt.close()
```

### Subplots

```python
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes[0, 0].plot(...)
axes[0, 1].plot(...)
# ... etc
plt.tight_layout()
plt.savefig('data/figures/name.png', dpi=120)
plt.close()
```

## Memory Management

Always call `plt.close()` after `plt.savefig()`. Without it, figures accumulate in memory and the REPL session grows.

## Arrow Plotting Performance

For large graphs (N > 100 edges), `ax.arrow()` is slow. Use `LineCollection` or skip arrows entirely.
