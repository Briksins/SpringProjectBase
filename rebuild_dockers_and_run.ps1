# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\clean_dockers.ps1
docker volume rm db_data
docker volume create --name db_data -d local
.\gradle_build.ps1
docker-compose up --build
