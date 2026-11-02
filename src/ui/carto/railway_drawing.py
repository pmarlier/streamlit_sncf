import folium
import matplotlib


def draw_railway(railway_data_list: list, map_to_update: folium.Map) -> folium.Map:

    # color map to show how important the delay could be on the railway
    # (from green to black)
    NAMED_COLOR_MAP = ["green", "orange", "red", "black"]
    cmap = matplotlib.colors.ListedColormap(NAMED_COLOR_MAP)

    for railway_data in railway_data_list:
        # railway_id = railway_data[0]
        railway_coords_list = railway_data[1]
        departure = railway_data[2]
        arrival = railway_data[3]
        mean_delay_on_arrival = railway_data[4]

        for railway_coords in railway_coords_list:
            if len(railway_coords) > 0:
                # Ajouter la ligne de chemin de fer à la carte
                folium.PolyLine(
                    railway_coords,
                    color=matplotlib.colors.rgb2hex(cmap(mean_delay_on_arrival / 35)),
                    weight=4,
                    opacity=0.8,
                    tooltip=str(
                        f"{departure.capitalize()} - {arrival.capitalize()} : {mean_delay_on_arrival:.0f} min de retard moyen"
                    ),
                ).add_to(map_to_update)

    return map_to_update
