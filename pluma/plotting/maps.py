import matplotlib.pyplot as plt
import tilemapbase as tmb
import numpy as np


def showmap(NavData,
            figsize=(20, 20),
            with_scaling=0.6, to_aspect=(4/3), tiles=tmb.tiles.build_OSM(),
            cmap='jet', markersize=15, colorscale_override=None):

    if 'Data' not in NavData.columns:
        raise ValueError(
            'NavData input must have a "Data" Column.\
                See Stream.resample_temporospatial() for an example.')

    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(figsize)
    extent = tmb.Extent.from_lonlat(
        np.min(NavData['Longitude'].values),
        np.max(NavData['Longitude'].values),
        np.min(NavData['Latitude'].values),
        np.max(NavData['Latitude'].values))
    extent = extent.to_aspect(to_aspect).with_scaling(with_scaling)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_ylabel("Value")
    ax.set_xlabel("Time")
    plotter = tmb.Plotter(extent, tiles, width=600)
    plotter.plot(ax)

    path = [tmb.project(x, y)
            for x, y in
            zip(
                NavData['Longitude'].values,
                NavData['Latitude'].values)]
    x, y = zip(*path)

    if colorscale_override is None:
        colorscale_override = NavData['Data'].values
    ax.scatter(x, y,
               c=colorscale_override,
               s=markersize,
               cmap=cmap)
    return fig
