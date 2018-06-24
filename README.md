# SI Project

## Postman

Postman Collection: https://www.getpostman.com/collections/e6e00ce3785eef4a9aa5

## Kubernetes

Running via `minikube`:

- First run

    1. Start VM
        ```bash
        $ minikube start
        ```
    2. Set-up Kubernetes docker environment
        ```bash
        $ eval $(minikube docker-env)
        ```
    3. Build images
        ```bash
        # build all images
        $ docker-compose build
        # or chosen ones
        $ docker-compose build aggregator-service image-service-resnet50
        ```

        Info: In case you may run out of memory skip while building image service (eg. vgg19) skip it in whole process

    4. Generate self-signed TLS certificate
        ```bash
        $ openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=*.minikube"
        ```
    5. Add generated certificate to cluster
        ```bash
        $ kubectl -n kube-system create secret tls tls-minikube-system --key=tls.key --cert=tls.crt
        $ kubectl create secret tls tls-minikube-default --key=tls.key --cert=tls.crt
        ```
    6. Deploy main services to cluster
        ```bash
        $ kubectl apply -f kubernetes/traefik
        $ kubectl apply -f kubernetes/aggregator-service
        ```
    7. Point *.minikube domains to local cluster entrypoint:
        ```bash
        $ echo "$(minikube ip) aggregator-service.minikube dashboard.minikube" | sudo tee -a /etc/hosts
        ```

    8. Wait for all pods to be in running state
        ```bash
        $ kubectl get pods --all-namespaces
        ```
        or use cluster dashboard:

        ```bash
        $ minikube dashboard
        ```

    9. Deploy image services:
        ```bash
        $ kubectl apply -f kubernetes/image-service-resnet50
        $ kubectl apply -f kubernetes/image-service-vgg19
        $ kubectl apply -f kubernetes/image-service-xceptv1
        $ kubectl apply -f kubernetes/image-service-inceptv3
        ```

        Info: Deploying all services on local computer escpecially with many replicas can cause issues, so it is not recommended

    10. (Optionally) Point image services to local minikube domain:
        ```bash
        $ echo "$(minikube ip) image-service-resnet50.minikube image-service-vgg19.minikube image-service-xceptv1.minikube image-service-inceptv3.minikube" | sudo tee -a /etc/hosts
        ```

        Info: You can use image services via aggregator without exposing them to the world by disabling their ingress controllers

- Available services:
    - [Aggregator Service](https://aggregator-service.minikube)
        ```bash
        $ curl -k https://aggregator-service.minikube/status
        ```
    - Image Services:
        ```bash
        $ curl -k https://image-service-resnet50.minikube/status
        $ curl -k https://image-service-vgg19.minikube/status
        $ curl -k https://image-service-inceptv3.minikube/status
        $ curl -k https://image-service-xceptv1.minikube/status
        ```
    - [Traefik Dashboard (Load Balancer)](https://dashboard.minikube)

        Basic auth credentials:

        ```
        username: admin
        password: admin
        ```

## Docker

Running via `docker-compose`:

- Basic:
    ```bash
    $ echo "127.0.0.1 image-resnet50.docker.localhost image-vgg19.docker.localhost image-inceptv3.docker.localhost image-xceptv1.docker.localhost aggregator-service.docker.localhost" | sudo tee -a /etc/hosts
    $ docker-compose up
    ```
    Go to http://localhost:8080/dashboard/ to see traefik dashboard

- Advanced:
    ```bash
    $ docker-compose up [-d] [--pull] [--build] [--scale image-service=5]
    ```
    Options:
    - `-d` - run in background
    - `--pull` - enforce to pull new images from docker hub
    - `--build` - enforce to rebuild dockerfiles
    - `--scale aggregator-service=5` - scale container having name "aggregator-service" to five instances

- Logs
    ```bash
    $ docker-compose logs [-f] [name]
    ```
    - `-f` - follow logs in real-time
    - `name` - show logs only of specific container by its name

- Testing Aggregator Service:
    - `/status` endpoint
      ```bash
      $ curl -H "Host: aggregator-service.docker.localhost" http://127.0.0.1
      ```
