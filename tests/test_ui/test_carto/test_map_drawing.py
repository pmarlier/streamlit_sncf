from unittest.mock import MagicMock

import folium
import pytest

from ui.carto import map_drawing


def test_create_map_defaults():
    m = map_drawing.create_map()
    assert isinstance(m, folium.Map)
    assert m.location == [46.3, 2.34]
    assert m.options["zoom"] == 6


def test_create_map_custom():
    m = map_drawing.create_map(latitude=48.8, longitude=2.3, zoom=12)
    assert isinstance(m, folium.Map)
    assert m.location == [48.8, 2.3]
    assert m.options["zoom"] == 12
