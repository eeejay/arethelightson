import cv, PIL.Image
from twisted.web import server, resource
from twisted.internet import reactor
import json
from twisted.web.error import NoResource

THRESHOLD = 0.2

class Root(resource.Resource):
    def getChild(self, name, request):
        if name:
            return NoResource()
        return RoomLight()

class RoomLight(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
        request.setHeader("content-type", "application/json")
        brightness = self.get_room_brightness()
        return json.dumps({'brightness' : brightness,
                           'lightson': brightness > THRESHOLD})

    def get_room_brightness(self):
        capture = cv.CreateCameraCapture(1)
        cv.QueryFrame(capture)
        cv.QueryFrame(capture)
        cv.QueryFrame(capture)
        cv.QueryFrame(capture)
        frame = cv.QueryFrame(capture)
        img = PIL.Image.fromstring('RGB', (frame.width, frame.height), frame.tostring()).convert('L')
        return img.getextrema()[1]/255.0

if __name__ == "__main__":
    site = server.Site(Root())
    reactor.listenTCP(8080, site)
    reactor.run()
