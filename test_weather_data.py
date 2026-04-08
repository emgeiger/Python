import pytest
import weather_data


class DummyLocation:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude


def test_tile_layer_uses_carto_provider() -> None:
    layer = weather_data.get_tile_layer()
    assert hasattr(layer, "url")
    assert "cartocdn.com" in layer.url.lower() or "carto" in layer.url.lower()


def test_geocode_address_returns_lat_lon(monkeypatch) -> None:
    monkeypatch.setattr(
        weather_data._geolocator,
        "geocode",
        lambda address, timeout=None: DummyLocation(39.7, -104.9),
    )
    lat, lon = weather_data.geocode_address("Denver, CO")
    assert lat == pytest.approx(39.7)
    assert lon == pytest.approx(-104.9)


def test_geocode_address_raises_when_address_not_found(monkeypatch) -> None:
    monkeypatch.setattr(
        weather_data._geolocator,
        "geocode",
        lambda address, timeout=None: None,
    )
    with pytest.raises(ValueError, match="Address not found"):
        weather_data.geocode_address("Unknown location")


def test_update_map_location_moves_map_and_marker() -> None:
    m, marker = weather_data.create_map()
    coord_label = weather_data.update_map_location(m, marker, 39.7, -104.9)
    assert tuple(m.center) == (39.7, -104.9)
    assert tuple(marker.location) == (39.7, -104.9)
    assert m.zoom == 10
    assert "39.70000°N" in coord_label
    assert "104.90000°W" in coord_label
