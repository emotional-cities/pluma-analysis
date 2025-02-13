# pluma-analysis

![build](https://github.com/emotional-cities/pluma-analysis/actions/workflows/build.yml/badge.svg?branch=main)

A low-level interface to data collected with the [pluma](https://github.com/emotional-cities/pluma) urban data acquisition system. Data used in the notebooks has been made publicly available in Amazon Simple Storage Service (S3) buckets.

More information about sample data sharing can be found in the [eMOTIONAL Cities data-share repository](https://github.com/emotional-cities/data-share).

## Set-up Instructions

We recommend [uv](https://docs.astral.sh/uv/) for python version, environment, and package dependency management. However, any other tool compatible with the `pyproject.toml` standard should work.

### Install from PyPI

```
uv pip install pluma-analysis
```

### Install from source

```
git clone https://github.com/emotional-cities/pluma-analysis.git
cd pluma-analysis
uv sync --all-extras
```

This package was developed for the eMOTIONAL CITIES Project, which received funding from European Union’s Horizon 2020 research and innovation programme, under the grant agreement No 945307. The eMOTIONAL CITIES Project is a consortium of 12 partners co-coordinated by IGOT and FMUL, taking place between 2021 and 2025. More information at https://emotionalcities-h2020.eu/