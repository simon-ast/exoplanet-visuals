import os
import matplotlib.pyplot as plt
import imageio
import pandas as pd


# GLOBAL
GIF_SAVE_DIR = "plots/animated"


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


def plot_wrap(exoplanet_data: pd.DataFrame):
    """DOC"""
    plot_data = exoplanet_data.copy(deep=True)
    plot_data = plot_data.loc[plot_data.radius > 1e-2]
    plot_data = plot_data.loc[plot_data.period < 1e6]

    # Frame out maximum plots bounds
    min_radius = plot_data.radius.min()
    max_radius = plot_data.radius.max()

    min_mass = plot_data.mass.min()
    max_mass = plot_data.mass.max()

    min_year = int(plot_data.discovered.min())

    max_year = min_year
    while max_year <= 2023:
        fig, ax = plt.subplots()
        ax.set(xlim=(min_mass * 0.9, max_mass * 1.1), xscale="log",
               ylim=(min_radius * 0.9, max_radius * 1.1), yscale="log",
               title=f"{max_year}")

        temp_data = plot_data.loc[
            plot_data.discovered <= max_year
        ]
        ax.scatter(temp_data.mass, temp_data.radius, alpha=0.3)
        ax.scatter(temp_data.mass_sini, temp_data.radius, alpha=0.3)

        plt.savefig(f"plots/radius_period_frames/{max_year}.png")
        plt.close()

        max_year += 1

