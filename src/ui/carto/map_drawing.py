import logging.config

import branca.colormap as cm

from ui.carto import folium

logger: logging.Logger

# arbitrary extrema values for delay
MIN_DELAY_VALUE = 15
MAX_DELAY_VALUE = 50


def init() -> None:
    """Initialize logger"""
    global logger
    logging.config.fileConfig("config/logging.conf")
    logger = logging.getLogger(__name__)


def get_custom_colormap() -> cm.LinearColormap:
    """Return the color map used for delay rendering

    Returns:
        cm.LinearColormap: a LinearColormap object set with
        constant values set in map_drawing
    """
    colormap = cm.LinearColormap(
        ["green", "orange", "red"], vmin=MIN_DELAY_VALUE, vmax=MAX_DELAY_VALUE
    )
    colormap.caption = "Retard moyen à l'arrivée (en minutes)"
    return colormap


def create_map(
    latitude: float = 46.5, longitude: float = 2.34, zoom: int = 6
) -> folium.Map:
    """Instantiate a Folium map

    Args:
        latitude (float, optional):
            Latitude (North / South coordinates) of the center point of the map
            Written in float : ex. 46° 51' 24''N ~ 46.86
            Defaults to almost the latitude of the most beautiful city: 46.86.

        longitude (float, optional):
            Longitude (East / West coordinates) of the center point of the map
            Written in float : ex. 2° 21' 07''E ~ 2.34
            Defaults to almost the longitude of the most beautiful city : 2.34.

        zoom (int, optional):
            The zoom level of the map visualization.
            Defaults to the level adapted for France display : 6

    Returns:
        folium.Map: the instance reference of the created Folium map
    """
    colormap = get_custom_colormap()
    logger.debug("Color map created")
    # Add a white background and slight padding to the legend SVG
    legend_bg = """
    <style>
        svg#legend {
            position: fixed; 
            top: 20px; left: 20px; height: 50px; 
            border:2px solid grey; z-index:9999; font-size:14px;
            background-color:white; opacity: 0.55;
            transform: scale(0.9);
            transform-origin: top left;
        }
    </style>
    """
    # centered on Paris with a zoom level to see the whole country
    map = folium.Map(
        location=(latitude, longitude), zoom_start=zoom, zoom_control="bottomleft"
    )
    logger.debug(f"Map instanciated at point {(latitude, longitude)}, with zoom {zoom}")

    colormap.add_to(map)
    map.get_root().header.add_child(folium.Element(legend_bg))

    logger.debug("Map and color map linked")
    return map
