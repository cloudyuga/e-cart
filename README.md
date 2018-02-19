## Github repo of microservices
 - [Frontend](https://github.com/cloudyuga/e-cart-frontend/tree/frontend-prometheus)
 - [Catalogue](https://github.com/cloudyuga/e-cart-catalogue/tree/catalogue-prometheus)
 - [User](https://github.com/cloudyuga/e-cart-user/tree/user-prometheus)
 - [Cart](https://github.com/cloudyuga/e-cart-cart/tree/cart-prometheus)
 - [Orders](https://github.com/cloudyuga/e-cart-orders/tree/orders-prometheus)
 - [Payment](https://github.com/cloudyuga/e-cart-payment/tree/payment-go-opentracing)

# Steps to run the application
Prerequiste: git, docker and docker-compose needs to be installed on the host machine

```sh
$ git clone https://github.com/cloudyuga/e-cart.git
$ cd e-cart
$ git checkout ninth-prometheus
$ docker-compose up -d
```
The application now runs in http://localhost:5000

Make few requests and navigate to http://localhost:9090 to access the prometheus server.

Enter **request_count** in the expression field and click execute to see the requests made on frontend, catalogue, user, cart and orders services.
