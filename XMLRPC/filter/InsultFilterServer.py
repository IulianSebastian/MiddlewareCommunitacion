from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer
import multiprocessing
import xmlrpc.client
import subprocess
import sys
import time

portServer = int(sys.argv[1])
sender = None

def insult_server():
    class RequestHandler(SimpleXMLRPCRequestHandler): 
        rpc_paths = ('/RPC2')

    with SimpleXMLRPCServer(('localhost',portServer),requestHandler=RequestHandler,allow_none=True) as server:
        server.register_introspection_functions()

        manager = multiprocessing.Manager()
        workers = manager.list()
        work_to_do = manager.list()
        process_workers = []

        class InsultFilterServer:

            def get_insults(self):
                list = []
                for worker in workers:
                    list.append(xmlrpc.client.ServerProxy(f'http://localhost:{worker}').get_insults())
                return list
            
            def send_text(self,phrase):
                work_to_do.append(phrase)

            def add_worker(self,port):
                if port not in workers:
                    workers.append(port)
                    process = multiprocessing.Process(target=send_work,args=(port,))
                    process.start()
                    process_workers.append(process)

            def done(self):
                if len(work_to_do) != 0:
                    return False
                return True

        def send_work(port):
            worker = xmlrpc.client.ServerProxy(f'http://localhost:{port}')
            while True:
                if work_to_do:
                    work = work_to_do.pop(0)
                    if work:
                        worker.work(work)
                time.sleep(0.01)
        
        server.register_instance(InsultFilterServer()) 
        server.serve_forever()

if __name__ == "__main__":
    insult_server()
