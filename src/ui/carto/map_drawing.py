from ui.carto import folium


def create_map(
    latitude: float = 46.3, longitude: float = 2.34, zoom: int = 6
) -> folium.Map:
    """Instantiate a Folium map

    Args:
        latitude (float, optional):
            Latitude (North / South coordinates) of the center point of the map as it will be displayed.
            Written in float : ex. 46° 51' 24''N ~ 46.86
            Defaults to almost the latitude of the most beautiful city of the world : 46.86.

        longitude (float, optional):
            Longitude (East / West coordinates) of the center point of the map as it will be displayed.
            Written in float : ex. 2° 21' 07''E ~ 2.34
            Defaults to almost the longitude of the most beautiful city of the world : 2.34.

        zoom (int, optional):
            The zoom level of the map visualization.
            Defaults to the level adapted for France display : 6

    Returns:
        folium.Map:
    """
    # centered on the most beautiful city in the world (Paris) with a zoom level to see the whole country
    map = folium.Map(location=(latitude, longitude), zoom_start=zoom)

    return map
