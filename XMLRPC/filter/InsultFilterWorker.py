# python3 InsultFilterWorker PortServer PortWorker
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import sys

# insults = [
#     "cavero",
#     "asshole",
#     "dumb",
#     "motherfucker"
# ]

portServer = int(sys.argv[1])
portWorker = int(sys.argv[2])
portService = int(sys.argv[3])

s = xmlrpc.client.ServerProxy(f'http://localhost:{portServer}')
s.add_worker(portWorker)

class RequestHandler(SimpleXMLRPCRequestHandler): 
    rpc_paths = ('/RPC2')

with SimpleXMLRPCServer(('localhost',portWorker),requestHandler=RequestHandler,allow_none=True) as server:
    server.register_introspection_functions()

    class InsultFilterWorker:
        phrases = []

        def get_insults(self):
            return self.phrases

        def work(self, phrase):
            insults = xmlrpc.client.ServerProxy(f'http://localhost:{portService}').get_insults() 
            for insult in insults:
                if insult in phrase:
                    self.phrases.append(phrase.replace(insult,"CENSORED"))

    server.register_instance(InsultFilterWorker()) 
    server.serve_forever()
    
