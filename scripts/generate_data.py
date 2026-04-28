#!/usr/bin/env python
"""
Generate spatial network test data for EDA showcase.

Creates three interlinked datasets:
  - data/grid_data.nc     : 3D atmospheric grid (50×50×10)
  - data/nodes.arrow      : ~200 network nodes
  - data/edges.arrow      : ~500 directed edges
"""

import numpy as np
import xarray as xr
import pyarrow as pa
import pyarrow as pa
import pyarrow.feather as feather
import scipy.spatial as spatial
import os

RNG = np.random.default_rng(42)

LAT_SIZE, LON_SIZE, ALT_SIZE = 50, 50, 10
N_NODES, N_EDGES = 200, 500
NAN_FRAC = 0.05

DATA_DIR = "data"


def make_grid():
    lat = np.linspace(-90, 90, LAT_SIZE, dtype=np.float32)
    lon = np.linspace(-180, 180, LON_SIZE, dtype=np.float32)
    alt = np.arange(ALT_SIZE, dtype=np.float32)

    lat_g, lon_g = np.meshgrid(lat, lon, indexing="ij")

    elev = (
        3000 * np.sin(lat_g / 30) * np.cos(lon_g / 40)
        + 1000 * np.sin(lat_g / 10 + lon_g / 15)
        + 500 * RNG.standard_normal((LAT_SIZE, LON_SIZE), dtype=np.float32)
    )
    elev = np.clip(elev, 0, 8000)

    lapse_rate = 6.5 / 1000
    T0, P0, H0 = 288.15, 1013.25, 8.4
    base_temp = T0 - lapse_rate * elev + 5 * RNG.standard_normal((LAT_SIZE, LON_SIZE), dtype=np.float32)
    temperature = np.zeros((ALT_SIZE, LAT_SIZE, LON_SIZE), dtype=np.float32)
    pressure = np.zeros((ALT_SIZE, LAT_SIZE, LON_SIZE), dtype=np.float32)
    humidity = np.zeros((ALT_SIZE, LAT_SIZE, LON_SIZE), dtype=np.float32)

    for k in range(ALT_SIZE):
        z = k
        temperature[k] = base_temp - lapse_rate * z * 1000 + 2 * RNG.standard_normal((LAT_SIZE, LON_SIZE), dtype=np.float32)
        pressure[k] = P0 * np.exp(-z * 1000 / H0) + 5 * RNG.standard_normal((LAT_SIZE, LON_SIZE), dtype=np.float32)
        humidity[k] = np.clip(
            50 + 20 * np.sin(lat_g / 45) - z * 2 + 10 * RNG.standard_normal((LAT_SIZE, LON_SIZE), dtype=np.float32),
            0, 100,
        )

    temperature = temperature.astype(np.float32)
    pressure = pressure.astype(np.float32)
    humidity = humidity.astype(np.float32)

    for arr in [temperature, pressure, humidity]:
        mask = RNG.random(arr.shape) < NAN_FRAC
        arr[mask] = np.nan

    temperature = np.flip(temperature, axis=0)
    pressure = np.flip(pressure, axis=0)
    humidity = np.flip(humidity, axis=0)

    return xr.Dataset(
        {
            "elevation": (["lat", "lon"], elev),
            "temperature": (["alt", "lat", "lon"], temperature),
            "pressure": (["alt", "lat", "lon"], pressure),
            "humidity": (["alt", "lat", "lon"], humidity),
        },
        coords={
            "lat": lat,
            "lon": lon,
            "alt": alt,
        },
    )


def make_nodes(ds):
    n = N_NODES
    lat_all = ds.lat.values
    lon_all = ds.lon.values

    lats = RNG.choice(lat_all, size=n, replace=True)
    lons = RNG.choice(lon_all, size=n, replace=True)

    lat_idx = np.searchsorted(lat_all, lats)
    lon_idx = np.searchsorted(lon_all, lons)
    lat_idx = np.clip(lat_idx, 0, LAT_SIZE - 1)
    lon_idx = np.clip(lon_idx, 0, LON_SIZE - 1)

    node_elev = ds.elevation.values[lat_idx, lon_idx]

    regions = ["north", "south", "east", "west", "tropical"]
    region_labels = RNG.choice(regions, size=n)
    types = ["sensor", "station", "relay"]
    type_labels = RNG.choice(types, size=n, p=[0.5, 0.3, 0.2])

    measured_temp = (
        ds.temperature.values[0, lat_idx, lon_idx]
        + 1.5 * RNG.standard_normal(n, dtype=np.float32)
    )
    measured_pressure = (
        ds.pressure.values[0, lat_idx, lon_idx]
        + 3 * RNG.standard_normal(n, dtype=np.float32)
    )
    measured_humidity = np.clip(
        ds.humidity.values[0, lat_idx, lon_idx]
        + 5 * RNG.standard_normal(n, dtype=np.float32),
        0, 100,
    )

    nan_mask_t = RNG.random(n) < 0.03
    nan_mask_p = RNG.random(n) < 0.03
    nan_mask_h = RNG.random(n) < 0.03
    measured_temp = np.where(nan_mask_t, np.nan, measured_temp)
    measured_pressure = np.where(nan_mask_p, np.nan, measured_pressure)
    measured_humidity = np.where(nan_mask_h, np.nan, measured_humidity)

    node_ids = np.arange(n, dtype=np.int32)

    table = pa.table({
        "id_node": node_ids,
        "latitude": lats.astype(np.float32),
        "longitude": lons.astype(np.float32),
        "elevation": node_elev.astype(np.float32),
        "node_type": type_labels,
        "region": region_labels,
        "measured_temp": measured_temp,
        "measured_pressure": measured_pressure,
        "measured_humidity": measured_humidity,
    })
    return table


def make_edges(nodes_table, ds):
    n = len(nodes_table)
    lat_all = ds.lat.values
    lon_all = ds.lon.values

    lats = nodes_table["latitude"].to_numpy()
    lons = nodes_table["longitude"].to_numpy()
    node_ids = nodes_table["id_node"].to_numpy()

    coords = np.stack([lats, lons], axis=1)
    tree = spatial.cKDTree(coords)

    candidate_edges = set()
    max_dist = 25.0

    for i in range(n):
        nearby = tree.query_ball_point(coords[i], r=max_dist)
        for j in nearby:
            if i != j:
                if RNG.random() < 0.6:
                    candidate_edges.add((i, j) if RNG.random() < 0.5 else (j, i))

    sampled = RNG.choice(list(candidate_edges), size=min(N_EDGES, len(candidate_edges)), replace=False)
    edges_from = node_ids[[e[0] for e in sampled]]
    edges_to = node_ids[[e[1] for e in sampled]]

    lat_from = lats[[e[0] for e in sampled]]
    lon_from = lons[[e[0] for e in sampled]]
    lat_to = lats[[e[1] for e in sampled]]
    lon_to = lons[[e[1] for e in sampled]]

    R = 6371.0
    dlat = np.radians(lat_to - lat_from)
    dlon = np.radians(lon_to - lon_from)
    a = np.sin(dlat / 2) ** 2 + np.cos(np.radians(lat_from)) * np.cos(np.radians(lat_to)) * np.sin(dlon / 2) ** 2
    distances = 2 * R * np.arcsin(np.sqrt(a))

    elev_from = nodes_table["elevation"].to_numpy()[[e[0] for e in sampled]]
    elev_to = nodes_table["elevation"].to_numpy()[[e[1] for e in sampled]]
    elev_diff = elev_to - elev_from
    alpha = 0.05
    terrain_factor = 1.0 + alpha * np.abs(elev_diff) / (distances + 1e-6)
    weight = distances * terrain_factor

    edge_types = RNG.choice(["direct", "indirect"], size=len(sampled), p=[0.85, 0.15])
    weight = np.where(edge_types == "indirect", weight * 1.5, weight)

    table = pa.table({
        "id_edge_from": edges_from,
        "id_edge_to": edges_to,
        "distance_km": distances.astype(np.float32),
        "weight": weight.astype(np.float32),
        "edge_type": edge_types,
        "terrain_factor": terrain_factor.astype(np.float32),
        "elevation_change": elev_diff.astype(np.float32),
    })
    return table


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    print("Generating grid data...")
    ds = make_grid()
    grid_path = os.path.join(DATA_DIR, "grid_data.nc")
    ds.to_netcdf(grid_path)
    print(f"  Wrote {grid_path}  ({os.path.getsize(grid_path) // 1024} KB)")

    print("Generating node data...")
    nodes_table = make_nodes(ds)
    nodes_path = os.path.join(DATA_DIR, "nodes.arrow")
    with open(nodes_path, "wb") as f:
        feather.write_feather(nodes_table, f)
    print(f"  Wrote {nodes_path}  ({os.path.getsize(nodes_path) // 1024} KB, {len(nodes_table)} rows)")

    print("Generating edge data...")
    edges_table = make_edges(nodes_table, ds)
    edges_path = os.path.join(DATA_DIR, "edges.arrow")
    with open(edges_path, "wb") as f:
        feather.write_feather(edges_table, f)
    print(f"  Wrote {edges_path}  ({os.path.getsize(edges_path) // 1024} KB, {len(edges_table)} rows)")

    print("Done.")


if __name__ == "__main__":
    main()
