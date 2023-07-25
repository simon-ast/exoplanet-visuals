from __future__ import annotations
import astropy.constants as c
import matplotlib.pyplot as plt
import matplotlib.colors as mcl
import matplotlib.cm as cm
import matplotlib as mpl
import numpy as np
import pandas as pd
import pyvo

# GLOBALS
CIRCLE_OFFSET = 0.5
CENTER_SIZE = 5e4
SYSTEM_NAME = "TOI-178"


def main():
    # First, read from NASA EPA
    system_data = nasa_epa_query(SYSTEM_NAME)
    pars = SystemParameters(system_data)
    pars.calculate_plot_location()

    # Set the plot parameters
    fig, ax = set_figure(pars)
    draw_star(ax, pars)

    # Plot individual planets
    for idx in range(pars.names.shape[0]):
        draw_planet(
            axis=ax, radius_raw=pars.sizes[idx], x_location=pars.xlocs[idx],
            letter=pars.letter[idx], radius_indicator=pars.size_nan[idx],
            host_radius=pars.hostrad
        )

    # Finish plot
    plt.tight_layout()
    plt.savefig(
        f"plots/system_sizes/system_size_{SYSTEM_NAME.replace(' ','')}.svg")


def nasa_epa_query(system_name: str) -> pd.DataFrame:
    """Query the NASA EPA for a specific system"""
    # Catch the example-case here
    if system_name == "Sun":
        data_frame = pd.read_csv(
            "data/exovis_systemsize_solarsystem.dat",
            delim_whitespace=True, skiprows=1
        )
        data_frame.columns = ["pl_name", "pl_rade", "pl_orbsmax"]
        data_frame["pl_letter"] = data_frame["pl_name"]
        data_frame["hostname"] = "Sun"
        data_frame["st_teff"] = 5800.0
        data_frame["st_rad"] = 1.0
        data_frame["sy_pnum"] = 8

        return data_frame

    adql = f"SELECT pl_name, pl_orbsmax, pl_rade, pl_letter, " \
           f"hostname, st_teff, st_rad, sy_pnum " \
           f"FROM ps WHERE default_flag = 1" \
           f"AND hostname = '{system_name}'"

    # Set up NASA EPA query with pyVO
    tap_source = "https://exoplanetarchive.ipac.caltech.edu/TAP"
    service = pyvo.dal.TAPService(tap_source)

    # Use pyVO to query NASA EPA
    result_table = service.search(adql).to_table().to_pandas()

    # SANITY CHECK: Catch empty data frame
    if result_table.empty:
        print(f"\n\t SEARCHING NASA ADS FOR {system_name} UNSUCCESSFUL!\n")
        exit()

    return result_table


class SystemParameters:
    """Collect all system parameters from NASA EPA"""
    def __init__(self, data_frame_raw: pd.DataFrame):
        # First, sort by distance
        data_frame = data_frame_raw.sort_values(by="pl_orbsmax")

        # Record size NaNs, and fill with sizes of 5% stellar disk equivalent
        data_frame["size_nan"] = np.isnan(data_frame["pl_rade"])
        data_frame["pl_rade"].fillna(
            0.05 * data_frame["st_rad"] * c.R_sun / c.R_earth, inplace=True
        )

        # Stellar parameters
        self.hostname = data_frame["hostname"].to_numpy(dtype="str")[0]
        self.hostrad = data_frame["st_rad"].to_numpy(dtype=float)[0]
        self.hostteff = data_frame["st_teff"].to_numpy(dtype=float)[0]
        self.p_num = data_frame["sy_pnum"].to_numpy(dtype=int)[0]

        # Planet parameters
        self.names = data_frame["pl_name"].to_numpy(dtype="str")
        self.letter = data_frame["pl_letter"].to_numpy(dtype="str")
        self.dist = data_frame["pl_orbsmax"].to_numpy(dtype=float) \
                    * c.au / c.au

        # Handle size of planets, considering NaN-values (from before)
        self.sizes = data_frame["pl_rade"].to_numpy(dtype=float) \
                     * c.R_earth / c.R_sun
        self.size_nan = data_frame["size_nan"].to_numpy(dtype=str)

        # Instantiate plot x-location values
        self.xlocs = None

    def calculate_plot_location(self):
        """Scale point location in plot with other planets and point sizes"""
        temp_xlocs = [0]

        for idx in range(1, self.sizes.shape[0]):
            temp_x = temp_xlocs[idx - 1] \
                     + self.sizes[idx - 1] \
                     + self.sizes[idx] \
                     + CIRCLE_OFFSET

            temp_xlocs.append(temp_x)

        xlocs = np.array(temp_xlocs)
        self.xlocs = xlocs + 1.3 + self.sizes[0]


def set_figure(system_pars: SystemParameters):
    """
    Set up figure, most importantly the correct size to keep a nice
    aspect ratio, regardless of the number of planets
    """
    # Set correct figure frame size to keep all circles actually circular
    x_limit = system_pars.xlocs[-1] + system_pars.sizes[-1] + CIRCLE_OFFSET
    fig_height = 5
    fig_width = x_limit / 3 * fig_height

    # Draw figure
    figure, axis = plt.subplots(figsize=(fig_width, fig_height))
    axis.set(xlim=(0, x_limit), ylim=(-1.5, 1.5))

    return figure, axis


def draw_star(axis, sys_pars: SystemParameters) -> None:
    """Draw the star as a nominal scatter-plot point"""
    # Sort out colour for stellar disk plot
    norm = mcl.Normalize(vmin=0, vmax=10000)
    star_colour = cm.autumn(norm(sys_pars.hostteff))
    star_edge_colour = cm.afmhot(norm(sys_pars.hostteff * 0.8))
    star_text_colour = cm.afmhot(norm(sys_pars.hostteff * 0.6))

    axis.scatter(
        0, 0, s=CENTER_SIZE, lw=10,
        color=star_colour, ec=star_edge_colour
    )

    # Stellar and system label
    stellar_label = f"{sys_pars.hostname}\n\n{sys_pars.hostrad:.2f} R$_\\odot$"
    system_label = f"{sys_pars.p_num} Planets"
    axis.text(
        0.05, 0, s=f"{stellar_label}\n\n{system_label}",
        verticalalignment="center", fontweight="bold", color=star_text_colour
    )

    return None


def draw_planet(
        axis: plt.Axes, radius_raw: float, x_location: float, letter: str,
        radius_indicator: str, host_radius: float
) -> None:
    """
    Draw planets as scatter-plot points, where the point size is scaled
    to the size of the stellar disk. Keep in mind that scatter-plot
    points are scaled by the square of the size-parameter 's'!
    """
    # Some display parameters
    if radius_indicator == "False":
        radius_string = f"{float(radius_raw * c.R_sun / c.R_earth):.2f}"
    else:
        radius_string = "?"

    # Scale point size to stellar disk size
    radius = radius_raw / host_radius

    axis.scatter(x_location, 0, s=CENTER_SIZE * radius ** 2, c="black")

    # Name and radius indicator
    text_offset = radius + 0.2
    axis.text(
        x_location, text_offset, s=letter, horizontalalignment="center",
        fontweight="bold", color="dimgrey"
    )
    axis.text(
        x_location, text_offset * -1, s=f"{radius_string}",
        horizontalalignment="center", fontweight="bold", color="dimgrey"
    )

    return None


def set_plot_parameters():
    """Utility - Generalized plot attributes"""
    mpl.rcParams["xtick.top"] = "False"
    mpl.rcParams["xtick.bottom"] = "False"
    mpl.rcParams["ytick.right"] = "False"
    mpl.rcParams["ytick.left"] = "False"

    mpl.rcParams["xtick.labeltop"] = "False"
    mpl.rcParams["xtick.labelbottom"] = "False"
    mpl.rcParams["ytick.labelleft"] = "False"
    mpl.rcParams["ytick.labelright"] = "False"

    mpl.rcParams["axes.grid"] = "False"
    mpl.rcParams["axes.linewidth"] = 1.5
    mpl.rcParams["axes.labelsize"] = "large"

    mpl.rcParams["legend.frameon"] = "False"


if __name__ == "__main__":
    set_plot_parameters()
    main()
