import json
import PortReader
# import PortReader

class Gateway:
    _instance = None

    def __init__(self):
        return

    def __del__(self):
        return

    @staticmethod
    def executeQuery(query,args):
        if (query == b'coordinates'):
            PortReader.readingCoordinates()
            return (json.dumps({'latitude':'ok','longitude':'coordinates information'})).encode()