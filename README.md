## Github repo of microservices
 - [Frontend](https://github.com/cloudyuga/e-cart-frontend)
 - [Catalogue](https://github.com/cloudyuga/e-cart-catalogue)
 - [User](https://github.com/cloudyuga/e-cart-user)
 - [Cart](https://github.com/cloudyuga/e-cart-cart)
 - [Orders](https://github.com/cloudyuga/e-cart-orders/tree/orders-for-payment-go)
 - [Payment](https://github.com/cloudyuga/e-cart-payment/tree/payment-go)

# Steps to run the application
Prerequiste: git, docker and docker-compose needs to be installed on the host machine

```sh
$ git clone https://github.com/cloudyuga/e-cart.git
$ cd e-cart
$ git checkout sixth-payment-go
$ docker-compose up -d
```
The application now runs in http://localhost:5000
