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
$ git checkout tenth-load-test
$ docker-compose up -d
```
The application now runs in http://localhost:5000

Now execute loadTest.py file to execute a series of requests on our application

```sh
$ cd load
$ python3 loadTest.py localhost 5000
```

Navigate to http://localhost:9090 to access the prometheus server.

Enter **request_count** in the expression field and click on execute to see number of requests that has been made on our application.
