import time
import random
import sys
from concurrent.futures import ThreadPoolExecutor
import h5pyd as h5py

filename = "/nrel/nsrdb/conus/nsrdb_conus_2018.h5"
bucket = "nrel-pds-hsds"

def get_column(index):
    arr = dset[:, index]
    return arr 

if len(sys.argv) > 1:
    count = int(sys.argv[1])
else:
    count = 8

f = h5py.File(filename, bucket=bucket)

dset = f["wind_speed"]
indices = set()
while len(indices) < count:
    index = random.randint(0, dset.shape[1] - 1)
    indices.add(index)

indices = list(indices)
indices.sort()
print("indices:", indices)
start = time.time()

with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(get_column, indices))
    print(results)
elapsed = time.time() - start
   
for i in range(len(indices)):
    index = indices[i]
    arr = results[i]
    print(f"index: {index}: {arr.min()}, {arr.max()}, {arr.mean():6.2f}")
    last_start = time.time()

print(f"total time: {elapsed:5.3f}s")

