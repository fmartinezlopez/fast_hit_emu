import numpy as np
import pandas as pd
from rich import print as rprint
from rich.progress import track

import fast_hit_emu

class StitchManager:
    
    def __init__(self) -> None:
        pass
    
    def run_stitching(self, fwtp_array, offline_ch):
        stitch = fast_hit_emu.TPStitcher()
        tps = stitch.hit_stitcher(fwtp_array, offline_ch)
        return tps