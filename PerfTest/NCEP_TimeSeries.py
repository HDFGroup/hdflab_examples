import sys
import random
import h5pyd
import numpy as np

# 
# Extracts a time series for the NCEP dataset
#

# choose random x,y coordinate for the time series
shape = (7850, 720, 1440)
x_index = random.randint(0, shape[2]-1)
y_index = random.randint(0, shape[1]-1)
end_index = shape[0]

if len(sys.argv) > 1:
    if sys.argv[1] in ("-h", "--help"):
        print("Usage python NCEP_TimeSeries.py  [end_index] [x_index] [y_index]")
        print("  end_index: [1,7850]")
        print("  x_index: [0, 1439]")
        print("  y_index: [0, 719]")
        sys.exit(1)
    end_index = int(sys.argv[1])
    if len(sys.argv) > 2:
        x_index = int(sys.argv[2])
    if len(sys.argv) > 3:
        y_index = int(sys.argv[3])

f = h5pyd.File("hdf5://shared/NASA/NCEP3/ncep3.he5", "r")
tair2m = f["/HDFEOS/GRIDS/NCEP/Data Fields/Tair_2m"]
fill_value = tair2m.attrs['_FillValue'][0]

print(f"Getting time series at point ({x_index}, {y_index}) for slices: 0-{end_index}")
tseries = tair2m[0:end_index, y_index, x_index]
non_fill = tseries[tseries != fill_value]
if len(non_fill) == 0:
    print("no non_fill values returned!")
    sys.exit(1)
print("done!")
tseries_mean = np.mean(non_fill)
tseries_min = np.min(non_fill)
tseries_max = np.max(non_fill)
print(f"Mean: {tseries_mean:.2f} Min: {tseries_min:.2f}  Max: {tseries_max:.2f}")
        



