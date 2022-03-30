
def test_conversions():

    from utility.converter import output_format, not_in_geofence, points_from_jsonip

    structure = {
                    "operational_data": {
                        "locationData": [
                            {
                                "latitude": 35.002394,
                                "longitude": 28.110035
                            },
                            {
                                "latitude": 10,
                                "longitude": 10
                            },
                            {
                                "latitude": 35.01820428466797,
                                "longitude": 28.102587947028705
                            }
                        ]
                    },
                    "checkGeofence": True
                }

    points = [{"latitude": 15, "longitude": 15}]

    my_list = [[10, 10], [15, 15]]
    
    assert output_format(structure, points) == {
                                                    "operational_data": {
                                                        "locationData": [
                                                            {
                                                                "latitude": 15,
                                                                "longitude": 15
                                                            }
                                                        ]
                                                    },
                                                    "checkGeofence": True,
                                                    "isGeofence": True
                                                }
    
    assert not_in_geofence(structure) == {
                                                    "operational_data": {
                                                        "locationData": {}
                                                    },
                                                    "checkGeofence": True,
                                                    "isGeofence": False
                                                }

    assert points_from_jsonip(points) == [(15, 15)]