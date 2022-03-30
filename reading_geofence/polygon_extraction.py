from psycopg2 import Error, connect
from logs.logger import get_logger
import yaml

with open("./config/config.yaml") as reader:
    file = yaml.load(reader, Loader=yaml.FullLoader)["database"]

LOGGER = get_logger('Database Read Operation')


def get_polygon(source: str):
    '''This func takes the location of the image as input and then fetches the geofence coordinates of that location from postgres.'''

    LOGGER.debug("Source is {0}".format(source))
    
    try:
        connection = connect(user=file['user'],
                                      password=file['pwd'],
                                      host=file['host'],
                                      port=file['port'],
                                      database=file['db'])

        sql = """SELECT loc.id, loc.layer, ST_AsGeoJSON(loc.coordinate)
    FROM m_location_space AS loc INNER JOIN m_layer on loc.layer = m_layer.id
    WHERE m_layer.name = '{0}'""".format(source)

        cursor = connection.cursor()
        cursor.execute(sql)
        poly_data = cursor.fetchall()

        return poly_data[0][2]

    except (Exception, Error) as error:
        LOGGER.debug("Error while connecting to PostgreSQL - {0}".format(error))

    finally:
        if (cursor):
            cursor.close()
            connection.close()
