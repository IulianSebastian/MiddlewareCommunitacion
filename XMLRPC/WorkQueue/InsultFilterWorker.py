# xmlrpc IMPORT
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client

import signal 
import sys

sys.path.insert(0,'../../')

from insults import listInsults

port=int(input("In which port do you want to start the InsultFilterWorker ? "))

s = xmlrpc.client.ServerProxy('http://localhost:8000')
s.add_worker(port)

def signal_handler(sig,frame):
    print(f'Removing worker in port = {port}')
    s.remove_worker(port)
    sys.exit(0)

signal.signal(signal.SIGINT,signal_handler)

class RequestHandler(SimpleXMLRPCRequestHandler): 
    rpc_paths = ('/RPC2')

with SimpleXMLRPCServer(('localhost',port),requestHandler=RequestHandler,allow_none=True) as server:
    server.register_introspection_functions()

    class InsultFilterWorker:
        phrases = []

        def get_insults(self):
            return self.phrases

        def work(self, phrase):
            for insult in listInsults.insult:
                if insult in phrase:
                    self.phrases.append(phrase.replace(insult,"CENSORED"))
            print(phrase)

    server.register_instance(InsultFilterWorker()) 
    server.serve_forever()
    