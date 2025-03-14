# XMLRPC IMPORT
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client

class RequestHandler(SimpleXMLRPCRequestHandler): 
    rpc_paths = ('/RPC2')

with SimpleXMLRPCServer(('localhost',4848),requestHandler=RequestHandler,allow_none=True) as server:
    server.register_introspection_functions()

    def notify(insult):
        print(f"This is the insult == {insult}")

    server.register_function(notify)

    service = xmlrpc.client.ServerProxy('http://localhost:8000')
    service.addObserver('http://localhost:4848')
    service.activateBroadcast()
    server.serve_forever()