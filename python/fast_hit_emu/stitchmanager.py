import numpy as np
import pandas as pd
from rich import print as rprint
from rich.progress import track

import fast_hit_emu

class StitchManager:
    
    def __init__(self) -> None:
        pass
    
    def run_stitching_chanel(self, fwtp_array) -> np.array:
        stitch = fast_hit_emu.TPStitcher()
        tps = stitch.hit_stitcher(fwtp_array)
        return np.array(tps)
    
    def parse_channel(self, fwtp_df, offline_ch) -> np.array:
        return fwtp_df.loc[fwtp_df["offline_ch"] == offline_ch].to_numpy()
    
    def run_stitching(self, fwtp_df) -> pd.DataFrame:
        unique_chs = fwtp_df['offline_ch'].unique()
        tp_list = []
        for chan in unique_chs:
            fwtp_array = self.parse_channel(fwtp_df, chan)
            tp_list.extend(self.run_stitching_chanel(fwtp_array))
        tp_df = pd.DataFrame(tp_list, columns=["start_time", "peak_time", "time_over_threshold", "offline_ch", "sum_adc", "peak_adc"])
        return tp_df