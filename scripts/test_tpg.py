import numpy as np
import pandas as pd
from rich import print as rprint
from rich.progress import track

from tpgmanager import TPGManager

noise_data = np.random.normal(loc=500, scale=100, size=(64*100, 256))
adc_df = pd.DataFrame(noise_data).astype(int)
rprint(adc_df)

tpgm = TPGManager(500, "data/fir_coeffs.dat", 6, 500)

tp_df, ped_df, pedval_df, fir_df = tpgm.run_capture(adc_df, pedchan=True)
rprint(ped_df)
rprint(fir_df)
rprint(tp_df)

import IPython
IPython.embed(colors="neutral")