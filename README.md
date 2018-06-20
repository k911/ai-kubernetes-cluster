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
    4. Deploy services to cluster
        ```bash
        $ kubectl apply -f kubernetes/traefik
        $ kubectl apply -f kubernetes/image-service
        ```
    5. Point hosts to VM:
        ```bash
        $ echo "$(minikube ip) image-service.minikube dashboard.minikube" | sudo tee -a /etc/hosts
        ```

    6. Wait for all pods to be in running state
        ```bash
        $ kubectl get pods --all-namespaces
        ```
        or use cluster dashboard:

        ```bash
        $ minikube dashboard
        ```

- Available services:
    - [Image Service](http://image-service.minikube)
        ```bash
        $ curl image-service.minikube/status
        ```
    - [Traefik Dashboard (Load Balancer)](http://dashboard.minikube)

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
      $ curl -H Host:image.docker.localhost http://127.0.0.1
      ```
