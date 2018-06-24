# SI Project

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
        $ docker-compose build --pull
        ```
    4. Generate self-signed TLS certificate
        ```bash
        $ openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=*.minikube"
        ```
    5. Add generated certificate to cluster
        ```bash
        $ kubectl -n kube-system create secret tls tls-minikube-system --key=tls.key --cert=tls.crt
        $ kubectl create secret tls tls-minikube-default --key=tls.key --cert=tls.crt
        ```
    6. Deploy services to cluster
        ```bash
        $ kubectl apply -f kubernetes/traefik
        $ kubectl apply -f kubernetes/image-service
        ```
    7. Point *.minikube domains to local cluster entrypoint:
        ```bash
        $ echo "$(minikube ip) image-service.minikube dashboard.minikube" | sudo tee -a /etc/hosts
        ```

    8. Wait for all pods to be in running state
        ```bash
        $ kubectl get pods --all-namespaces
        ```
        or use cluster dashboard:

        ```bash
        $ minikube dashboard
        ```

- Available services:
    - [Image Service](https://image-service.minikube)
        ```bash
        $ curl -k https://image-service.minikube/status
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
    - `--scale image-service=5` - scale container having name "image-service" to five instances

- Logs
    ```bash
    $ docker-compose logs [-f] [name]
    ```
    - `-f` - follow logs in real-time
    - `name` - show logs only of specific container by its name

- Testing Image Service:
    - `/status` endpoint
      ```bash
      $ curl -H "Host: image.docker.localhost" http://127.0.0.1
      ```
