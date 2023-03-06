import click
import numpy as np
import pandas as pd
from rich import print as rprint
from rich.progress import track
from pathlib import Path

from matplotlib import pyplot as plt
import matplotlib.backends.backend_pdf

hit_labels = {'start_time':("start time", " [ticks]"), 'end_time':("end time", " [ticks]"), 'peak_time':("peak time", " [ticks]"), 'peak_adc':("peak adc", " [ADCs]"), 'sum_adc':("sum adc", " [adc]")}

#------------------------------------------------------------------------------
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--fw_file',
              help="File containing FWTPs")
@click.option('--emu_file',
              help="File containing emulated TPs")
@click.option('--emu_key',
              help="Key of emulated group to compare")
@click.option('-i', '--interactive', is_flag=True,
              help="Open interactive terminal before finishing", default=False, show_default=True)
def cli(fw_file: str, emu_file: str, emu_key: str, interactive: bool) -> None:

    hdf5_fw  = pd.HDFStore(fw_file, mode="r")
    hdf5_emu = pd.HDFStore(emu_file, mode="r")

    n_windows = len(list(hdf5_fw.walk())[0][1])
    print("a")

    comp_list = []
    rprint(f'Slices to be compared: {n_windows}')
    for i in track(range(n_windows), description="Reading slices..."):
        fwtp_df  = hdf5_fw.get(f'window_{i}/data/fwtp').astype(int)
        emutp_df = hdf5_emu.get(f'window_{i}/emu/{emu_key}').astype(int)
        comp_list.append(pd.merge(emutp_df, fwtp_df, on=["ts", "offline_ch"]))
    comp_df = pd.concat(comp_list, ignore_index=True)

    out_path = "./plots_2d.pdf"
    pdf = matplotlib.backends.backend_pdf.PdfPages(out_path)
    for var in hit_labels.keys():
        fig = plt.figure(figsize=(8,8))
        plt.style.use('ggplot')
        ax = fig.add_subplot(111)

        if((var == "peak_adc")or(var == "sum_adc")):
            out_min = min(np.min(comp_df[var+"_x"]), np.min(comp_df[var+"_y"]))
            out_max = max(np.max(comp_df[var+"_x"]), np.max(comp_df[var+"_y"]))
            plt.hist2d(comp_df[var+"_x"], comp_df[var+"_y"], bins=[np.linspace(out_min,out_max,100), np.linspace(out_min,out_max,100)], cmap="plasma", norm=matplotlib.colors.LogNorm())
        else:
            plt.hist2d(comp_df[var+"_x"], comp_df[var+"_y"], bins=[np.arange(0,64,1), np.arange(0,64,1)], cmap="plasma", norm=matplotlib.colors.LogNorm())

        plt.xlabel("Emulated "+hit_labels[var][0]+hit_labels[var][1], fontsize=14, labelpad=10, loc="right")
        plt.ylabel("Firmware "+hit_labels[var][0]+hit_labels[var][1], fontsize=14, labelpad=10, loc="top")
        plt.grid(True)

        pdf.savefig(bbox_inches='tight')
        plt.close()
    pdf.close()

    hdf5_fw.close()
    hdf5_emu.close()

if __name__ == "__main__":

    cli()