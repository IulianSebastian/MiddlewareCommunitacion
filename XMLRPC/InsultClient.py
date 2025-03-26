import xmlrpc.client
import time

s = xmlrpc.client.ServerProxy('http://localhost:8000')
s.add_insult("Fuck you")
time.sleep(2)
print(s.get_insults()) 