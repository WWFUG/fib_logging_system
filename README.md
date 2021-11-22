# django-rest-tutorial

## How to run
- Install project dependencies
```bash
$ pip3 install -r requirements.txt
```
- Migrate database tables
```bash
$ cd REST/
$ python3 manage.py migrate
```
- Run the REST server
```bash
$ cd REST/
$ python3 manage.py runserver 127.0.0.1:8080
```
- Run the MQTT broker 
```bash
$  docker run -d -it -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
                       
```
- Run the gRPC Fibonacci server
```bash
$ cd gRPC/Fib
$ python3 fib_server.py 
```
- Run the gRPC Log server (Be sure to run the MQTT broker first)
```bash
$ cd gRPC/Log
$ python3 log_server.py 
```

- Note that if the build/ directory doesn't exist in any server directory (gRPC/Fib/, REST/ ...)
  run ```make``` before running the server


## Using `curl` to perform client request
- POST request
- e.g. if order = 4
```bash
$ curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8080/rest/fibonacci/ -d "{\"order\":\"4\"}"
```

- GET request
```
$ curl 127.0.0.1:8080/rest/logs
```

