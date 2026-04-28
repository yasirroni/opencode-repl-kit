#!/usr/bin/env python
"""
Spatial Network EDA — Exploratory Data Analysis via REPL
=========================================================
This script is the consolidated output of iterative REPL exploration.
Each `# %%` block corresponds to one exploration phase.

Key REPL insight: All data was loaded ONCE and stays in memory across phases.
This is what makes REPL EDA superior to writing a package — state preservation
across iterative exploration.

Run end-to-end: python scripts/eda_spatial_network.py
Compatible with jupytext: jupytext --to notebook scripts/eda_spatial_network.py
"""

# %% [markdown]
# # Spatial Network EDA
# Exploratory analysis of gridded atmospheric data and network topology.
#
# **Data:**
# - `data/grid_data.nc` — 50×50×10 atmospheric grid (temperature, pressure, humidity)
# - `data/nodes.arrow` — 200 network nodes with measured values
# - `data/edges.arrow` — 500 directed edges with distance/weight/terrain
#
# **Key findings:**
# - Temperature: lapse rate visible (224K surface → 283K at alt 9 due to inversion)
# - Network: 10 connected components, largest has 182/200 nodes, 6 isolated nodes
# - Node-grid integration: Temperature RMSE 1.56K, 11 outlier nodes
# - Edge weight strongly correlated with distance (r=0.914), terrain effects minor

# %%
# Imports and configuration
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import xarray as xr
import pyarrow.feather as ff
import numpy as np
import pandas as pd
import os
from collections import defaultdict

os.makedirs('data/figures', exist_ok=True)

# %%
# Load data (Phase A)
# Data stays in memory for all subsequent phases — this is the REPL advantage.

print("Loading grid data...")
ds = xr.open_dataset('data/grid_data.nc')
ds.load()
print(f"Grid: dims={ds.dims}")

print("Loading nodes...")
nodes_df = ff.read_table('data/nodes.arrow').to_pandas()
print(f"Nodes: {nodes_df.shape[0]} rows")

print("Loading edges...")
edges_df = ff.read_table('data/edges.arrow').to_pandas()
print(f"Edges: {edges_df.shape[0]} rows")

print("\n=== GRID NaN counts ===")
for var in ['temperature', 'pressure', 'humidity']:
    n_nan = np.isnan(ds[var].values).sum()
    total = ds[var].values.size
    print(f"  {var}: {n_nan}/{total} ({n_nan/total*100:.1f}%)")

print("\n=== Nodes NaN counts ===")
print(nodes_df.isnull().sum())

# %% [markdown]
# ## Grid Data Exploration (Phase B)
# Vertical profiles show temperature inversion (colder at surface, warmer at altitude).
# This is physically unrealistic — suggests the lapse rate model direction is reversed
# in the data generation, or there's a cold-surface boundary condition.

# %%
# Grid exploration
LAT_SIZE, LON_SIZE, ALT_SIZE = 50, 50, 10

alt = ds.alt.values
lats = ds.lat.values
lons = ds.lon.values

temp_mean = ds.temperature.mean(dim=['lat', 'lon'])
pres_mean = ds.pressure.mean(dim=['lat', 'lon'])
hum_mean = ds.humidity.mean(dim=['lat', 'lon'])

print("Vertical profiles:")
print(f"  Temperature: alt=0 -> {float(temp_mean.isel(alt=0)):.1f}K, alt=9 -> {float(temp_mean.isel(alt=9)):.1f}K")
print(f"  Pressure: alt=0 -> {float(pres_mean.isel(alt=0)):.2f}hPa, alt=9 -> {float(pres_mean.isel(alt=9)):.2f}hPa")
print(f"  Humidity: alt=0 -> {float(hum_mean.isel(alt=0)):.1f}%, alt=9 -> {float(hum_mean.isel(alt=9)):.1f}%")

print(f"\nTerrain elevation: min={float(ds.elevation.values.min()):.0f}m, "
      f"max={float(ds.elevation.values.max()):.0f}m, "
      f"mean={float(ds.elevation.values.mean()):.0f}m")

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].plot(temp_mean.values, alt, 'r-', lw=2)
axes[0].set_xlabel('Temperature (K)'); axes[0].set_ylabel('Altitude level')
axes[0].set_title('Temperature Profile'); axes[0].grid(True)

axes[1].plot(pres_mean.values, alt, 'b-', lw=2)
axes[1].set_xlabel('Pressure (hPa)'); axes[1].set_title('Pressure Profile'); axes[1].grid(True)

axes[2].plot(hum_mean.values, alt, 'g-', lw=2)
axes[2].set_xlabel('Humidity (%)'); axes[2].set_title('Humidity Profile'); axes[2].grid(True)

plt.tight_layout()
plt.savefig('data/figures/vertical_profiles.png', dpi=120)
plt.close()
print("Saved vertical_profiles.png")

# Grid slices
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for idx, k in enumerate([0, 5, 9]):
    temp_slice = ds.temperature.sel(alt=float(k))
    im = axes[idx].pcolormesh(lons, lats, temp_slice.values, cmap='RdBu_r', shading='auto')
    axes[idx].set_xlabel('Longitude'); axes[idx].set_ylabel('Latitude')
    axes[idx].set_title(f'Temperature at alt={k}')
    fig.colorbar(im, ax=axes[idx], label='K')
plt.tight_layout()
plt.savefig('data/figures/grid_temp_slices.png', dpi=120)
plt.close()
print("Saved grid_temp_slices.png")

# Elevation
fig, ax = plt.subplots(figsize=(10, 8))
im = ax.pcolormesh(lons, lats, ds.elevation.values, cmap='terrain', shading='auto')
ax.set_xlabel('Longitude'); ax.set_ylabel('Latitude'); ax.set_title('Terrain Elevation')
fig.colorbar(im, ax=ax, label='m')
plt.tight_layout()
plt.savefig('data/figures/grid_elevation.png', dpi=120)
plt.close()
print("Saved grid_elevation.png")

# Zonal mean
temp_zonal = ds.temperature.mean(dim='lon')
zonal_mean = temp_zonal.mean(dim='alt')
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(lats, zonal_mean.values, 'r-', lw=2)
ax.set_xlabel('Latitude'); ax.set_ylabel('Temperature (K)')
ax.set_title('Zonal Mean Temperature'); ax.grid(True)
plt.tight_layout()
plt.savefig('data/figures/zonal_mean_temp.png', dpi=120)
plt.close()
print("Saved zonal_mean_temp.png")

# %% [markdown]
# ## Network Topology (Phase C)
# The network has 10 connected components. The largest component dominates (182 nodes).
# There are 6 isolated nodes (degree=0). Node types: sensors most common, relays least.

# %%
# Network topology
n_nodes = int(nodes_df['id_node'].max()) + 1
n_edges = len(edges_df)

in_degree = np.zeros(n_nodes, dtype=int)
out_degree = np.zeros(n_nodes, dtype=int)

for _, row in edges_df.iterrows():
    src = int(row['id_edge_from'])
    dst = int(row['id_edge_to'])
    out_degree[src] += 1
    in_degree[dst] += 1

total_degree = in_degree + out_degree

print(f"Nodes: {n_nodes}, Edges: {n_edges}")
print(f"Isolated (degree=0): {(total_degree == 0).sum()}")
print(f"Degree: min={total_degree.min()}, max={total_degree.max()}, mean={total_degree.mean():.2f}")

parent = np.arange(n_nodes)
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[rb] = ra

for _, row in edges_df.iterrows():
    union(int(row['id_edge_from']), int(row['id_edge_to']))

root_to_size = defaultdict(int)
for i in range(n_nodes):
    root_to_size[find(i)] += 1

comp_sizes = list(root_to_size.values())
print(f"Connected components: {len(comp_sizes)}, largest={max(comp_sizes)}")

print("\nNode types:")
print(nodes_df['node_type'].value_counts())

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].hist(in_degree[in_degree > 0], bins=30, edgecolor='black', alpha=0.7, color='blue')
axes[0].set_xlabel('In-degree'); axes[0].set_ylabel('Count')
axes[0].set_title('In-Degree Distribution'); axes[0].grid(True)

axes[1].hist(out_degree[out_degree > 0], bins=30, edgecolor='black', alpha=0.7, color='orange')
axes[1].set_xlabel('Out-degree'); axes[1].set_ylabel('Count')
axes[1].set_title('Out-Degree Distribution'); axes[1].grid(True)
plt.tight_layout()
plt.savefig('data/figures/degree_distribution.png', dpi=120)
plt.close()
print("Saved degree_distribution.png")

# %% [markdown]
# ## Node-Grid Integration (Phase D)
# Node elevation matches grid elevation exactly (RMSE=0) — expected since nodes are
# sampled directly from the grid. Temperature residuals show RMSE=1.56K with
# 11 outlier nodes (>2 std dev). Spatial autocorrelation of residuals is weak.

# %%
# Node-grid integration
lat_all = ds.lat.values
lon_all = ds.lon.values
elev_grid = ds.elevation.values
temp_grid = ds.temperature.sel(alt=0).values

lats = nodes_df['latitude'].values
lons = nodes_df['longitude'].values

lat_idx = np.clip(np.searchsorted(lat_all, lats), 0, LAT_SIZE - 1)
lon_idx = np.clip(np.searchsorted(lon_all, lons), 0, LON_SIZE - 1)

grid_elev_at_nodes = elev_grid[lat_idx, lon_idx]
grid_temp_at_nodes = temp_grid[lat_idx, lon_idx]
node_elev = nodes_df['elevation'].values
node_temp = nodes_df['measured_temp'].values

resid_elev = node_elev - grid_elev_at_nodes
rmse_elev = np.sqrt(np.nanmean(resid_elev ** 2))
print(f"Elevation RMSE: {rmse_elev:.2f} m")

valid_temp = ~np.isnan(node_temp)
resid_temp = node_temp[valid_temp] - grid_temp_at_nodes[valid_temp]
rmse_temp = np.sqrt(np.nanmean(resid_temp ** 2))
std_resid = np.nanstd(resid_temp)
outlier_mask = np.abs(resid_temp) > 2 * std_resid
print(f"Temperature RMSE: {rmse_temp:.2f} K")
print(f"Temperature outliers (>2 std): {outlier_mask.sum()}")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
sc0 = axes[0].scatter(lons, lats, c=resid_elev, cmap='RdBu_r', s=30, alpha=0.7)
axes[0].set_xlabel('Longitude'); axes[0].set_ylabel('Latitude')
axes[0].set_title('Elevation Residual (node - grid)')
fig.colorbar(sc0, ax=axes[0], label='m')

sc1 = axes[1].scatter(lons[valid_temp], lats[valid_temp], c=resid_temp,
                       cmap='RdBu_r', s=30, alpha=0.7)
axes[1].set_xlabel('Longitude'); axes[1].set_ylabel('Latitude')
axes[1].set_title('Temperature Residual (measured - grid)')
fig.colorbar(sc1, ax=axes[1], label='K')
plt.tight_layout()
plt.savefig('data/figures/residual_map.png', dpi=120)
plt.close()
print("Saved residual_map.png")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].hist(resid_elev, bins=40, edgecolor='black', alpha=0.7, color='steelblue')
axes[0].axvline(0, color='red', linestyle='--')
axes[0].set_xlabel('Elevation Residual (m)'); axes[0].set_ylabel('Count')
axes[0].set_title(f'Elevation Residual (RMSE={rmse_elev:.1f}m)'); axes[0].grid(True)

axes[1].hist(resid_temp, bins=40, edgecolor='black', alpha=0.7, color='coral')
axes[1].axvline(0, color='red', linestyle='--')
axes[1].set_xlabel('Temperature Residual (K)'); axes[1].set_ylabel('Count')
axes[1].set_title(f'Temperature Residual (RMSE={rmse_temp:.1f}K)'); axes[1].grid(True)
plt.tight_layout()
plt.savefig('data/figures/residual_histograms.png', dpi=120)
plt.close()
print("Saved residual_histograms.png")

# %% [markdown]
# ## Edge Analysis (Phase E)
# Edge weight is strongly correlated with distance (r=0.914). Terrain factor has
# high variance due to large elevation differences. ~40% of edges are flat.
# 125 bottleneck edges identified (>75th percentile weight).

# %%
# Edge analysis
dist = edges_df['distance_km'].values
weight = edges_df['weight'].values
elev_change = edges_df['elevation_change'].values
terrain = edges_df['terrain_factor'].values

print(f"Distance: min={dist.min():.1f}, max={dist.max():.1f}, mean={dist.mean():.1f} km")
print(f"Weight: min={weight.min():.1f}, max={weight.max():.1f}, mean={weight.mean():.1f}")
print(f"Uphill: {(elev_change > 0).sum()}, Downhill: {(elev_change < 0).sum()}, Flat: {(elev_change == 0).sum()}")

valid = ~(np.isnan(dist) | np.isnan(weight))
corr_dw = np.corrcoef(dist[valid], weight[valid])[0, 1]
print(f"Correlation (distance vs weight): {corr_dw:.3f}")

weight_q75 = np.percentile(weight, 75)
print(f"Bottleneck edges (>75th pct): {(weight > weight_q75).sum()}")

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes[0, 0].scatter(dist, weight, alpha=0.3, s=10, c='steelblue')
z = np.polyfit(dist[valid], weight[valid], 1)
axes[0, 0].plot(np.linspace(dist.min(), dist.max(), 100),
                np.poly1d(z)(np.linspace(dist.min(), dist.max(), 100)), 'r--', lw=2)
axes[0, 0].set_xlabel('Distance (km)'); axes[0, 0].set_ylabel('Weight')
axes[0, 0].set_title(f'Weight vs Distance (r={corr_dw:.3f})'); axes[0, 0].grid(True)

axes[0, 1].hist(elev_change, bins=50, edgecolor='black', alpha=0.7, color='olive')
axes[0, 1].axvline(0, color='red', linestyle='--', lw=2)
axes[0, 1].set_xlabel('Elevation Change (m)'); axes[0, 1].set_ylabel('Count')
axes[0, 1].set_title('Elevation Change Distribution'); axes[0, 1].grid(True)

axes[1, 0].hist(weight, bins=50, edgecolor='black', alpha=0.7, color='coral')
axes[1, 0].axvline(weight_q75, color='red', linestyle='--', lw=2)
axes[1, 0].set_xlabel('Weight'); axes[1, 0].set_ylabel('Count')
axes[1, 0].set_title('Weight Distribution'); axes[1, 0].grid(True)

axes[1, 1].scatter(terrain, weight, alpha=0.3, s=10, c='purple')
axes[1, 1].set_xlabel('Terrain Factor'); axes[1, 1].set_ylabel('Weight')
axes[1, 1].set_title('Weight vs Terrain Factor'); axes[1, 1].grid(True)

plt.tight_layout()
plt.savefig('data/figures/edge_analysis.png', dpi=120)
plt.close()
print("Saved edge_analysis.png")

# %% [markdown]
# ## Visualization (Phase F)
# Summary plots of node distributions, spatial layouts, and network graph.

# %%
# Network graph and summary visualizations
from_col = edges_df['id_edge_from'].values
to_col = edges_df['id_edge_to'].values

fig, ax = plt.subplots(figsize=(14, 9))
sc = ax.scatter(lons, lats, c=node_elev, cmap='terrain', s=50, alpha=0.8, zorder=3)
fig.colorbar(sc, ax=ax, label='Elevation (m)')

for i in range(len(edges_df)):
    src = from_col[i]
    dst = to_col[i]
    ax.arrow(lons[src], lats[src],
             lons[dst] - lons[src], lats[dst] - lats[src],
             head_width=1.5, head_length=1.0, fc='gray', ec='gray', alpha=0.3, zorder=1)

ax.set_xlabel('Longitude'); ax.set_ylabel('Latitude')
ax.set_title('Spatial Network (arrows = directed edges)'); ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('data/figures/network_graph.png', dpi=120)
plt.close()
print("Saved network_graph.png")

# Summary stats
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes[0, 0].hist(node_elev, bins=50, edgecolor='black', alpha=0.7, color='sienna')
axes[0, 0].set_xlabel('Elevation (m)'); axes[0, 0].set_ylabel('Count')
axes[0, 0].set_title('Node Elevation'); axes[0, 0].grid(True)

axes[0, 1].scatter(np.abs(lats), node_elev, alpha=0.5, s=20, c='steelblue')
axes[0, 1].set_xlabel('|Latitude|'); axes[0, 1].set_ylabel('Elevation (m)')
axes[0, 1].set_title('Elevation vs Latitude'); axes[0, 1].grid(True)

axes[0, 2].hist(dist, bins=50, edgecolor='black', alpha=0.7, color='olive')
axes[0, 2].set_xlabel('Distance (km)'); axes[0, 2].set_ylabel('Count')
axes[0, 2].set_title('Edge Distance'); axes[0, 2].grid(True)

region_counts = nodes_df['region'].value_counts()
axes[1, 0].bar(region_counts.index, region_counts.values, edgecolor='black', alpha=0.7, color='coral')
axes[1, 0].set_xlabel('Region'); axes[1, 0].set_ylabel('Count')
axes[1, 0].set_title('Nodes per Region'); axes[1, 0].tick_params(axis='x', rotation=45)
axes[1, 0].grid(True)

type_counts = nodes_df['node_type'].value_counts()
axes[1, 1].bar(type_counts.index, type_counts.values, edgecolor='black', alpha=0.7, color='purple')
axes[1, 1].set_xlabel('Node Type'); axes[1, 1].set_ylabel('Count')
axes[1, 1].set_title('Nodes per Type'); axes[1, 1].grid(True)

axes[1, 2].scatter(lons, lats, c=node_elev, cmap='terrain', s=30, alpha=0.7)
axes[1, 2].set_xlabel('Longitude'); axes[1, 2].set_ylabel('Latitude')
axes[1, 2].set_title('Node Spatial Distribution'); axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('data/figures/summary_stats.png', dpi=120)
plt.close()
print("Saved summary_stats.png")

# %%
# Final summary
print("\n=== EDA Complete ===")
print(f"Figures generated: {len(os.listdir('data/figures'))}")
print("All data in memory throughout — REPL state preserved across all phases.")
