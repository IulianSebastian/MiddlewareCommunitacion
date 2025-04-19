# XMLRPC IMPORT
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import signal
import sys

port = int(sys.argv[1])
service = xmlrpc.client.ServerProxy(f'http://localhost:{port}')

portObserver = int(sys.argv[2])

def deleteObs(signum,frame):
    print(service.deactivateBroadcast())
    print(service.deleteObserver(f'http://localhost:{portObserver}'))
    exit()

signal.signal(signal.SIGTERM, deleteObs)

class RequestHandler(SimpleXMLRPCRequestHandler): 
    rpc_paths = ('/RPC2')

with SimpleXMLRPCServer(('localhost',portObserver),requestHandler=RequestHandler,allow_none=True) as server:
    server.register_introspection_functions()

    def notify(insult):
        print(f"This is the insult == {insult}")

    server.register_function(notify)

    print(service.addObserver(f'http://localhost:{portObserver}'))
    print(service.activateBroadcast())
    server.serve_forever()
