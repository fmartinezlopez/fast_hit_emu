import numpy as np
import pandas as pd
from rich import print as rprint
from rich.progress import track

from tpgmanager import TPGManager
from stitchmanager import StitchManager

import matplotlib.pyplot as plt

n_frames = 10
noise_data = np.random.normal(loc=500, scale=250, size=(64*n_frames, 256))
adc_df = pd.DataFrame(noise_data).astype(int)
adc_df.index = [i*32 for i in range(64*n_frames)]
rprint(adc_df)

tpgm = TPGManager(500, "data/fir_coeffs.dat", 6, 1000)

fwtp_df, ped_df, pedval_df, fir_df = tpgm.run_capture(adc_df, pedchan=True)
rprint(ped_df)
rprint(fir_df)
rprint(fwtp_df)

stitcher = StitchManager()
tp_df = stitcher.run_stitching(fwtp_df)
rprint(tp_df)

plt.imshow(fir_df.T, aspect="auto", origin="lower", cmap="coolwarm", extent=[min(adc_df.index), max(adc_df.index), min(adc_df.columns), max(adc_df.columns)])
for i in range(n_frames):
    plt.axvline(i*32*64, linestyle="--", color="k", alpha=0.6)
plt.errorbar(fwtp_df["ts"]+fwtp_df["peak_time"]*32, fwtp_df["offline_ch"], xerr=[(fwtp_df["peak_time"]-fwtp_df["start_time"])*32, (fwtp_df["end_time"]-fwtp_df["peak_time"])*32], markerfacecolor="None", markeredgecolor="dodgerblue", marker="s", linestyle='', ecolor="dodgerblue", capsize=0.2, capthick=0.2)
plt.scatter(tp_df["peak_time"], tp_df["offline_ch"], facecolor="None", edgecolors="red", marker="o")
plt.savefig("test.png")