# ejemplo ilustrativo (ajusta nombres de columnas y timebase a tus datos)
import csv, json, datetime

epoch = "2025-10-15T00:00:00Z"   # pon aquí tu epoch real
czml = [{
  "id": "document",
  "version": "1.0"
}]

# fcd.csv: columns = veh_id,time,lon,lat,angle
vehicles = {}
with open("fcd.csv") as f:
    r = csv.DictReader(f)
    for row in r:
        vid = row["veh_id"]
        t = float(row["time"])   # segundos desde sim start o timestamp
        lon = float(row["lon"])
        lat = float(row["lat"])
        alt = 0
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
      "path": {"material": {"solidColor": {"color": {"rgba":[255,0,0,255]}}}, "width":2}
    }
    czml.append(ent)

with open("traffic.czml","w") as out:
    json.dump(czml, out, indent=2)
