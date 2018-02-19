## Github repo of microservices
 - [Frontend](https://github.com/cloudyuga/e-cart-frontend/tree/frontend-prometheus)
 - [Catalogue](https://github.com/cloudyuga/e-cart-catalogue)
 - [User](https://github.com/cloudyuga/e-cart-user)
 - [Cart](https://github.com/cloudyuga/e-cart-cart)
 - [Orders](https://github.com/cloudyuga/e-cart-orders/tree/orders-for-payment-go)
 - [Payment](https://github.com/cloudyuga/e-cart-payment/tree/payment-go-opentracing)

# Steps to run the application
Prerequiste: git, docker and docker-compose needs to be installed on the host machine

```sh
$ git clone https://github.com/cloudyuga/e-cart.git
$ cd e-cart
$ git checkout eighth-payment-opentracing
$ docker-compose up -d
```
The application now runs in http://localhost:5000

Now register a user and make payment for an item. Then navigate to http://localhost:8700/traces to see the traces on /payment
