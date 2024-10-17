from __future__ import annotations

import pandas as pd
from typing import Optional

from pluma.stream import Stream, StreamType
from pluma.io.eeg import load_eeg, synchronize_eeg_to_harp
from pluma.sync import ClockRefId
from pluma.stream.harp import HarpStream

from mne.io import Raw


class EegStream(Stream):
    """_summary_

    Args:
            Stream (_type_): _description_
    """

    def __init__(
        self,
        data: Optional[Raw] = None,
        server_lsl_marker: Optional[pd.DataFrame] = None,
        clockreferenceid: ClockRefId = ClockRefId.HARP,
        autoalign: bool = True,
        **kw,
    ):
        super(EegStream, self).__init__(data=data, **kw)
        self.streamtype = StreamType.EEG
        self.clockreference.referenceid = clockreferenceid
        self.autoalign = autoalign
        self.server_lsl_marker = server_lsl_marker
        if self.autoload:
            self.load()

    def load(self):
        self.data, _lsl_timestamp = load_eeg(filename=None, root=self.rootfolder)
        if self.server_lsl_marker is None:
            self.server_lsl_marker = _lsl_timestamp
        if (
            self.data is not None
            and self.autoalign
            and (self.clockreference.referenceid == ClockRefId.HARP)
        ):
            self.align_to_harp()

    def align_to_harp(self):
        print(
            "Attempting to automatically correct eeg timestamps to harp timestamps..."
        )
        eeg_to_harp_model = synchronize_eeg_to_harp(self.server_lsl_marker)
        self.data.np_time = HarpStream.from_seconds(
            eeg_to_harp_model.predict(self.data.np_time.reshape(-1, 1)).flatten()
        )
        print("Done.")

    def add_clock_offset(self, offset):
        if self.server_lsl_marker is not None:
            self.server_lsl_marker["Seconds"] += offset
        self.data.np_time += offset

    def __str__(self):
        return f"EEG stream from device {self.device}, stream {self.streamlabel}"
