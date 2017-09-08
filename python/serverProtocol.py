from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver


class NavtelecomProtocol(LineReceiver):
    def connectionMade(self):
        print("Connection made")

    def connectionLost(self, reason):
        print("Connection lost")

    def dataReceived(self, line):
        return "data"


class ProtocolFactory(ServerFactory):

    protocol = NavtelecomProtocol

    def __init__(self):
        self.clientProtocols = []
