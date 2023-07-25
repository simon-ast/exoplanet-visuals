import os
import typing as tp
import imageio
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


# GLOBAL
GIF_SAVE_DIR = "plots/animated"
FRAME_SAVE_TOP = "plots"


def plot_wrap(exoplanet_data: pd.DataFrame) -> None:
    """Total wrapper for individual frames"""
    # Set minimum and maximum year value from data frame
    min_year = int(exoplanet_data.discovered.min())
    max_year = int(exoplanet_data.discovered.max())

    # Iterate over each year
    curr_year = min_year
    while curr_year <= max_year:
        plot_mass_radius(exoplanet_data, curr_year)
        plot_radius_period(exoplanet_data, curr_year)

        # Increment current year
        curr_year += 1

    plot_current_relations(exoplanet_data)

    return None


def plot_current_relations(exoplanet_data: pd.DataFrame) -> None:
    """Multiplot of exoplanet data"""
    # Local parameters
    save_dir = f"{FRAME_SAVE_TOP}"
    mass_min, mass_max = data_range(exoplanet_data.mass)
    rad_min, rad_max = data_range(exoplanet_data.radius)
    per_min, per_max = data_range(exoplanet_data.period)

    # Instantiate figure
    fig, (ax_mr, ax_rp) = plt.subplots(ncols=2, figsize=(12, 6))
    ax_mr.set(
        xlim=(mass_min * 0.9, mass_max * 1.1), xscale="log",
        xlabel="Planetary mass [M$_\\mathrm{J}$]",
        ylim=(rad_min * 0.9, rad_max * 1.1), yscale="log",
        ylabel="Planetary radius [R$_\\mathrm{J}$]"
    )
    ax_rp.set(
        ylim=(rad_min * 0.9, rad_max * 1.1), xscale="log",
        ylabel="Planetary radius [R$_\\mathrm{J}$]",
        xlim=(per_min * 0.9, per_max * 1.1), yscale="log",
        xlabel="Orbital period [d]"
    )

    # Plot parameters
    ax_mr.scatter(exoplanet_data.mass, exoplanet_data.radius, alpha=0.3)
    ax_rp.scatter(exoplanet_data.period, exoplanet_data.radius, alpha=0.3)
    plt.tight_layout()

    plt.savefig(f"{save_dir}/exoplanet_parameters.png")
    plt.close()
    return None


def plot_mass_radius(
        exoplanet_data: pd.DataFrame,
        current_year: int
) -> None:
    """
    Generate mass-radius plot for all exoplanets discovered until
    'current_year'
    """
    # Set-up recurring variables
    frame_save_dir = f"{FRAME_SAVE_TOP}/mass_radius_frames"
    mass_min, mass_max = data_range(exoplanet_data.mass)
    rad_min, rad_max = data_range(exoplanet_data.radius)

    # Instantiate plot
    fig, ax = plt.subplots()
    ax.set(
        xlim=(mass_min * 0.9, mass_max * 1.1), xscale="log",
        xlabel="Planetary mass [M$_\\mathrm{J}$]",
        ylim=(rad_min * 0.9, rad_max * 1.1), yscale="log",
        ylabel="Planetary radius [R$_\\mathrm{J}$]",
        title=f"{current_year}"
    )

    # Select sub-frame based on maximum year
    plot_data = exoplanet_data.copy(deep=True)
    temp_data = plot_data.loc[
        plot_data.discovered <= current_year
    ]

    # Plot Mass-Radius data with opacity
    ax.scatter(temp_data.mass, temp_data.radius, alpha=0.3)
    plt.tight_layout()

    # Save as individual frame
    frame_name = f"mr_{current_year}"
    plt.savefig(f"{frame_save_dir}/{frame_name}.png")
    plt.close()

    return None


def plot_radius_period(
        exoplanet_data: pd.DataFrame,
        current_year: int
) -> None:
    """
    Generate mass-radius plot for all exoplanets discovered until
    'current_year'
    """
    # Set-up recurring variables
    frame_save_dir = f"{FRAME_SAVE_TOP}/radius_period_frames"
    rad_min, rad_max = data_range(exoplanet_data.radius)
    per_min, per_max = data_range(exoplanet_data.period)

    # Instantiate plot
    fig, ax = plt.subplots()
    ax.set(
        ylim=(rad_min * 0.9, rad_max * 1.1), yscale="log",
        ylabel="Planetary radius [R$_\\mathrm{J}$]",
        xlim=(per_min * 0.9, per_max * 1.1), xscale="log",
        xlabel="Orbital period [d]",
        title=f"{current_year}"
    )

    # Select sub-frame based on maximum year
    plot_data = exoplanet_data.copy(deep=True)
    temp_data = plot_data.loc[
        plot_data.discovered <= current_year
    ]

    # Plot Mass-Radius data with opacity
    ax.scatter(temp_data.period, temp_data.radius, alpha=0.3)
    plt.tight_layout()

    # Save as individual frame
    frame_name = f"rp_{current_year}"
    plt.savefig(f"{frame_save_dir}/{frame_name}.png")
    plt.close()

    return None


def data_range(exoplanet_data_series: pd.Series) -> tp.Tuple:
    """Utility - Read min/max value for plot bounds"""
    # Read out minimum and maximum values for plot constraints
    data_min = exoplanet_data_series.min()
    data_max = exoplanet_data_series.max()

    return data_min, data_max


def rc_setup():
    """Utility - Generalized plot attributes"""
    mpl.rcParams["xtick.direction"] = "in"
    mpl.rcParams["xtick.labelsize"] = "large"
    mpl.rcParams["xtick.major.width"] = 1.5
    mpl.rcParams["xtick.minor.width"] = 1.5
    mpl.rcParams["xtick.minor.visible"] = "True"
    mpl.rcParams["xtick.top"] = "True"

    mpl.rcParams["ytick.direction"] = "in"
    mpl.rcParams["ytick.labelsize"] = "large"
    mpl.rcParams["ytick.major.width"] = 1.5
    mpl.rcParams["ytick.minor.width"] = 1.5
    mpl.rcParams["ytick.minor.visible"] = "True"
    mpl.rcParams["ytick.right"] = "True"

    mpl.rcParams["axes.grid"] = "False"
    mpl.rcParams["axes.linewidth"] = 1.5
    mpl.rcParams["axes.labelsize"] = "large"

    mpl.rcParams["legend.frameon"] = "False"


def create_looped_gif(folder_name: str,
                      gif_save_name: str,
                      frame_dur: float = 1e3) -> None:
    """Wrapper to create a looped gif of all images saved in a folder"""
    # Create a list of all images (read in by 'imageio') of all images
    image_list = []
    for image in sorted(os.listdir(folder_name)):
        image_list.append(
            imageio.imread(f"{folder_name}/{image}")
        )

    # Save as a gif (with optional arguments)
    full_save = f"{GIF_SAVE_DIR}/{gif_save_name}"
    imageio.mimsave(
        f"{full_save}.gif", image_list, duration=frame_dur, loop=0
    )

    return None
