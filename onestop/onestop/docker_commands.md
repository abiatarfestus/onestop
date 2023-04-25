docker-compose up -d --no-deps --build <service_name>
Django: Running management commands inside a Docker container: 
    $ docker ps
    docker exec -it <django container name> bash
Finding volumes on the host:
    For Docker version 20.10.+ : \\wsl$\docker-desktop-data\data\docker\volumes
    For Docker Engine v19.03: \\wsl$\docker-desktop-data\version-pack-data\community\docker\volumes\