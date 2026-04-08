import ipyleaflet
from geopy.geocoders import Nominatim

DEFAULT_CENTER = (39.5, -98.35)
DEFAULT_ZOOM = 4
REQUEST_TIMEOUT = 15

_geolocator = Nominatim(user_agent="weather-explorer-notebook/1.0")


def get_tile_layer() -> ipyleaflet.TileLayer:
    """Return the notebook's chosen tile layer."""
    return ipyleaflet.basemap_to_tiles(ipyleaflet.basemaps.CartoDB.Positron)


def create_map() -> tuple[ipyleaflet.Map, ipyleaflet.Marker]:
    tile_layer = get_tile_layer()
    m = ipyleaflet.Map(center=DEFAULT_CENTER, zoom=DEFAULT_ZOOM, layers=[tile_layer])
    marker = ipyleaflet.Marker(
        location=DEFAULT_CENTER,
        draggable=False,
        title="Selected location",
    )
    return m, marker


def _format_coordinate(value: float, positive_label: str, negative_label: str) -> str:
    suffix = positive_label if value >= 0 else negative_label
    return f"{abs(value):.5f}°{suffix}"


def update_map_location(map_obj: ipyleaflet.Map, marker_obj: ipyleaflet.Marker, lat: float, lon: float) -> str:
    marker_obj.location = (lat, lon)
    map_obj.center = (lat, lon)
    map_obj.zoom = 10
    return (
        f"{_format_coordinate(lat, 'N', 'S')}, "
        f"{_format_coordinate(lon, 'E', 'W')}"
    )


def geocode_address(address: str) -> tuple[float, float]:
    location = _geolocator.geocode(address.strip(), timeout=REQUEST_TIMEOUT)
    if location is None:
        raise ValueError(f"Address not found: '{address}'")
    return location.latitude, location.longitude
