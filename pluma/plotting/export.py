import pandas as pd
import simplekml


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