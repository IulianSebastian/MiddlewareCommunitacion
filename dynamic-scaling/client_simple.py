import pika
import random
import time

INSULTS = ["CAVERO", "UCRANIANO", "MOLARENC", "REUSENC", "RUMANO"]

connexio = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
canal = connexio.channel()
canal.exchange_declare(exchange='insultExchange', exchange_type='fanout')

def enviar_missatges(velocitat_mps, duracio_s):
    missatges_total = velocitat_mps * duracio_s
    interval = 1.0 / velocitat_mps  # segons entre missatges
    print(f"Iniciant etapa: {velocitat_mps} missatges/segon durant {duracio_s} segons...")

    inici = time.time()
    next_time = inici
    enviats = 0

    while enviats < missatges_total:
        now = time.time()
        if now >= next_time:
            canal.basic_publish(exchange='insultExchange', routing_key='', body=random.choice(INSULTS))
            enviats += 1
            next_time += interval
        else:
            time.sleep(min(next_time - now, 0.001))  
            
    print(f"Etapa finalitzada: enviats {enviats} missatges")

if __name__ == "__main__":
    try:
        print("TESTS D'ESCALABILITAT")
        print("Enviant 1 missatge per segon")
        enviar_missatges(1, 10)
        print("Enviant 1000 missatges per segon")
        enviar_missatges(1000, 10)
        print("Enviant 2000 missatges per segon")
        enviar_missatges(2000, 10)
        print("Test completat!")

    except KeyboardInterrupt:
        print("Aturat per l'usuari.")
    finally:
        connexio.close()
