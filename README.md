# "Catalogue service" extracted as an individual service from monolith

Catalogue service is extracted from the monolith.  It now runs as an individual service with MongoDB as its own database. 
It comunicates with the monolith through API calls.

At this step, the monolith is left with just the Frontend, which will be extracted in the next branch.

![](images/Catalogue.jpeg?raw=true)

# Steps to run the application
Prerequiste: git, docker and docker-compose needs to be installed on the host machine

```sh
$ git clone https://github.com/cloudyuga/e-cart.git
$ cd e-cart
$ git checkout fifth-breakdown-catalogue
$ docker-compose up -d
```
The application now runs in http://localhost:5000
