import folium

from ui.carto import map_drawing


def test_create_map_defaults():
    map_drawing.init()
    m = map_drawing.create_map()
    assert isinstance(m, folium.Map)
    assert m.location == [46.5, 2.34]
    assert m.options["zoom"] == 6


def test_create_map_custom():
    map_drawing.init()
    m = map_drawing.create_map(latitude=48.8, longitude=2.3, zoom=12)
    assert isinstance(m, folium.Map)
    assert m.location == [48.8, 2.3]
    assert m.options["zoom"] == 12
