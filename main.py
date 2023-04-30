"""
PSEUDOCODE
Read in data file
    - Could be from exoplanet.eu or NASA ExoArch
Create a standardised data frame

"""
import modules.data_table as dt
import modules.plotting as pt


def main():
    data_table = dt.read_exoplanet_eu("data/exoplanet.eu_catalog.csv")
    pt.plot_wrap(data_table)
    pt.create_looped_gif("plots/radius_period_frames", "radius_period",
                         frame_dur=2e2)


if __name__ == "__main__":
    main()
