import numpy as np
from dataclasses import dataclass
from sklearn.linear_model import LinearRegression

from pluma.io.harp import to_harptime
from pluma.stream.harp import HarpStream
from pluma.stream.ubx import UbxStream, _UBX_MSGIDS


class SyncTimestamp:
    def __init__(self, ts_array, seconds_conversion=(lambda x: x)) -> None:
        self.raw_ts_array = ts_array
        self.ts_array = ts_array
        self.seconds_conversion_factor = seconds_conversion
        self.zero()
        self.to_seconds()
        self.max_pairs = len(ts_array) - 1

    def to_seconds(self):
        if self.seconds_conversion_factor is not None:
            self.ts_array = self.seconds_conversion_factor(self.ts_array)

    def zero(self, idx=0):
        self.ts_array = self.ts_array - self.ts_array[idx]

    def get_pair(self, pair_idx, order=1):
        if pair_idx > self.max_pairs + (order - 1):
            raise ValueError("Pair index is larger than the size of the array")
        else:
            return (
                self.ts_array[pair_idx],
                self.ts_array[pair_idx + order],
                self.ts_array[pair_idx + order] - self.ts_array[pair_idx],
            )

    def get_diff(self):
        return np.diff(self.ts_array)

    def compute_diff_matrix(self):
        d = np.expand_dims(self.ts_array, 1) - self.ts_array
        #  Consider using "return np.tril(d, k = 0)"
        return d.transpose()

    def find_closest_pair(
        self,
        pair_diff_seconds: float,
        dt_error: float = 0.001,
        method: str = "leq",
        return_first: bool = True,
        min_pair_index: int = 0,
    ):
        available_methods = ("leq", "eq")

        diff_mat = np.abs(self.compute_diff_matrix() - pair_diff_seconds)
        diff_mat = diff_mat[min_pair_index:, min_pair_index:]
        if dt_error is not None:
            if not np.any(diff_mat < dt_error):
                raise ValueError("All values above the minimum allowed dt_error.")

        if method == "leq":
            arg_min = np.argwhere(diff_mat < dt_error)
        elif method == "eq":
            arg_min = np.argwhere(diff_mat == np.min(diff_mat))
        else:
            raise ValueError(
                f"Method not known.\
                    Available methods are: {available_methods}"
            )

        if return_first:
            return arg_min[0] + min_pair_index
        else:
            return [x + min_pair_index for x in arg_min]

    def __repr__(self) -> str:
        return str(self.ts_array)

    def __str__(self) -> str:
        return str(self.ts_array)


@dataclass
class SyncLookup:
    ubx_ts: SyncTimestamp
    harp_ts: SyncTimestamp
    align_lookup: np.ndarray


def align_ubx_to_harp(
    ubx_SyncTimestamp: SyncTimestamp,
    harp_SyncTimestamp: SyncTimestamp,
    dt_error: float = 0.002,
    plot_diagnosis: bool = False,
):
    """Matches sync pulse indices from the ubx to the harp stream. First step to correct alignment drift.

    Args:
        ubx_SyncTimestamp (SyncTimestamp): SyncTimestamp object created from the timestamps of ubx alignment events
        harp_SyncTimestamp (SyncTimestamp): SyncTimestamp object created from the timestamps of Harp alignment events
        dt_error (float, optional): _description_. Defaults to 0.002.
        plot_diagnosis (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    """

    Args:
        dt_error (float, optional): Temporal error to flag automatic misdetections of alignment events (in seconds). Defaults to 0.002.
        plot_diagnosis (bool, optional): Defaults to False.

    Returns:
        np.array : A 2 column array that matches sync pulse indices from the ubx to the harp stream.
    """
    ubx_ts = ubx_SyncTimestamp
    harp_ts = harp_SyncTimestamp

    min_pair_index = 0
    pulses_lookup = np.empty((ubx_ts.max_pairs, 2), dtype=np.int16)
    for pair in np.arange(ubx_ts.max_pairs):
        dyad = harp_ts.find_closest_pair(
            ubx_ts.get_pair(pair)[-1], dt_error=dt_error, min_pair_index=min_pair_index
        )
        pulses_lookup[pair, :] = [pair, dyad[0]]
        min_pair_index = dyad[1]

    if plot_diagnosis is True:
        import pluma.sync.plotting as plotting

        plotting.plot_clockcalibration_diagnosis(ubx_ts=ubx_ts, harp_ts=harp_ts, pulses_lookup=pulses_lookup)

    return pulses_lookup


def get_clockcalibration_lookup(
    ubx_stream: UbxStream,
    harp_sync: HarpStream,
    dt_error: float = 0.002,
    plot_diagnosis: bool = False,
) -> SyncLookup:
    # Get the TIM_TM2 Message that timestamps the incoming TTL
    if not (ubx_stream.has_event(_UBX_MSGIDS.TIM_TM2)):
        raise KeyError(f"UbxStream does not contain {_UBX_MSGIDS.TIM_TM2.value} event. Try to load it?")

    tim_tm2 = ubx_stream.data.TIM_TM2.copy()  # TTL
    tim_tm2.insert(
        tim_tm2.shape[1],
        "RisingEdge",
        tim_tm2.apply(lambda x: x.loc["Message"].towMsR, axis=1),
        False,
    )
    risingEdgeEvents = tim_tm2["RisingEdge"].drop_duplicates(keep="first").values.astype(float)

    #  From Harp, get the second output channel
    harp_sync_out = harp_sync.copy()
    harp_sync_out = harp_sync_out[harp_sync_out["Value"].values & 3 > 0]

    ubx_ts = SyncTimestamp(risingEdgeEvents, seconds_conversion=lambda x: x * 1e-3)
    harp_ts = SyncTimestamp(
        harp_sync_out.index.values,
        seconds_conversion=lambda x: x / np.timedelta64(1, "s"),
    )

    align_lookup = align_ubx_to_harp(ubx_ts, harp_ts, dt_error=dt_error, plot_diagnosis=plot_diagnosis)
    return SyncLookup(ubx_ts, harp_ts, align_lookup)


def get_clockcalibration_model(sync_lookup: SyncLookup, r2_min_qc: float = 0.99) -> LinearRegression:
    ubx_ts = sync_lookup.ubx_ts
    harp_ts = sync_lookup.harp_ts
    align_lookup = sync_lookup.align_lookup

    harp_ts_seconds = to_harptime(harp_ts.raw_ts_array)
    x_gps_time = ubx_ts.raw_ts_array[align_lookup[:, 0]].reshape(-1, 1)
    y_harp_time = harp_ts_seconds[align_lookup[:, 1]]
    model = LinearRegression().fit(x_gps_time, y_harp_time)
    r2 = model.score(x_gps_time, y_harp_time)
    if r2 < r2_min_qc:
        raise AssertionError(f"The quality of the linear fit is lower than expected {r2}")
    else:
        return model
