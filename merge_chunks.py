import glob
import os
from pathlib import Path

import xarray as xr


def merge_year_chunks(year_folder: str | os.PathLike, output_file: str | os.PathLike):
    """Merge all chunk_*.nc files in a year folder back into one dataset."""
    folder = Path(year_folder)
    chunk_files = sorted(folder.glob("chunk_*.nc"))
    if not chunk_files:
        raise FileNotFoundError(f"No chunk files found in: {folder}")

    datasets = []
    for chunk_path in chunk_files:
        ds = xr.open_dataset(chunk_path, engine="netcdf4", decode_times=False)
        datasets.append(ds)

    try:
        merged = xr.concat(datasets, dim="valid_time")
        if "valid_time" in merged.coords:
            merged = merged.sortby("valid_time")

        merged.to_netcdf(output_file, engine="netcdf4")
        print(f"Merged {len(chunk_files)} chunks into: {output_file}")
        return merged
    finally:
        for ds in datasets:
            ds.close()


def inspect_dataset(nc_path: str | os.PathLike):
    """Open a NetCDF and print the basic structure and metadata."""
    ds = xr.open_dataset(nc_path, engine="netcdf4", decode_times=False)
    try:
        print("\nFile:", nc_path)
        print("Dimensions:", dict(ds.dims))
        print("Coordinates:", list(ds.coords))
        print("Data variables:", list(ds.data_vars))
        for var in ds.data_vars:
            da = ds[var]
            print(var, da.dims, da.shape, da.dtype)
        return ds
    finally:
        ds.close()


if __name__ == "__main__":
    # Example 1: merge one year
    year_dir = r"split_chunks\india_era5_2025"
    merged_path = r"merged\india_era5_2025_merged.nc"
    os.makedirs(os.path.dirname(merged_path), exist_ok=True)
    merge_year_chunks(year_dir, merged_path)

    # Example 2: inspect the merged dataset
    inspect_dataset(merged_path)
