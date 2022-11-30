import sys
import time
import h5pyd as h5py

if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
    usage = f"Usage: python {sys.argv[0]} --day n [--file filepath] "
    usage += "[--var Tair_2m|Psea_level|Qsat|SST] "
    print(usage)
    sys.exit(0)

day = None
var = "Tair_2m"
filepath = "/shared/NASA/NCEP3/ncep3.h5"
n = 1

while n < len(sys.argv):
    arg = sys.argv[n]
    val = sys.argv[n+1] if n+1 < len(sys.argv) else None
    if arg == "--day":
        day = int(val)
    elif arg == "--file":
        filepath = val
    elif arg == "--var":
        var = val
    else:
        sys.exit(f"Invalid argument: {arg}")
    n += 2

print(f"day: {day} file: {filepath} variable: {var}")

f = h5py.File(filepath)
grp = f["/HDFEOS/GRIDS/NCEP/Data Fields/"]
if var not in grp:
    sys.exit(f"invalid variable: {var}")
dset = grp[var]
print(dset)
fill_value = dset.attrs["_FillValue"][0]
print(f"fill_value: {fill_value}")
if day < 0 or day >= dset.shape[0]:
    sys.exit(f"day must be in range: [0, {dset.shape[0]}")
start_time = time.time()
arr = dset[day, :, :]
end_time = time.time()
print(f"data retrieved in {(end_time - start_time):.2f} s")
print(f"with_fill - min: {arr.min():5.2f} max: {arr.max():5.2f} mean: {arr.mean():5.2f}")
no_fill = arr[arr != fill_value]
print(f"no_fill - min: {no_fill.min():5.2f} max: {no_fill.max():5.2f} mean: {no_fill.mean():5.2f}")



