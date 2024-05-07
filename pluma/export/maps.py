import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import tilemapbase as tmb
import numpy as np

import pandas as pd
import geopandas as gpd
import simplekml

from mpl_toolkits.axes_grid1 import make_axes_locatable


def showmap(path,
            color=None,
            fig=None,
            ax=None,
            figsize=(20, 20),
            with_scaling=0.6,
            to_aspect=None,
            tiles=tmb.tiles.build_OSM(),
            cmap='jet',
            markersize=15,
            **cbarkwargs):

    if fig is None:
        fig, ax = plt.subplots(1, 1)
        fig.set_size_inches(figsize)

    if isinstance(color, str):
        cmap = None

    if isinstance(path, gpd.GeoDataFrame):
        extent = tmb.extent_from_frame(path)
        coords = path.get_coordinates()
        path = coords.apply(lambda p: tmb.project(p.x, p.y), axis=1)
    else:
        extent = tmb.Extent.from_lonlat(
            np.min(path['Longitude'].values),
            np.max(path['Longitude'].values),
            np.min(path['Latitude'].values),
            np.max(path['Latitude'].values))
        path = [tmb.project(x, y)
                for x, y in
                zip(
                    path['Longitude'].values,
                    path['Latitude'].values)]
    x, y = zip(*path)

    if to_aspect is not None:
        extent = extent.to_aspect(to_aspect)
    if with_scaling is not None:
        extent = extent.with_scaling(with_scaling)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_ylabel("Value")
    ax.set_xlabel("Time")
    plotter = tmb.Plotter(extent, tiles, width=600)
    plotter.plot(ax)

    if color is None:
        color = mdates.date2num(path.index)
        if len(cbarkwargs) == 0:
            loc = mdates.AutoDateLocator()
            cbarkwargs['ticks'] = loc
            cbarkwargs['format'] = mdates.ConciseDateFormatter(loc)
            cbarkwargs['label'] = 'time'

    im = ax.scatter(
        x, y,
        c=color,
        s=markersize,
        cmap=cmap)
    if cmap is not None:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        fig.colorbar(im, cax=cax, **cbarkwargs)
    return fig


def exploremap(data: gpd.GeoDataFrame, **kwargs):
    index = data.index
    data = data.reset_index(drop=True)
    if not 'column' in kwargs:
        minutes = (index - index[0]).to_series(index=data.index).dt.total_seconds() / 60
        kwargs['column'] = minutes
        legend_kwds = kwargs.get('legend_kwds', {})
        if not 'caption' in legend_kwds:
            legend_kwds['caption'] = 'time (minutes)'
        kwargs['legend_kwds'] = legend_kwds
    if not 'cmap' in kwargs:
        kwargs['cmap'] = 'jet'
    return data.explore(**kwargs)


def export_kml_line(df: pd.DataFrame,
                    output_path: str = "walk.kml",
                    **kwargs):
    kml = simplekml.Kml()
    ls = kml.newlinestring(**kwargs)
    ls.coords = [(x, y) for x, y in zip(
        df.Longitude.values, df.Latitude.values)]
    ls.extrude = 1
    ls.altitudemode = simplekml.AltitudeMode.relativetoground
    kml.save(output_path)