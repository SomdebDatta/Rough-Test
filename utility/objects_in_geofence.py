from geojson import Feature, FeatureCollection, Point
from turfpy.measurement import points_within_polygon

from utility.converter import dict_from_list
from logs.logger import get_logger
import json

LOGGER = get_logger('Location Validator')


def check_if_within_geo(points, poly):

    '''This func takes the coordinates of the incidents and polygon coordinates of the corresponding geofence as ip and checks whether the points are inside the geofence.
    \nIt returns a list of the points only inside the polygon. 
    '''

    list_to_feature_pts = []

    for i in range (len(points)):
        list_to_feature_pts.append(Feature(geometry= Point(points[i])))

    input_point = FeatureCollection(list_to_feature_pts)
    print("--------------------------------------")
    print(json.loads(poly))
    LOGGER.debug("Point Collection - {0}".format(input_point))
    points_inside_dict = points_within_polygon(input_point, json.loads(poly))
    print(f'\n\n{points_inside_dict}\n\n')
    points_inside_list = [
        feature.get("geometry").get("coordinates") for feature in points_inside_dict.get("features")
    ]
    if points_inside_list:
        output = dict_from_list(points_inside_list)
        return output