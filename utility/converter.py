from logs.logger import get_logger
LOGGER = get_logger('Utility Converter')



def dict_from_list(lst):
    '''This func takes list as input and returns in the designated lat long dictionary format'''

    main = []
    LOGGER.debug("No list received")
    for i in lst: 
        dic = {"latitude": i[0], "longitude": i[1]}
        main.append(dic)
    return main

def output_format(structure, points):
    '''This function adds only the validated points in the expected json output format.'''

    structure["operational_data"]["locationData"] = points
    structure["isGeofence"] = True
    LOGGER.debug("Output structure generated - {0}".format(structure))
    return structure


def not_in_geofence(structure):
    '''Returns the expected output format if none of the points are inside the geofence.'''

    structure["operational_data"]["locationData"] = {}
    structure["isGeofence"] = False
    LOGGER.debug("Output structure generated - {0}".format(structure))
    return structure

def points_from_jsonip(lst:list):
    '''This function fetches the the 4 points from the given input json string and returns it as a list.'''

    points = [(item["latitude"], item["longitude"]) for item in lst]
    LOGGER.debug("Lat Long points successfully fetched from input json string.")
    return points