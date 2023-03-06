import click
import numpy as np
import pandas as pd
from rich import print as rprint
from rich.progress import track
from pathlib import Path

from matplotlib import pyplot as plt
import matplotlib.backends.backend_pdf

from tpgmanager import TPGManager

#!HARDCODED: Known noisy channels from CRP4 (as of its VDCB testing 08.02.23-17.02.23)
chan_mask = [2949, 3019, 1849, 2997, 2780]

#------------------------------------------------------------------------------
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--window_fraction',
              help="Fraction of slices to process", default=1., show_default=True)
@click.option('--align_tps', is_flag=True,
              help="Align emulated TPs to TPs in input file", default=False, show_default=True)
@click.option('-p', '--initial_pedestal',
              help="Select initial pedestal guess", default=500, show_default=True)
@click.option('--ped_chan', is_flag=True,
              help="Set initial pedestal to first ADC per channel", default=False, show_default=True)
@click.option('--ped_med', is_flag=True,
              help="Set initial pedestal to median ADC per channel", default=False, show_default=True)
@click.option('-f', '--filter_data_file',
              help="Select input filter coefficients", default="./data/fir_coeffs.dat", show_default=True)
@click.option('-s', '--filter_bit_shift',
              help="Select bit shift for filter normalization", default=6, show_default=True)
@click.option('-t', '--threshold',
              help="Select threshold for hit finder", default=500, show_default=True)
@click.option('-o', '--outfile',
              help="Name of output file")
@click.option('-i', '--interactive', is_flag=True,
              help="Open interactive terminal before finishing", default=False, show_default=True)
def cli(file_path: str, window_fraction: float, align_tps: bool, initial_pedestal: int, ped_chan: bool, ped_med: bool, filter_data_file: str, filter_bit_shift: int, threshold: int, outfile: str, interactive: bool) -> None:
    filter_path = Path(filter_data_file)
    tpgm = TPGManager(initial_pedestal, filter_data_file, filter_bit_shift, threshold)

    hdf5 = pd.HDFStore(file_path, mode="r")
    hdf5_out = pd.HDFStore(outfile, mode="w")
    n_windows = round(len(list(hdf5.walk())[0][1])*window_fraction)
    rprint(f'Slices to be processed: {n_windows}')
    for i in track(range(n_windows), description="Processing slices..."):
        tpc_df = hdf5.get(f'window_{i}/data/adc').astype(int)
        fwtp_df = hdf5.get(f'window_{i}/data/fwtp').astype(int)
        #rprint(fwtp_df)

        links = tpc_df.columns.get_level_values(0).unique()

        tp_list = []
        for link in links:
            #rprint(link)
            tpc_link_df = tpc_df[link]
            #rprint(tpc_link_df)
            link = eval(link)
            fwtp_link_df = fwtp_df.loc[(fwtp_df["crate_no"] == link[0])&(fwtp_df["slot_no"] == link[1])&(fwtp_df["fiber_no"] == link[2])]
            #rprint(fwtp_link_df)
            t0_tpc_link = tpc_link_df.index[0]
            t0_tp_link =  fwtp_link_df['ts'].min()
            tp_link_df, _, _, _ = tpgm.run_capture(tpc_link_df, chan_mask, ts_tpc_min=t0_tpc_link, ts_tp_min=t0_tp_link, pedchan=ped_chan, pedmed=ped_med, align=align_tps)
            tp_list.append(tp_link_df)
        tp_df = pd.concat(tp_list, ignore_index=True)
        #rprint(tp_df)

        hdf5_out.put(f'window_{i}/emu/{filter_path.stem}_t{threshold}', tp_df)  

    hdf5.close()
    hdf5_out.close()

    if interactive:
        import IPython
        IPython.embed(color="neutral")

if __name__ == "__main__":

    cli()