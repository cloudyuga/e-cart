# "Frontend service" extracted as an individual service from monolith

Frontend service is extracted from the monolith.  It now runs as an individual service with MongoDB as its own database. 

With this step, we have broken down our complete monolith application into microservices that run independent of each other with the communication between them happening through API calls.

![](images/Frontend.jpeg?raw=true)

# Steps to run the application
Prerequiste: git, docker and docker-compose needs to be installed on the host machine

```sh
$ git clone https://github.com/cloudyuga/e-cart.git
$ cd e-cart
$ git checkout master
$ docker-compose up -d
```
The application now runs in http://localhost:5000