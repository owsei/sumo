# ejemplo ilustrativo (ajusta nombres de columnas y timebase a tus datos)
import csv, json, datetime
import rasterio
from pyproj import Transformer

dem = rasterio.open("SRTM.tif")
transformer = Transformer.from_crs("EPSG:4326", dem.crs, always_xy=True)

def get_alt(lon, lat):
    x, y = transformer.transform(lon, lat)
    for val in dem.sample([(x, y)]):
        print(val)
        return float(val+50)

epoch = "2025-10-15T00:00:00Z"   # pon aquí tu epoch real
czml = [{
  "id": "document",
  "version": "1.0"
}]

# fcd.csv: columns = veh_id,time,lon,lat,angle
vehicles = {}
with open("fcd.csv") as f:
    r = csv.reader(f, delimiter=';', quotechar='|')
    for row in r:
        vid = row[2]
        t = float(row[0])   # segundos desde sim start o timestamp
        lon = float(row[8])
        lat = float(row[9])
        alt = get_alt(lon, lat) # altitud en metros (2m sobre el suelo)
        vehicles.setdefault(vid, []).append((t, lon, lat, alt))

for vid, samples in vehicles.items():
    # crear una entidad con epoch + muestras (segundos desde epoch)
    pos_array = []
    for s in samples:
        pos_array += [int(s[0]), s[1], s[2], s[3]]  # [sec, lon, lat, alt, ...]
    ent = {
      "id": f"veh_{vid}",
      "availability": f"{epoch}/{epoch}",  # opcional, puedes usar intervales reales
      "position": {
        "epoch": epoch,
        "cartographicDegrees": pos_array
      },
      "point": {"pixelSize": 6},
      "path": {
        "material": {
          "solidColor": {
              "color": {
                  "rgba":[255,0,0,255]
                  }
              }
          }, 
        "width":2}
    }
    czml.append(ent)

with open("traffic.czml","w") as out:
    json.dump(czml, out, indent=2)



# with open('fcd.csv', newline='') as csvfile:
#   spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
#   for row in spamreader:
#     print(row[0])