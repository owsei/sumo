import rasterio
from pyproj import Transformer

# cargar modelo SRTM (GeoTIFF)
dem = rasterio.open("SRTM.tif")
transformer = Transformer.from_crs("EPSG:4326", dem.crs, always_xy=True)

def get_alt(lon, lat):
    x, y = transformer.transform(lon, lat)
    for val in dem.sample([(x, y)]):
        return float(val)
