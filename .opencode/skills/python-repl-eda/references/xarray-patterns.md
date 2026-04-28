# xarray Patterns — Detailed Reference

## Lazy Loading

```python
import xarray as xr

# Open is lazy — no data loaded yet
ds = xr.open_dataset('data/grid_data.nc')

# Inspect without loading
print(ds.dims)      # {'lat': 50, 'lon': 50, 'alt': 10}
print(ds.data_vars) # list of variables

# Load all data into memory
ds.load()

# Or load specific variables
ds['temperature'].load()
```

## Slicing and Selection

```python
# By coordinate value
ds.sel(lat=0, lon=0)
ds.sel(alt=0)        # surface

# By index
ds.isel(lat=0, lon=0)
ds.isel(lat=range(5), lon=range(5))

# Select altitude — use float() for exact match
ds.sel(alt=float(0))
```

## Statistics with NaN

```python
# xarray by default skips NaN
ds.temperature.mean()           # NaN-aware by default
ds.temperature.mean(dim=['lat', 'lon'])

# For numpy arrays
np.nanmean(arr)
np.nanstd(arr)
np.isnan(arr).sum()
```

## Describe Gotcha

```python
# WRONG — xarray Dataset has NO .describe()
ds.describe()  # AttributeError

# CORRECT — convert to DataFrame first
ds.to_dataframe().describe()
```

## Zonal Mean

```python
# Mean across longitude
temp_zonal = ds.temperature.mean(dim='lon')

# Then mean across altitude
zonal_mean = temp_zonal.mean(dim='alt')
```
