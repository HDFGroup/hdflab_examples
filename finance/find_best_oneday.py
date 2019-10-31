import h5pyd
import numpy as np
# Open a file containing stock quote data
f = h5pyd.File("hdf5://shared/sample/snp500.h5", 'r')
table = f["dset"]
# find the largest one day gain for any stock
max_gain = 0.0
symbol = None
date = None
cursor = table.create_cursor()
for row in cursor:
    if row["low"] <= 0.0:
        continue
    gain = (row["close"] - row["open"])/row["open"]
    gain *= 100.0  # make a percent
    if gain > max_gain:
        max_gain = gain
        date = row['date'].decode('utf-8')
        symbol = row['symbol'].decode('utf-8')
        print("updated target: {} {:4} {:7.2f}%".format(date, symbol, gain))

print("="*30)
print("best oneday: {} {:4} {:7.2f}%".format(date, symbol, max_gain))
