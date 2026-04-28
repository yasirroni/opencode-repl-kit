# Python Bridge — Using Python from MATLAB for Data Loading

## Why Use Python Bridge

MATLAB's native NetCDF support requires additional toolboxes. The Python bridge uses the project's existing Python environment (with xarray, pyarrow) to load data, then passes it to MATLAB workspace.

## NetCDF Loading

```matlab
% Add Python path
py.sys.path.insert(0, 'python');
py.os.chdir(pwd);

% Read NetCDF via xarray
ds = py.xarray.open_dataset('data/grid_data.nc');
ds.load();

% Extract variables as MATLAB arrays
temperature = double(ds{"temperature"}.values);
pressure = double(ds{"pressure"}.values);
humidity = double(ds{"humidity"}.values);
elevation = double(ds{"elevation"}.values);
lat = double(ds{"lat"}.values);
lon = double(ds{"lon"}.values);
alt = double(ds{"alt"}.values);

% Close after reading
ds.close();
```

## Arrow Loading

```matlab
% Load Arrow file via pyarrow
nodes_table = py.arrow.feather.read_table('data/nodes.arrow');

% Convert to MATLAB table (helper function needed)
% Or use JSON interchange:
% Python: nodes_df.to_json('data/nodes.json')
% MATLAB: nodes_data = jsondecode(fileread('data/nodes.json'));
```

## MAT File Interchange

Generate `.mat` files from Python, load directly in MATLAB:

```python
# In Python (generate_mat.py)
import scipy.io
scipy.io.savemat('data/grid.mat', {
    'temperature': grid_data,
    'pressure': pressure_data,
})
```

```matlab
% In MATLAB
load('data/grid.mat')
```

## Dimension Order Warning

NetCDF data loaded via Python may be in different order than MATLAB expects. Always verify:

```matlab
disp(['Grid dimensions: ', mat2str(size(temperature))]);
```

MATLAB stores arrays in column-major order. Python (numpy) uses row-major. After conversion, verify the dimensions match your expectations.
