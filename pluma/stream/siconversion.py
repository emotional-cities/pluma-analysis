import pandas as pd


class SiUnitConversion:

    def __init__(self,
                 conversion_function: list = [],
                 units: list = [],
                 attempt_conversion=False
                 ) -> None:

        self.conversion_function = conversion_function
        self.units = units
        self.attempt_conversion = attempt_conversion
        self.is_si = False

    def validate_si_meta(self, data: pd.DataFrame) -> bool:
        n_handles = len(self.conversion_function)
        n_units = len(self.units)
        n_col = len(data.columns)

        if n_handles == 0:
            raise AssertionError("No conversion function handles are set.")
        if n_units == 0:
            raise AssertionError("No conversion units are set.")

        if not(n_handles == n_units == n_col):
            raise AssertionError(f"Number of SI conversion handles (={n_handles}),\
        units' labels (={n_units}),\
            and DataFrame columns (={n_col}) must be the same")

    def convert_to_si(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.is_si:
            raise AssertionError("Data is already in SI units.")
        else:
            self.validate_si_meta(df)
            return self._apply_si_conversion(df)

    def _apply_si_conversion(self, df):
        for col, fun in zip(df, self.conversion_function):
            df[col] = df[col].apply(fun)
        df.columns = [f"{col}_{unit}"
                      for col, unit
                      in zip(df.columns, self.units)]
        return df
