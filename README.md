# ERA5 Hourly 2m Temperature (2015-2025) - South Asia Gridded Dataset

This repository stores the ERA5 hourly 2m temperature dataset for South Asia, split into 20 NetCDF chunks per year to make each file smaller and easier to upload to GitHub and Kaggle.

## Folder structure

- `split_chunks/india_era5_2016/chunk_00.nc` ... `chunk_19.nc`
- `split_chunks/india_era5_2017/chunk_00.nc` ... `chunk_19.nc`
- ...
- `split_chunks/india_era5_2025/chunk_00.nc` ... `chunk_19.nc`

The 2015 file was skipped because it was found to be invalid/corrupt and cannot be opened with the standard NetCDF reader.

## Why this is split

Each yearly dataset was divided into 20 time-based chunks along `valid_time` so that:

- file sizes are smaller,
- uploads are easier,
- chunks can be stored separately,
- and the original dataset can be reconstructed later.

## Re-merge the chunks into one dataset

Use the script `merge_chunks.py`.

Example:

```bash
python merge_chunks.py
```

This script will merge all `chunk_*.nc` files inside `split_chunks/<year>/` into a single NetCDF file in a `merged/` folder.

## Open and inspect a NetCDF file

```python
import xarray as xr

path = 'split_chunks/india_era5_2025/chunk_00.nc'
ds = xr.open_dataset(path, engine='netcdf4', decode_times=False)
print(ds)
print(ds.dims)
print(ds.data_vars)
```

## Recommended Python environment

Use a Python environment with:

```bash
pip install xarray netCDF4
```

For ERA5 NetCDF files, always open them with:

```python
xr.open_dataset(path, engine='netcdf4', decode_times=False)
```

## Merge example

```python
import xarray as xr

parts = [
    'split_chunks/india_era5_2025/chunk_00.nc',
    'split_chunks/india_era5_2025/chunk_01.nc',
    # ... all 20 files
]

datasets = [xr.open_dataset(p, engine='netcdf4', decode_times=False) for p in parts]
merged = xr.concat(datasets, dim='valid_time').sortby('valid_time')
merged.to_netcdf('merged/india_era5_2025_merged.nc', engine='netcdf4')
```

## Important note

The original full 2015 file is not included in this repository because it was invalid and failed to open as a NetCDF dataset. If needed, it should be re-downloaded or repaired separately.
