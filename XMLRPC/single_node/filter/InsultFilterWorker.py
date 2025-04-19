# xmlrpc IMPORT
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import sys

insults = [
    "cavero",
    "asshole",
    "dumb",
    "motherfucker"
]

port = int(sys.argv[1])

s = xmlrpc.client.ServerProxy('http://localhost:8000')
s.add_worker(port)

class RequestHandler(SimpleXMLRPCRequestHandler): 
    rpc_paths = ('/RPC2')

with SimpleXMLRPCServer(('localhost',port),requestHandler=RequestHandler,allow_none=True) as server:
    server.register_introspection_functions()

    class InsultFilterWorker:
        phrases = []

        def get_insults(self):
            return self.phrases

        def work(self, phrase):
            for insult in insults:
                if insult in phrase:
                    self.phrases.append(phrase.replace(insult,"CENSORED"))

    server.register_instance(InsultFilterWorker()) 
    server.serve_forever()
