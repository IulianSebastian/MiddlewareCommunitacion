from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer
import multiprocessing
import xmlrpc.client
import subprocess
import sys
import time

sender = None

def insult_server():
    class RequestHandler(SimpleXMLRPCRequestHandler): 
        rpc_paths = ('/RPC2')

    with SimpleXMLRPCServer(('localhost',8000),requestHandler=RequestHandler,allow_none=True) as server:
        server.register_introspection_functions()

        manager = multiprocessing.Manager()
        workers = manager.list()
        work_to_do = manager.list()

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

            def done(self):
                if len(work_to_do) != 0:
                    return False
                return True

        def send_work(port,phrase):
            xmlrpc.client.ServerProxy(f'http://localhost:{port}').work(phrase)

        def sender_verify():
            worker_process = {}
            while True:
                if len(work_to_do) != 0:
                    phrase = work_to_do.pop(0)
                    worked = False
                    while (not worked):
                        for worker in workers:
                            process = worker_process.get(worker)
                            if (process is None) or (not process.is_alive()):
                                workers.remove(worker)
                                process = multiprocessing.Process(target=send_work,args=(worker,phrase))
                                process.start()
                                workers.append(worker)
                                worked = True
                                break

        sender = multiprocessing.Process(target=sender_verify)
        sender.start()

        server.register_instance(InsultFilterServer()) 
        server.serve_forever()

if __name__ == "__main__":
    insult_server()
