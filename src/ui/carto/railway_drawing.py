from ui.carto import st_folium
import folium


def draw_railway(railway_data_list: list, map_to_update: folium.Map) -> folium.Map:
    
    for railway_data in railway_data_list:

        railway_id = railway_data[0]
        railway_coords_list = railway_data[1]
        departure = railway_data[2]
        arrival = railway_data[3]
        mean_delay_on_arrival = railway_data[4]

        for railway_coords in railway_coords_list:
            # Ajouter la ligne de chemin de fer à la carte
            folium.PolyLine(
                railway_coords,
                color='red',
                weight=4,
                opacity=0.8,
                tooltip=str(f"Retard Moyen sur la ligne : {mean_delay_on_arrival:.0f} min")
            ).add_to(map_to_update)

    return map_to_update
    
