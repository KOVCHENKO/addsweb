from __future__ import print_function
from twisted.internet import reactor, protocol

class EchoClient(protocol.Protocol):

   # Here is the message which should be sent
    def connectionMade(self):
        self.transport.write("Connection has been made")

    def dataReceived(self, data):
        print("Server said: ", data)
        self.transport.write(b'information is here')

def connectionLost(self, reason):
        print("Connection Lost")

class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed - goodbye!")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost - goodbye!")
        reactor.stop()

# connection to a server running on port 9000
if __name__ == '__main__':
    f = EchoFactory()
    reactor.connectTCP("localhost", 9005, f)
    reactor.run()