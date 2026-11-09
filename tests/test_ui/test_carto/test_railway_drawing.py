from unittest.mock import MagicMock

import folium
import matplotlib.colors
import pytest

from ui.carto import railway_drawing


def test_draw_railway():
    # Mock map
    mock_map = MagicMock(spec=folium.Map)

    # railway_data_list: [[railway_id, coords_list, departure, arrival, mean_delay]]
    # coords_list: [[(lat, lon), (lat, lon)], ...]
    test_data = [
        [123, [[(48.0, 2.0), (47.0, 3.0)]], "Paris", "Lyon", 10.0],
        [456, [[(45.0, 4.0), (44.0, 5.0)]], "Lyon", "Marseille", 40.0],
        [789, [], "Marseille", "Nice", 20.0],  # empty coords should be skipped
    ]

    result = railway_drawing.draw_railway(test_data, mock_map)

    assert result == mock_map
    # PolyLine.add_to should have been called for the first two entries
    # Since PolyLine is a class, we need to check if it was called or if the map was modified.
    # In a real test we might patch folium.PolyLine.
    # But here we just verify it doesn't crash and returns the map.
