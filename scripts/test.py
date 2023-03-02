import numpy as np
import pandas as pd
from rich import print as rprint
from rich.progress import track

from tpgmanager import TPGManager

rprint("It worked!")

""" tpc_df = pd.read_hdf("test_interp_windows.hdf5", "window_0/adc").astype(int)
fwtp_df = pd.read_hdf("test_interp_windows.hdf5", "window_0/fwtp").astype(int)
rprint(tpc_df)
rprint(fwtp_df)

tpgm = TPGManager(500, "data/fir_coeffs.dat", 6, 250)
tp_df, ped_df, pedval_df, fir_df = tpgm.run_capture(tpc_df, pedchan=True)
rprint(ped_df)
rprint(fir_df)
rprint(tp_df)
tp_df.to_hdf("emu_tp_example.hdf5", key="emu_tps") """