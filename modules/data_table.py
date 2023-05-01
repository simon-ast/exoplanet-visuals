import pandas as pd

DATA_COLUMNS_EU = {
    "name": "# name",
    "discovered": "discovered",
    "mass": "mass",
    "mass_sini": "mass_sini",
    "radius": "radius",
    "period": "orbital_period",
    "det_type": "detection_type"
}


"""
'# name'
'planet_status'
'discovered'
'detection_type'
'mass'
'mass_error_min'
'mass_error_max'
'radius'
'radius_error_min'
'radius_error_max'
'orbital_period'
"""


def read_exoplanet_eu(filename: str) -> pd.DataFrame:
    """
    Read in the csv-file downloaded from exoplanet.eu, and generate
    standardised data frame based on mapping in DATA_COLUMNS_EU
    """
    # Instantiate final data frame and column name mapping
    exoplanet_data = pd.DataFrame(columns=list(DATA_COLUMNS_EU.keys()))

    # Read in raw csv-file from exoplanet.eu
    raw_data = pd.read_csv(filename)

    # Map values
    for key in DATA_COLUMNS_EU.keys():
        exoplanet_data[key] = raw_data[DATA_COLUMNS_EU[key]]

    # Todo: This is still very crude
    print("\n DROPPING ALL PLANETS WITH RADII < 1e-3"
          "\n DROPPING ALL PLANETS WITH PERIODS > 1e6\n\n")
    exoplanet_data = exoplanet_data[
        exoplanet_data.radius >= 1e-3
    ]
    exoplanet_data = exoplanet_data[
        exoplanet_data.period < 1e6
        ]

    return exoplanet_data
