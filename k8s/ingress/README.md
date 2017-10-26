### Carry out following deployments first.

#### Create the Namespace.
```
$ curl https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/namespace.yaml \
    | kubectl apply -f -

```

#### Create default Backend for the Nginx ingress controller.
```
$ curl https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/default-backend.yaml \
    | kubectl apply -f -

```

#### Create ConfigMap for the Nginx ingress controller.
```
$ curl https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/configmap.yaml \
    | kubectl apply -f -
    
$ curl https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/tcp-services-configmap.yaml \
    | kubectl apply -f -

$ curl https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/udp-services-configmap.yaml \
    | kubectl apply -f -
```

#### Set the RBAC rules.
```
$ curl https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/rbac.yaml \
    | kubectl apply -f -
```

Create the `Nginx ingress controller` configuration file as shown below.
```
$ vi ingress-controller.yaml

apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-ingress-controller
  namespace: ingress-nginx 
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ingress-nginx
  template:
    metadata:
      labels:
        app: ingress-nginx
      annotations:
        prometheus.io/port: '10254'
        prometheus.io/scrape: 'true'
    spec:
      serviceAccountName: nginx-ingress-serviceaccount
      hostNetwork: true
      containers:
        - name: nginx-ingress-controller
          image: gcr.io/google_containers/nginx-ingress-controller:0.9.0-beta.15
          args:
            - /nginx-ingress-controller
            - --default-backend-service=$(POD_NAMESPACE)/default-http-backend
            - --configmap=$(POD_NAMESPACE)/nginx-configuration
            - --tcp-services-configmap=$(POD_NAMESPACE)/tcp-services
            - --udp-services-configmap=$(POD_NAMESPACE)/udp-services
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
          ports:
          - name: http
            containerPort: 80
          - name: https
            containerPort: 443

```

Deploy the Nginx Ingress controller.
```
$ kubectl create -f ingress-controller.yaml
```
### Deploy the E-cart application using the following commnads.
```
$ git clone https://github.com/cloudyuga/e-cart.git
$ cd e-cart
$ git checkout master
$ kubectl create -f ./k8s/
```
Once your service and deployments get created. We can create the Ingress object for our E-cart application.

```
$ vim vhost_ingress.yaml

apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: vhost-ingress
spec:
  rules:
  - host: cy.myweb.com
    http:
      paths:
      - backend:
          serviceName: frontend
          servicePort: 5000

```

Deploy the Ingress.
```
$ kubectl create -f vhost_ingress.yaml
ingress "vhost-ingress" created
```
Lets take a look at the ingress.
```
$ kubectl get ing
NAME            HOSTS          ADDRESS         PORTS     AGE
vhost-ingress   cy.myweb.com   165.227.65.31   80        1m

```
Edit the `/etc/hosts` file  on your host from where you want to access the application and create records of `cy.myweb.com` with above shown address for me it is `165.227.65.31`.

Now open browser. and try to access the http://cy.myweb.com/ you will access the E-cart web application.
