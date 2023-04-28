import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


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
               ylim=(min_radius * 0.9, max_radius * 1.1), yscale="log")

        temp_data = plot_data.loc[
            plot_data.discovered <= max_year
        ]
        ax.scatter(temp_data.mass, temp_data.radius, alpha=0.3)
        ax.scatter(temp_data.mass_sini, temp_data.radius, alpha=0.3)

        plt.savefig(f"plots/{max_year}.png")
        plt.close()

        max_year += 1

