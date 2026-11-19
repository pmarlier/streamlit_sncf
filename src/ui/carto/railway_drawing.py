import folium
import matplotlib

from ui.carto import map_drawing


def draw_railway(
    railway_data_list: list, map_to_update: folium.Map, delay_range: tuple | None
) -> folium.Map:
    """Draw polylines on the given folium map from the data returned by railway_network
    module. The polylines are drawn regarding their delay and the match with the
    slider timerange values from the streamlit app.

    Args:
        railway_data_list (list): custom list made from the railway_network module
            list[0] : railway_id : used only to check consistency
            list[1] : railway_point_to_draw : the geographical railway data points
            list[2] : departure : the departure city of the railway link (hover)
            list[3] : arrival_city : the arrival city of the railway link (hover)
            list[4] : mean_delay : match the colormap of national delay statistics

        map_to_update (folium.Map): the displayed Folium Map to update

        delay_range (tuple | None): the delay range set by the user in the streamlit app
        to filter railway regarding their mean delay.
        If set to None, no filter has been set, and all the datas are displayed
        (unfiltered)

    Returns:
        folium.Map: The updated folium map
    """
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

        # if the railway holds the delay filter condition
        if railway_to_plot:
            for railway_coords in railway_coords_list:
                if len(railway_coords) > 0:
                    # add the railway by hand
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
