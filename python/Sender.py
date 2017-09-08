from twisted.web import server, resource, http


class RootResource(resource.Resource):
    def __init__(self):
        resource.Resource.__init__(self)
        self.putChild('coordinates', TestHandler())


class TestHandler(resource.Resource):
    isLeaf = True

    def __init__(self):
        resource.Resource.__init__(self)

    def render_GET(self, request):
        return self.render_POST(request)

    def render_POST(self, request):
        return "hello world!"


if __name__ == "__main__":
    import sys
    from twisted.internet import reactor

    reactor.listenTCP(9005, server.Site(RootResource()))
    reactor.run()
