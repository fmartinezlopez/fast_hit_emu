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

rprint(fwtp_array)

stitcher = StitchManager()
tp_array = stitcher.run_stitching(fwtp_array, 3019)

rprint(tp_array)