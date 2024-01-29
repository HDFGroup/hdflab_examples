import time
import random
import sys
import h5pyd as h5py

filename = "/nrel/nsrdb/conus/nsrdb_conus_2018.h5"
bucket = "nrel-pds-hsds"

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
for i in range(len(indices)):
    index = indices[i]
    arr = dset[:, index]
    print(f"index: {index}: {arr.min()}, {arr.max()}, {arr.mean():6.2f}")
elapsed = time.time() - start
print(f"time: {elapsed:5.3f}s")


