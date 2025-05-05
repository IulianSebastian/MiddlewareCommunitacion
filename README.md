# Analysis of diferent MIDDLEWARE

> [!WARNING]
> We recommend using Linux as OS and not Windows 10/11 because Windows can give errors with the multiprocessing 
## Testing Requirements

> ⚠️ **Important:** The following libraries and services must be installed before running the project.

### Installation Commands

```bash
# Update package list
sudo apt update

# Install Redis and its Python client
sudo apt install redis-server -y
pip3 install redis

# Install RabbitMQ and its Python client
sudo apt install rabbitmq-server -y
pip3 install pika

# Enable and start RabbitMQ service
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server

# Install Pyro4 for remote object communication
pip3 install Pyro4
```


## Testing Xmlrpc
> [!CAUTION]
> Every command that is here as to be executed in his own terminal (shell) if it's not indicated otherwise
### For testing InsultService
```
python3 InsultService.py 8080
```
```
python3 InsultService.py 8081
```
```
python3 InsultService.py 8082
```
```
python3 single_multiple_service.py
```

### For testing InsultFilter
```
python3 InsultService.py 8080
```
```
python3 InsultFilterServer.py 8000
```
```
python3 InsultFilterWorker.py 8000 8001 8080
```
> [!NOTE]
> If you see a step that is to wait until something happens or if you need to interact with some bash will be about this one
> ```
> python3 single_multiple_filter.py
> ```

Wait here until the bash from the note says to start the second and then pres enter. If the message has been printed we do this steps (in new bash every steps):

```
python3 InsultService.py 8081
```
```
python3 InsultFilterWorker.py 8000 8002 8081
```

Once this steps that are up of this message are done we can pres enter on the bash from the note.

Wait here until the bash from the note says to start the second and then pres enter. If the message has been printed we do this steps (in new bash every steps):

```
python3 InsultService.py 8082
```
```
python3 InsultFilterWorker.py 8000 8003 8082
```
Once this steps that are up of this message are done we can pres enter on the bash from the note.

When the test finishes is going to open a graphic showing a comparation between one single node, two single node and three single node, if we close this window we will se in the terminal of the bash that we have executed the test, the values of each number of request for each number of nodes. ( Values of the graphic but in a table )


## Testing Pyro
> [!CAUTION]
> Every command that is here as to be executed in his own terminal (shell) if it's not indicated otherwise.
> For both tests, the Pyro name server must be running:
> ```bash
> python3 -m Pyro4.naming
> ```
### For testing InsultService
```
python3 service1.py
```
```
python3 service2.py
```
```
python3 service3.py
```
```
python3 test_service.py
```
### For testing InsulFilter
```
python3 service1.py
```
```
python3 service2.py
```
```
python3 service3.py
```
```
python3 filter1.py
```
```
python3 filter2.py
```
```
python3 filter3.py
```
```
python3 test_service.py
```
## Testing Redis
> [!CAUTION]
> Every command that is here as to be executed in his own terminal (shell) if it's not indicated otherwise
### For testing InsultService
```
python3 InsultService.py insultChannel ob1
```
```
python3 InsultService2.py insultChannel ob2
```
```
python3 InsultService3.py insultChannel ob3
```
```
python3 test_service.py
```
### For testing InsultFilter
> [!IMPORTANT]
> For executing this tests you have to execute the commands for the Redis InsultService but without the las command that is test_service.py of course each one of them in a different terminal
```
python3 InsultFilter.py work_queue insultChannel queue
```
> [!NOTE]
> If you see a step that is to wait until something happens or if you need to interact with some bash will be about this one
> ```
> python3 test_filter.py
> ```

Wait here until the bash from the note says to start the second and then pres enter. If the message has been printed we do this steps (in new bash every steps):
```
python3 InsultFilter.py work_queue insultChannel2 queue2
```
Once this steps that are up of this message are done we can pres enter on the bash from the note.

Wait here until the bash from the note says to start the second and then pres enter. If the message has been printed we do this steps (in new bash every steps):

```
python3 InsultFilter.py work_queue insultChannel3 queue3
```
Once this steps that are up of this message are done we can pres enter on the bash from the note.

When the test finishes is going to open a graphic showing a comparation between one single node, two single node and three single node, if we close this window we will se in the terminal of the bash that we have executed the test, the values of each number of request for each number of nodes. ( Values of the graphic but in a table )

## Testing RabbitMQ
> [!CAUTION]
> Every command that is here as to be executed in his own terminal (shell) if it's not indicated otherwise
### For testing InsultService
```
python3 service1.py
```
```
python3 service2.py
```
```
python3 service3.py
```
```
python3 test_service.py
```
### For testing InsulFilter
```
python3 service1.py
```
```
python3 service2.py
```
```
python3 service3.py
```
```
python3 filter1.py
```
```
python3 filter2.py
```
```
python3 filter3.py
```
```
python3 test_service.py
```
> [!NOTE]
> Changes that you can make simply : </br>
>   XML-RPC: You can change the port by modifying the number passed as an argument.</br>
>   Redis: Change the connection string passed as an argument.</br>
>   Pyro and RabbitMQ: You need to modify the specific lines of code of those variables.</br>
>   However, changing these configurations can disrupt the stress tests, likely because the tests are designed to work with specific settings.
