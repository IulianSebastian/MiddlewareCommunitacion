import xmlrpc.client
import time
import sys

listWorkers = sys.argv[1:-1]
for i in range(int(sys.argv[-1])):
    aux = listWorkers.pop(0)
    listWorkers.append(aux)

for i in range(4):
    worker = listWorkers.pop(0)
    s = xmlrpc.client.ServerProxy(f'http://localhost:{worker}')
    s.send_text("what happens motherfucker")
    listWorkers.append(worker)
    # time.sleep(2)

for i in range(4):
    worker = listWorkers.pop(0)
    s = xmlrpc.client.ServerProxy(f'http://localhost:{worker}')
    print(s.get_insults("what happens motherfucker"))
