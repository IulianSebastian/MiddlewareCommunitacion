# xmlrpc IMPORT
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer
import sys

port = int(sys.argv[1])

class RequestHandler(SimpleXMLRPCRequestHandler): 
    rpc_paths = ('/RPC2')

with SimpleXMLRPCServer(('localhost',port),requestHandler=RequestHandler,allow_none=True) as server:

    insults = [
        "cavero",
        "asshole",
        "dumb",
        "motherfucker"
    ]

    server.register_introspection_functions()

    class InsultFilterWorker:
        phrases = []

        def get_insults(self):
            return self.phrases

        def send_text(self, phrase):
            print(f"Worker == {phrase}")
            for insult in insults:
                if insult in phrase:
                    self.phrases.append(phrase.replace(insult,"CENSORED"))
            print(phrase)

    server.register_instance(InsultFilterWorker()) 
    server.serve_forever()    