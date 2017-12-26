# Workflow of breaking down a Monolith Application into Microservices

## Monolith Application:
![](images/Monolith.jpeg?raw=true)

### Catalogue
'Catalogue' consists the product details such as product name, price, etc

### User
'User' contains the data and workflow related to user registration and login

### Cart
'Cart' has the information of the products that has been added to cart by the user

### Orders
'Orders' contains the details of all the orders placed by the user

### Payment
'Payment' contains the payment details for the orders placed by the user

## Extracting components one by one from the monlith
Our end goal is to convert the monolith application into microservices that run independent of each other. To accomplish this, we need to extract the service one by one from the monolith without breaking the application. The order of extraction should be decided based on the current implementation of the monolith.

Here, the monolith uses SQLdb for persistence. Joins have been implemented between the tables. For this reason, we need to extract the component that does not have dependency on any other components. The following order will be followed while extracting the components so as to not to break the application:

- Payment
- Orders
- Cart
- User
- Catalogue

## Extracting Payment Service from Monolith
![](images/Payment.jpeg?raw=true)

Here, Payment is extracted from the monolith.

Payment is now a separate entity without any dependency on the monolith. It has its own database as NoSQL MongoDB

The communication with the monolith happens through API calls.

[Github Repo](https://github.com/cloudyuga/e-cart/tree/first-breakdown-payment-service)

## Extracting Orders Service from Monolith
![](images/Orders.jpeg?raw=true)

Similarly, Orders service is extracted next from the monolith.

Orders service communicates with Payment service and monolith through API calls.

[Github Repo](https://github.com/cloudyuga/e-cart/tree/second-breakdown-orders)

## Extracting Cart Service from Monolith
![](images/Cart.jpeg?raw=true)

Next, we extract Cart service from the monolith. Cart service now communicates with Orders and the monolith through API calls.

[Github Repo](https://github.com/cloudyuga/e-cart/tree/third-breakdown-cart)

## Extracting User Service from Monolith
![](images/User.jpeg?raw=true)

User service is extracted from monolith and it now communicates with monolith through API calls.

[Github Repo](https://github.com/cloudyuga/e-cart/tree/fourth-breakdown-user)

## Extracting Catalogue from Monolith
[Github Repo](https://github.com/cloudyuga/e-cart/tree/fifth-breakdown-catalogue)

Once we extract the Catalogue service from monolith, our monolith is left with just the Frontend. We make Frontend as an individual service as well.
![](images/Catalogue.jpeg?raw=true)


Frontend communicates with all the other services through API calls. Other services talk among themselves through API calls when necessary.

With this, we have broken down a complete monolith application into microservices that run independent of each other.

Each service can be written in any language, backed by any database. They only need to handle the API calls appropriately. 

Each service runs in docker containers which are invoked using docker-compose.

## Github repo of microservices
 - [Frontend](https://github.com/cloudyuga/e-cart-frontend)
 - [Catalogue](https://github.com/cloudyuga/e-cart-catalogue)
 - [User](https://github.com/cloudyuga/e-cart-user)
 - [Cart](https://github.com/cloudyuga/e-cart-cart)
 - [Orders](https://github.com/cloudyuga/e-cart-orders)
 - [Payment](https://github.com/cloudyuga/e-cart-payment)

# Steps to run the application
Prerequiste: git, docker and docker-compose needs to be installed on the host machine

```sh
$ git clone https://github.com/cloudyuga/e-cart.git
$ cd e-cart
$ git checkout ninth-prometheus
$ docker-compose up -d
```
The application now runs in http://localhost:5000
