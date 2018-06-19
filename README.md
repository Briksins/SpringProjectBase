# About Project

This project was designed to be the start base for any `Spring Boot` project with Dockerized infrastructure, 
which would include the following containers:
    
    * Reverse Proxy Server (Nginx)
    * Server API (Spring Boot Application)
    * Database (PostgreSQL)

![Docker Schema](https://i.gyazo.com/1a42d9882f93f8480ece05cabf570c18.png "Docker Schema")

Everything is controlled trough `docker-compose` which automatically manage containers, internal networks and 
shared volume for data persistence.

The project support cross-platform build and can be run on Windows / Mac / Linux


# Renaming Project

Project can be cloned and renamed to match your needs with use of `RenameProject.py` script.

Here are the steps:
1. Clone Project
2. Rename project root folder from `SpringProjectBase` to `<YourProjectName>`
3. Navigate inside `<YourProjectName>` space trough `CMD` || `Terminal`
4. Execute:
    ```
    python RenameProject.py package=com.yourpackage
    ``` 
    It will rename the whole project, all references inside as well as java package name
5. Import project as `gradle` project in your IDE
6. Done


# Running Project

The project can be run by calling `rebuild_dockers_and_run.[sh || ps]` script.
It will compile and re-build everything automatically as well as create docker images and start containers
trough `docker-compose`

**Note for Windows users:** To execute `PowerShell` script on `Windows` trough `CMD` it is required to grant permission. 
It is single time activity per user, but still required to run in `PowerShell`:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```


# Components in details

## Spring - REST API Server

#### Description:
This project contains bare minimum of Spring Boot application which would be easy to wipe and continue 
with your own project.<br/> 
Spring App contains the following functionality:

* Application
    * Main Application to run
    * Simple Controller
        * Hello World
        * Add Item
        * Get Item by ID
        * Get All Items
        * Health Check
    * Database DAO, Model and Service Implementation
    * Properties configuration for PostgreSQL
    * Pre-populated DB dummy data with DB Schema trough prepared `SQL` files in `src/main/resources`
* Tests
    * Tests to test all APIs in controller
    * Properties configuration for H2 database
    * Pre-populated DB dummy data with DB Schema trough prepared `SQL` files in `src/test/resources`

#### Build Artifact:

The project require `gradle v4.7` for the build and can be build locally by simply executing `gradle build` command<br/>
However, to be platform independent as well as do not configure and maintain `gradle` package locally 
the project designed to be build with use of docker container. 

The `Dockerfile` located in `deployment/build/Dockerfile`

For simplicity project contains scrip `gradle_build.[sh || ps1]` which can be executed as on Windows in `PowerShell` 
as well as on Mac or Linux using bash.

To speedup the build and do not pull `gradle` dependencies each build it is recommended to mound `gradle cache` to the 
local space.

The `Docker` command for the build:

```
docker run -it --rm -v gradle:/home/gradle/.gradle/ -v $(pwd):/opt/SpringProjectBase -e ACTION=build gradle-build
```

This command mount local `gradle` volume to container to store persistent all downloaded dependencies<br/>
And mount local project to `/opt/<YourProjectName>` (if you renamed it). Once build is complete it will produce
`Build/lib` folder with required jar artifact.

**Note:** that command can be used not only for the `gradle build`, but also for any other pre-defined `gradle` 
action like `gradle test` for example. For that just change the value of `ACTION` environment variable

#### Docker Image:

The `Dockerfile` is located in `deployment/target/Dockerfile`. It is based on `Alpine OS` to reduce size with latest
available for Alpine `OpenJDK 1.8`

During the build process it execute the following steps:

* Setup Health Check
* Add custom spring user and group (to not run service as a root)
* Copy artifact from `build/libs/*.jar` (**Note:** The Artifact need to be already present from previous step 
`Build Artifact`)
* Change ownership
* Expose 8080 ports (only for internal docker network)
* Run Spring Boot jar (Tomcat is embedded this days, no need to drop *.war's anymore in `webapps` folder)

Docker image can be build manually with:
```
docker build -t backend_server . -f deployment/target/Dockerfile
```
But usually this process controlled by `docker-compose`

**Note:** If you run container on its own it will more likely to fail dew to missing database. 
For simplicity you can run DB in container (see below teh chapter about DB), but don't forgot to expose the ports 
to your local machine as well as make record in system `hosts` file to resolve correctly `postgres_db` hostname or
update property file for custom connection.


## PostgreSQL Database

The `Dockerfile` is located in `deployment/db/Dockerfile`. It is based on original Postgres Alpine image.<br/>
It implements only Health Check, no any other changes.

**Note Windows Users:** For persistent storage you cannot simply mount a local folder to container, as Postgres 
in the docker running in Linux environment and cannot have data to be stored in Windows `NTFS`. 
Therefore to solve this problem create Docker Volume:

```
docker volume create --name <db_data> -d local
```

This process is automated in the script `rebuild_dockers_and_run.[sh || ps]` and if you don't what that
your data is wiped each docker image re-build just comment it out.


## Nginx - Reverse Proxy Server

Using Nginx Alpine OS as base images to reduce container size as maximum as possible<br/>
`Dokcerfile` and `nginx.conf` are located in: `deployment/proxy/` folder

It implements Health Check and overwrite default `Nginx` config.

Docker build command:

```
docker build -t nginx_proxy . -f deployment/proxy/Dockerfile
```


 
 