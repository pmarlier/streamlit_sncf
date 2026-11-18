import folium
import matplotlib

from ui.carto import map_drawing


def draw_railway(
    railway_data_list: list, map_to_update: folium.Map, delay_range: tuple | None
) -> folium.Map:

    # color map to show how important the delay could be on the railway
    # (from green to black)
    cmap = map_drawing.get_custom_colormap()

    for railway_data in railway_data_list:
        # railway_id = railway_data[0]
        railway_coords_list = railway_data[1]
        departure = railway_data[2]
        arrival = railway_data[3]
        mean_delay_on_arrival = railway_data[4]

        # by default, plot the line
        railway_to_plot = True

        # if the slider is set, check if the mean delay of the line
        # is within the range
        if delay_range is not None:
            if not (
                mean_delay_on_arrival >= delay_range[0]
                and mean_delay_on_arrival <= delay_range[1]
            ):
                railway_to_plot = False

        if railway_to_plot:
            for railway_coords in railway_coords_list:
                if len(railway_coords) > 0:
                    # Ajouter la ligne de chemin de fer à la carte
                    folium.PolyLine(
                        railway_coords,
                        color=matplotlib.colors.rgb2hex(cmap(mean_delay_on_arrival)),
                        weight=4,
                        opacity=0.8,
                        tooltip=str(
                            f"{departure} - {arrival} : {mean_delay_on_arrival:.0f} min"
                        ),
                    ).add_to(map_to_update)

    return map_to_update
