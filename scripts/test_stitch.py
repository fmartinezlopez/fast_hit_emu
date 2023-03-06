import numpy as np
import pandas as pd
from rich import print as rprint
from rich.progress import track

from stitchmanager import StitchManager

fwtp_array = np.array(([36448,          32,        55,         49,      2092,    32441,             0],
                       [38496,           4,        23,         13,      2950,    35391,             0],
                       [38496,          35,        63,         46,      1790,    39104,             1],
                       [40544,           0,        40,         10,      2489,    91846,             0],
                       [40544,          50,        63,         55,      4892,    14992,             1],
                       [46688,           0,        40,         10,      2489,    91846,             0]))

tp_array_manual = np.array(([37472, 38016, 736,  3019, 32441,  2092],
                            [38624, 38912, 608,  3019, 35391,  2950],
                            [39616, 40864, 2208, 3019, 130950, 2489],
                            [42144, 42304, 416,  3019, 14992,  4892],
                            [46688, 47008, 1280, 3019, 91846,  2489]))

rprint(fwtp_array)

stitcher = StitchManager()
tp_array = stitcher.run_stitching_channel(fwtp_array, 3019)

rprint(tp_array_manual)
rprint(tp_array)
rprint(tp_array_manual-tp_array)