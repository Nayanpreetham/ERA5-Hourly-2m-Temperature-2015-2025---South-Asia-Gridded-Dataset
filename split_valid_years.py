import os
import glob
import xarray as xr

root = r'C:\Users\Nayan preetham\OneDrive\Documents\era5 Temperarture Dataset'
out_root = r'C:\Users\Nayan preetham\OneDrive\Documents\era5 Temperarture Dataset\split_chunks'

os.makedirs(out_root, exist_ok=True)

for nc_file in sorted(glob.glob(os.path.join(root, 'india_era5_*', '*.nc'))):
    year_dir = os.path.basename(os.path.dirname(nc_file))
    if year_dir == 'india_era5_2015':
        print(f'SKIP invalid file: {nc_file}')
        continue
    try:
        with xr.open_dataset(nc_file, engine='netcdf4', decode_times=False) as ds:
            total = ds.sizes['valid_time']
            num_chunks = 20
            chunk_size = total // num_chunks
            year_out = os.path.join(out_root, year_dir)
            os.makedirs(year_out, exist_ok=True)

            for i in range(num_chunks):
                start = i * chunk_size
                end = total if i == num_chunks - 1 else (i + 1) * chunk_size
                chunk = ds.isel({'valid_time': slice(start, end)})
                out_path = os.path.join(year_out, f'chunk_{i:02d}.nc')
                chunk.to_netcdf(out_path, engine='netcdf4')
                print(f'SAVED {out_path}')

            print(f'DONE {year_dir}')
    except Exception as e:
        print(f'FAILED {year_dir}: {type(e).__name__}: {e}')
