from filter_redis import Filter
import multiprocessing
import pika
import time
import math

nodes = []
C = 768 # missatges per segon (aproximació dels tests d'estres)
T = 0.2 # segons que te de mitja tractar peticions (S'ha augmentat ja que hauria de ser 1/C però si no no escalaria)
anterior_lambda=0 # Porta el compte de missatges total
missatges_s=0

connexio = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
canal = connexio.channel()
canal.exchange_declare(exchange='filterExchange', exchange_type='fanout')

canal.queue_declare(queue='filterChannel')
canal.queue_bind(exchange='filterExchange', queue='filterChannel')

canal.queue_declare(queue='countFilter')
canal.queue_bind(exchange='filterExchange', queue='countFilter')

canal.queue_purge(queue='filterChannel')
canal.queue_purge(queue='countFilter')

def afegeix_node():
    print("Afegint node...")
    p = multiprocessing.Process(target=Filter)
    p.start()
    nodes.append(p)
    

def elimina_node():
    if nodes:
        print("Eliminant node...")
        p = nodes.pop()
        p.terminate()
        p.join()

def calcul_nodes():
    global T
    #if len(nodes) > 0: t_actual = T/len(nodes)
    #else: t_actual=T --> Hauria de recalcular-se la T però per simplificació i poder escalar més facilment els nodes no es fa
    return math.ceil(calcul_lambda()*T / C)

def calcul_lambda():
    global anterior_lambda, missatges_s
    estat_cua = canal.queue_declare(queue='countFilter', passive=True)
    lambd=estat_cua.method.message_count/5.0
    aux = anterior_lambda
    anterior_lambda= lambd
    missatges_s=max(lambd-aux,0)
    return missatges_s
    

def escalar():
    while True:
        try:
            N = calcul_nodes()
            print(f"[SCALER] N_necessaris:{N} N_actuals:{len(nodes)} lambda:{missatges_s}")
            diferencia = N - len(nodes) # Necessaris - actuals (comprovem si hem d'afegir o eliminar i quants)
            if diferencia > 0:
                for _ in range(diferencia):
                    afegeix_node()
                    
            elif diferencia < 0:
                diferencia = abs(diferencia)
                for _ in range(diferencia):
                    elimina_node()
            
            time.sleep(5)
        except KeyboardInterrupt:
            print("Finalitzant scaler")
            connexio.close()
            break
        
    

if __name__ == "__main__":
    try:
        escalar()
    except KeyboardInterrupt:
        print("Finalitzant scaler")
        connexio.close()