# xmlrpc IMPORT
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer
import multiprocessing
import xmlrpc.client
import subprocess
import sys

# proc = [] 
workers = []

# Round Robin method to repart the work to the workers
def insult_server():
    class RequestHandler(SimpleXMLRPCRequestHandler): 
        rpc_paths = ('/RPC2')

    with SimpleXMLRPCServer(('localhost',8000),requestHandler=RequestHandler,allow_none=True) as server:
        server.register_introspection_functions()

        class InsultFilterServer:

            def get_insults(self):
                list = []
                for worker in workers:
                    list.append(xmlrpc.client.ServerProxy(f'http://localhost:{worker}').get_insults())
                return list
            
            def add_insult(self,phrase):
                work = workers.pop(0)
                xmlrpc.client.ServerProxy(f'http://localhost:{work}').work(phrase)
                workers.append(work)

        server.register_instance(InsultFilterServer()) 
        server.serve_forever()

# Execute a worker in the backgorund
def worker(port):
    subprocess.Popen(["python3", "InsultFilterWorker.py", str(port)])

# Start all the specified workers
def start_workers(num_workers):
    for i in range(num_workers):
        port = i+8080
        process = multiprocessing.Process(target=worker(port))
        process.start()
        # proc.append(process)
        workers.append(port)

if __name__ == "__main__":
    # num_workers = int(input("How many workers do you want to have ?"))
    num_workers = int(sys.argv[1])
    start_workers(num_workers)
    insult_server()