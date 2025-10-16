import rasterio
from pyproj import Transformer

# cargar modelo SRTM (GeoTIFF)

def get_alt(lon, lat):
    x, y = transformer.transform(lon, lat)
    for val in dem.sample([(x, y)]):
        print(val)
        return float(val)
    
if __name__ == "__main__":
    print(f"Madrid: {get_alt(-1.647521, 42.813046)}")  # Ejemplo: Coordenadas de Madrid
# Ejemplo de uso
    # print(f"Londres: ".get_alt(-0.127758, 51.507351))  # Ejemplo: Coordenadas de Londres
   