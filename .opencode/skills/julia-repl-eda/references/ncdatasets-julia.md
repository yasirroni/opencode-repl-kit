# NCDatasets.jl — Detailed Reference

## Dimension Order

**NCDatasets reads NetCDF in FILE dimension order**, NOT Python dimension order.

- File dimension order: `lon x lat x alt` = `(50, 50, 10)` in this dataset
- Python (numpy) convention: `alt x lat x lon`
- After numpy `flip` in `generate_data.py`: surface (physical alt 0) -> index 10 (1-based in Julia)
- So `temperature[:,:,10]` = surface slice

```julia
# WRONG (assumes Python dim order):
temp_grid_surf = temperature[1,:,:]

# CORRECT (NCDatasets uses file dimension order lon×lat×alt):
temp_grid_surf = temperature[:,:,10]
```

## Missing Values

```julia
# NCDatasets returns `missing` for fill values — convert to NaN:
temperature = coalesce.(ds["temperature"][:,:,:], Float32(NaN))

# Filter for valid (non-NaN) data — MUST filter BOTH arrays:
valid = .!(isnan.(node_temp)) .& isfinite.(grid_temp_at_nodes)
resid_temp = node_temp[valid] .- grid_temp_at_nodes[valid]
rmse_temp = sqrt(mean(resid_temp.^2))
```

## Reading Variables

```julia
using NCDatasets

ds = NCDataset("data/grid_data.nc")

# Read entire variable into memory
temperature = ds["temperature"][:,:,:]

# Read with slicing
temp_slice = ds["temperature"][:,:,1]

# Get variable attributes
ds["temperature"].attrib

# Close when done
close(ds)
```

## Statistics

```julia
using Statistics

# With NaN — use skipna
mean(skipna, arr)
std(skipna, arr)

# Count NaN
count(isnan, arr)

# Element-wise NaN check
isnan.(arr)
```
