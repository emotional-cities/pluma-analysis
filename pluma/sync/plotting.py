import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.ticker import MaxNLocator
from pluma.sync.ubx2harp import SyncTimestamp


def plot_clockcalibration_diagnosis(
    ubx_ts: SyncTimestamp,
    harp_ts: SyncTimestamp,
    pulses_lookup: np.ndarray,
    axes: tuple[Axes] = None,
):
    if axes is None:
        fig = plt.figure(figsize=(12, 8))
        idx_ax = fig.add_subplot(211)
        scatter_ax = fig.add_subplot(212)
    else:
        idx_ax = axes[0]
        scatter_ax = axes[1]

    idx_ax.plot(pulses_lookup[:, 0], pulses_lookup[:, 1], ".")
    idx_ax.set_xlabel("ubx_index")
    idx_ax.set_ylabel("Harp_index")
    idx_ax.set_title("Index correspondence between streams")

    scatter_ax.scatter(
        np.arange(len(ubx_ts.ts_array[pulses_lookup[:, 0]]) - 1),
        np.diff(ubx_ts.ts_array[pulses_lookup[:, 0]]),
        100,
        label="ubx",
    )
    scatter_ax.scatter(
        np.arange(len(harp_ts.ts_array[pulses_lookup[:, 1]]) - 1),
        np.diff(harp_ts.ts_array[pulses_lookup[:, 1]]),
        label="HARP",
    )

    scatter_ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    scatter_ax.set_ylabel("$\Delta t$ (s)")
    scatter_ax.set_xlabel("Trial number")
    scatter_ax.legend()
    if axes is None:
        plt.show()
