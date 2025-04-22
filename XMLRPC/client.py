#python3 InsultClient.py port_where_to_send option(0 -> Random Insult) (service or filter)
import sys
import random
import xmlrpc.client

insults = [
    "cavero",
    "asshole",
    "dumb",
    "motherfucker"
]

client = xmlrpc.client.ServerProxy(f'http://localhost:{sys.argv[1]}')
choice = None
if sys.argv[2] == "0":
    choice = random.choice(insults)
else:
    choice = sys.argv[2] 

if sys.argv[3] == "service":
    client.add_insult(choice)
elif sys.argv[3] == "filter":
    client.send_text(choice)