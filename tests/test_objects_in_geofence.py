with open("tests/polygon_testing.json") as reader:
        poly = reader.read()

points1 = [(-46.6246, -23.5325), (2, 2), (3, 3), (4, 4)]
points2 = [(-46.6318, -23.5523), (2, 2), (3, 3), (4, 4)]

def test_if_within_poly():
    from utility.objects_in_geofence import check_if_within_geo

    assert check_if_within_geo(points1, poly) == None

    assert check_if_within_geo(points2, poly) == [{"latitude": -46.6318, "longitude": -23.5523}]
