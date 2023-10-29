import modules.data_table as dt
import modules.plotting as pt


def main():
    # Read in the data for plotting
    data_table = dt.read_exoplanet_eu(
        "data/exoplanet.eu_catalog.csv"
    )
    
    # Plot all designated relations
    pt.plot_wrap(data_table)

    # Wrap individual frames into gifs
    pt.create_looped_gif(
        "plots/radius_period_frames", "radius_period", frame_dur=2e2
    )
    pt.create_looped_gif(
        "plots/mass_radius_frames", "mass_radius", frame_dur=2e2
    )


if __name__ == "__main__":
    pt.rc_setup()
    main()
