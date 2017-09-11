import json
import PortReader

class Gateway:
    _instance = None

    def __init__(self):
        return

    def __del__(self):
        return

    @staticmethod
    def executeQuery(query,args):
        if (query == b'coordinates'):
            result_coordinates = PortReader.readingCoordinates()
            print("in gateway: {0}".format(result_coordinates[0]))
            return (json.dumps({'latitude': result_coordinates[0],'longitude': result_coordinates[1], 'status': result_coordinates[2] })).encode()
