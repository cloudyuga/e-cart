## Github repo of microservices
 - [Frontend](https://github.com/cloudyuga/e-cart-frontend/tree/frontend-prometheus)
 - [Catalogue](https://github.com/cloudyuga/e-cart-catalogue/tree/catalogue-opentracing)
 - [User](https://github.com/cloudyuga/e-cart-user/tree/user-jaeger-with-time-delay)
 - [Cart](https://github.com/cloudyuga/e-cart-cart/tree/cart-prometheus)
 - [Orders](https://github.com/cloudyuga/e-cart-orders/tree/orders-prometheus)
 - [Payment](https://github.com/cloudyuga/e-cart-payment/tree/payment-go-opentracing)

# Steps to run the application
Prerequiste: Kubernetes needs to be installed

Start all the yaml files under k8s using kubectl and execute the below commands

```sh
$ minikube service frontend
$ minikube service jaeger-query
```

In JaegerUI, find traces of "catalogue" and "user"
