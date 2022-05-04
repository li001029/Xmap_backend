# Dockerized Flask Application 
We use docker container to standardise everything (versions/libraries). In one word, you'll find it more convenient and elegant to write/debug code in docker container env (instead of on your laptop's local env).

## Quick Start 
1. In terminal, run the above command to do some cleaning. 
```shell
## Delete all containers using the following command
docker rm -f $(docker ps -a -q)
## Delete all volumes using the following command
docker volume rm $(docker volume ls -q)
```
2. To build, create and run the container, run the following command and this will take miniutes to finish
```shell
# For the first time
# Or whenever you want to update the image, 
# e.g changing Dockerfile, requirements.txt
docker-compose up -d --build
  
# Otherwise
docker-compose up -d
```
> You should see new containers created and running as above. 

3. Application now is hosted on `localhost:5001` 

4. Close connexion with container; Shut down container
    * In terminal, run the command below. It will shutdown and remove container (as you can see it disappears from Docker Desktop > Containers / Apps)
    ```shell
    docker-compose down
    ```

## Project Structure 
    .
    ├── README.md  # Readme file
    ├── docker-compose.yml # Development config for docker compose in debug mode
    └── flask_docker  # Rest API backend docker files

