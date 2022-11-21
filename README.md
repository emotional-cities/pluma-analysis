# pluma-analysis

A low-level interface to data collected with the [pluma](https://github.com/emotional-cities/pluma) urban data acquisition system. Data used in the notebooks has been made publicly available in Amazon Simple Storage Service (S3) buckets.

More information about sample data sharing can be found in the [eMOTIONAL Cities data-share repository](https://github.com/emotional-cities/data-share).

## Compatible Environments

[Visual Studio Code](https://code.visualstudio.com/): All notebooks have been tested in Visual Studio Code on a Windows platform. Tests in other platforms and environments are forthcoming and will be added here.

## How to build

1. Open project folder in VS Code
2. Install [miniconda](https://docs.conda.io/en/latest/miniconda.html) (Python 3.9)
3. Install [Python Extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
4. Create environment from VS Code:
  - `Ctrl+Shift+P` > `Create Environment`
  - Select `.conda` environment
5. Make sure correct environment is selected in the notebook

The current notebook requires Python 3.9+ to run successfully. The file `environment.yml` contains the list of minimal package dependencies required.
