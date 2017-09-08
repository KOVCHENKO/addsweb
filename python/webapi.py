from twisted.internet import reactor
from twisted.web import server, resource
from serverProtocol import ProtocolFactory
import webserver

print("Starting Web Server")
factory = ProtocolFactory()
site = server.Site(webserver.Simple(factory))
reactor.listenTCP(9005, site)
reactor.run()