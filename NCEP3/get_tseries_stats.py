import sys
import time
import h5pyd as h5py

if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
    usage = f"Usage: python {sys.argv[0]} --lat n --lon m "
    usage += "[--day-start j] [--day-end k] [--file filepath] "
    usage += "[--var Tair_2m|Psea_level|Qsat|SST] "
    print(usage)
    sys.exit(0)

day_start = None
day_end = None
lat = None
lon = None
var = "Tair_2m"
filepath = "/shared/NASA/NCEP3/ncep3.h5"
n = 1

while n < len(sys.argv):
    arg = sys.argv[n]
    val = sys.argv[n+1] if n+1 < len(sys.argv) else None
    if arg == "--lat":
        lat = int(val)
    elif arg == "--lon":
        lon = int(val)
    elif arg == "--day-start":
        day_start = int(val)
    elif arg == "--day-end":
        day_end = int(val)
    elif arg == "--file":
        filepath = val
    elif arg == "--var":
        var = val
    else:
        sys.exit(f"Invalid argument: {arg}")
    n += 2

f = h5py.File(filepath)
grp = f["/HDFEOS/GRIDS/NCEP/Data Fields/"]
if var not in grp:
    sys.exit(f"invalid variable: {var}")
dset = grp[var]
print(dset)
print(dset.id.id)
print(dset.id.layout)
fill_value = dset.attrs["_FillValue"][0]
print(f"fill_value: {fill_value}")
if day_start is None:
    day_start = 0
elif day_start < 0 or day_start >= dset.shape[0]:
    sys.exit(f"start day must be in range: [0, {dset.shape[0] - 1}")
if day_end is None:
    day_end = dset.shape[0] - 1
elif day_end <= day_start or day_end >= dset.shape[0]:
    sys.exit(f"end day must be in range: [{day_start+1}, {dset.shape[0] - 1}]")
if lon is None:
    lon = 300
elif lon < 0 or lon >= dset.shape[1]:
    sys.exit(f"lon number must be in range [0, {dset.shape[1] - 1}]")
if lat is None:
    lat = 300
elif lat < 0 or lat >= dset.shape[2]:
    sys.exit(f"lat number must be in range [0, {dset.shape[2] - 1}]")

print(f"lat: {lat} lon: {lon} file: {filepath} variable: {var}[{day_start}:{day_end}]")

start_time = time.time()
arr = dset[day_start:day_end, lon, lat]
end_time = time.time()
print(f"data retrieved in {(end_time - start_time):.2f} s")
print(f"with_fill - min: {arr.min():5.2f} max: {arr.max():5.2f} mean: {arr.mean():5.2f}")
no_fill = arr[arr != fill_value]
if len(no_fill) == 0:
    print("no none fill value point returned")
else:
    print(f"no_fill - min: {no_fill.min():5.2f} max: {no_fill.max():5.2f} mean: {no_fill.mean():5.2f}")


