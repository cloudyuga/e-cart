# Monolith Application

The monolith application consists of 5 components(Catalogue, User, Cart, Orders, Payment) that is written using the Flask framework of Python and SQLdb for persistence.

![](images/monolith.jpeg?raw=true)

# Steps to run the application
Prerequiste: git, docker and docker-compose needs to be installed on the host machine

```sh
$ git clone https://github.com/cloudyuga/e-cart.git
$ cd e-cart
$ docker-compose up -d
```
The application now runs in http://localhost:5000
