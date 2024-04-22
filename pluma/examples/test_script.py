import matplotlib.pyplot as plt
import datetime
import tilemapbase as tmb
import numpy as np
import pandas as pd
from pluma.stream.georeference import Georeference
from pluma.stream.ubx import _UBX_MSGIDS
from pluma.schema import Dataset
from IPython.display import clear_output
from pluma.schema import outdoor

plt.style.use('ggplot')

## Figure export parameters
new_rc_params = {'text.usetex': False,
"svg.fonttype": 'none'
}
import matplotlib as mpl
mpl.rcParams.update(new_rc_params)

stream_root_folder = 'C:/Users/erski/Downloads/Lansing_NorthNatural_sub-OE036001_2023-09-07T161930Z/Lansing_NorthNatural_sub-OE036001_2023-09-07T161930Z/'
root = r"C:/Users/erski/Desktop"

dataset = Dataset(
    stream_root_folder,
    datasetlabel="Example",
    georeference= Georeference(),
    schema=outdoor.build_schema)
dataset.populate_streams(autoload=False)  # Add the "schema" that we want to load to our Dataset. If we want to load the whole dataset automatically, set autoload to True.

dataset.reload_streams(force_load=True)  # We will just load every single stream at the same time. This might take a while if loading from AWS
dataset.add_georeference_and_calibrate()
dataset.export_dataset(filename=f"{root}\dataset.pickle") # We can export the dataset as a .pickle file.