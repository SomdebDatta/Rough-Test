from geojson import loads

def read_geojson(filename: str):
    with open(filename) as reader:
        poly = loads(reader.read())
    return poly
