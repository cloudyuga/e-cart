# "User service" extracted as an individual service from monolith

User service is extracted from the monolith.  It now runs as an individual service with MongoDB as its own database. 
It comunicates with the monolith through API calls.

![](images/User.jpeg?raw=true)

# Steps to run the application
Prerequiste: git, docker and docker-compose needs to be installed on the host machine

```sh
$ git clone https://github.com/cloudyuga/e-cart.git
$ cd e-cart
$ git checkout fourth-breakdown-user
$ docker-compose build
$ docker-compose up -d
```
The application now runs in http://localhost:5000
